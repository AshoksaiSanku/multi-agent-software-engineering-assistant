# Lesson-14: Multi-Agent Workflow with LangGraph and WebSocket Events

## Objective

Implement the multi-agent engineering workflow and real-time event streaming.

## Files Created

```text
backend/app/agents/__init__.py
backend/app/agents/workflow.py
backend/app/services/agent_service.py
backend/app/services/generated_project_service.py
backend/app/api/routes/agents.py
```

## Knowledge Required

- **LangGraph**: Library for graph-based workflows.
- **State graph**: Workflow where each node receives and returns state.
- **Agent**: Specialized step that performs one task.
- **WebSocket**: Persistent connection for live updates.
- **Background task**: Long work that runs after HTTP response.
- **Generated artifact**: File content produced by the workflow.

## Data Flow

Requirements -> run id -> background workflow -> each node updates state -> event saved and streamed -> generated project saved -> ZIP available later.

## Common Mistakes

- WebSocket without authentication.
- Losing events if browser disconnects.
- Missing state keys between nodes.
- No persistent logs.

## Verification

Start an agent run and confirm logs appear and a generated project exists.

