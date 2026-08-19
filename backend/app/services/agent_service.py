from collections import defaultdict

from fastapi import WebSocket

from app.agents.workflow import build_workflow
from app.database.models import AgentLog, GeneratedProject
from app.database.session import AsyncSessionLocal
from app.vector_store.store import RepositoryVectorStore


AGENT_STEPS = [
    "Requirement Analysis Agent",
    "Repository Understanding Agent",
    "Backend Generation Agent",
    "Frontend Generation Agent",
    "Documentation Agent",
    "Code Review Agent",
]


class AgentEventHub:
    def __init__(self) -> None:
        self.connections: defaultdict[str, set[WebSocket]] = defaultdict(set)

    async def connect(self, channel: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self.connections[channel].add(websocket)

    def disconnect(self, channel: str, websocket: WebSocket) -> None:
        self.connections[channel].discard(websocket)

    async def publish(self, channel: str, message: dict) -> None:
        dead: list[WebSocket] = []
        for websocket in self.connections[channel]:
            try:
                await websocket.send_json(message)
            except RuntimeError:
                dead.append(websocket)
        for websocket in dead:
            self.disconnect(channel, websocket)


event_hub = AgentEventHub()


async def record_event(
    run_id: str,
    user_id: str,
    repository_id: str | None,
    agent: str,
    status: str,
    message: str,
    payload: dict | None = None,
) -> None:
    event = {
        "run_id": run_id,
        "agent_name": agent,
        "status": status,
        "message": message,
        "payload": payload or {},
    }
    async with AsyncSessionLocal() as db:
        db.add(
            AgentLog(
                user_id=user_id,
                repository_id=repository_id,
                run_id=run_id,
                agent_name=agent,
                status=status,
                message=message,
                payload=payload or {},
            )
        )
        await db.commit()
    await event_hub.publish(repository_id or user_id, event)


async def execute_agent_run(
    run_id: str,
    user_id: str,
    repository_id: str | None,
    project_name: str,
    requirements: str,
) -> None:
    context = "No repository context provided."
    if repository_id:
        matches = await RepositoryVectorStore().query(repository_id, requirements, 5)
        context = "\n\n".join(
            f"{match['file_path']}:\n{match['content']}" for match in matches
        )
    await record_event(
        run_id, user_id, repository_id, "Orchestrator", "running", "Workflow started"
    )
    try:
        # LangGraph executes each named specialist and returns the accumulated deliverables.
        result = {"requirements": requirements, "repository_context": context}
        labels = {
            "requirements": AGENT_STEPS[0],
            "repository": AGENT_STEPS[1],
            "backend": AGENT_STEPS[2],
            "frontend": AGENT_STEPS[3],
            "documentation": AGENT_STEPS[4],
            "review": AGENT_STEPS[5],
        }
        async for update in build_workflow().astream(result, stream_mode="updates"):
            node, values = next(iter(update.items()))
            result.update(values)
            agent = labels[node]
            await record_event(
                run_id, user_id, repository_id, agent, "completed", f"{agent} completed"
            )
        files = {
            "backend/generated_feature.py": result["backend_code"],
            "frontend/src/GeneratedFeature.jsx": result["frontend_code"],
            "README.generated.md": result["documentation"],
            "CODE_REVIEW.md": result["review"],
            "IMPLEMENTATION_PLAN.md": result["plan"],
        }
        async with AsyncSessionLocal() as db:
            db.add(
                GeneratedProject(
                    user_id=user_id,
                    repository_id=repository_id,
                    name=project_name,
                    requirements=requirements,
                    files=files,
                )
            )
            await db.commit()
        await record_event(
            run_id, user_id, repository_id, "Orchestrator", "completed", "Artifacts ready"
        )
    except Exception as exc:  # pragma: no cover - model/network errors depend on runtime
        await record_event(
            run_id, user_id, repository_id, "Orchestrator", "failed", str(exc)[:500]
        )
