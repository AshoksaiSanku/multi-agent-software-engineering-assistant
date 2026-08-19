from app.database.models import Repository
from app.services.ai_service import AIService
from app.vector_store.store import RepositoryVectorStore


async def architecture_report(repository: Repository) -> str:
    matches = await RepositoryVectorStore().query(
        repository.id, "explain repository architecture main functionality", 5
    )
    context = "\n\n".join(
        f"FILE: {match['file_path']}\n{match['content']}" for match in matches
    )
    return await AIService().complete(
        "Act as a software architect. Produce a markdown architecture report with "
        "sections for structure, risks, scaling, security, and next actions.",
        f"Repository: {repository.name}\nSummary metrics: {repository.summary}\n\nRepository context:\n{context}",
    )
