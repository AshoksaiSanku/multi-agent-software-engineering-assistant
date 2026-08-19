import asyncio
from dataclasses import dataclass

import chromadb
from openai import AsyncOpenAI
from sklearn.feature_extraction.text import HashingVectorizer

from app.core.config import settings


@dataclass
class VectorDocument:
    vector_id: str
    path: str
    chunk_index: int
    content: str


class RepositoryVectorStore:
    """Indexes source chunks in Chroma using OpenAI or deterministic local embeddings."""

    def __init__(self) -> None:
        self.client = chromadb.PersistentClient(path=str(settings.chroma_path))
        self.openai = None
        if settings.ai_provider.lower() == "openai" and settings.openai_api_key:
            self.openai = AsyncOpenAI(api_key=settings.openai_api_key)
        self.local_embedder = HashingVectorizer(
            n_features=384, alternate_sign=False, norm="l2"
        )

    def collection(self, repository_id: str):
        safe_id = repository_id.replace("-", "_")
        return self.client.get_or_create_collection(
            name=f"repo_{safe_id}", metadata={"hnsw:space": "cosine"}
        )

    async def delete_repository(self, repository_id: str) -> None:
        safe_id = repository_id.replace("-", "_")
        collection_name = f"repo_{safe_id}"
        try:
            await asyncio.to_thread(self.client.delete_collection, name=collection_name)
        except Exception as exc:
            message = str(exc).lower()
            if "does not exist" not in message and "not found" not in message:
                raise

    async def documents(self, repository_id: str) -> list[dict]:
        collection = await asyncio.to_thread(self.collection, repository_id)
        count = await asyncio.to_thread(collection.count)
        if not count:
            return []
        result = await asyncio.to_thread(
            collection.get, include=["documents", "metadatas"]
        )
        documents: list[dict] = []
        for content, metadata in zip(result["documents"], result["metadatas"]):
            documents.append(
                {
                    "file_path": metadata.get("path", "unknown"),
                    "chunk_index": metadata.get("chunk_index", 0),
                    "content": content,
                    "characters": len(content or ""),
                }
            )
        return documents

    async def embeddings(self, texts: list[str]) -> list[list[float]]:
        if self.openai:
            result = await self.openai.embeddings.create(
                model=settings.openai_embedding_model,
                input=texts,
                dimensions=384,
            )
            return [item.embedding for item in result.data]
        return self.local_embedder.transform(texts).toarray().tolist()

    async def index(self, repository_id: str, documents: list[VectorDocument]) -> None:
        collection = await asyncio.to_thread(self.collection, repository_id)
        existing = await asyncio.to_thread(collection.get)
        if existing["ids"]:
            await asyncio.to_thread(collection.delete, ids=existing["ids"])
        if not documents:
            return
        content = [document.content for document in documents]
        vectors = await self.embeddings(content)
        await asyncio.to_thread(
            collection.add,
            ids=[document.vector_id for document in documents],
            documents=content,
            metadatas=[
                {"path": document.path, "chunk_index": document.chunk_index}
                for document in documents
            ],
            embeddings=vectors,
        )

    async def query(self, repository_id: str, query: str, limit: int = 5) -> list[dict]:
        collection = await asyncio.to_thread(self.collection, repository_id)
        count = await asyncio.to_thread(collection.count)
        if not count:
            return []
        query_vector = await self.embeddings([query])
        result = await asyncio.to_thread(
            collection.query,
            query_embeddings=query_vector,
            n_results=min(limit, count),
        )
        matches: list[dict] = []
        for content, metadata, distance in zip(
            result["documents"][0], result["metadatas"][0], result["distances"][0]
        ):
            score = max(0.0, 1.0 - distance)
            if score == 0.0:
                score = 0.01
            matches.append(
                {
                    "file_path": metadata["path"],
                    "content": content,
                    "score": round(score, 4),
                }
            )
        return matches
