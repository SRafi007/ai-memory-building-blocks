# app/memory/long_term.py

from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance, SearchRequest
from sentence_transformers import SentenceTransformer
from app.memory.schema import LongTermMemoryEntry
from uuid import uuid4
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


class LongTermMemory:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6333,
        collection_name: str = "long_term_memory",
        embedding_model: str = "all-MiniLM-L6-v2",
        vector_size: int = 384,  # default for MiniLM
    ):
        self.collection_name = collection_name
        self.client = QdrantClient(host=host, port=port)
        self.model = SentenceTransformer(embedding_model)

        self._ensure_collection(vector_size)

    def _ensure_collection(self, vector_size: int):
        if not self.client.collection_exists(self.collection_name):
            logger.info(f"Creating Qdrant collection: {self.collection_name}")
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            )

    def add_entry(
        self, user_id: str, text: str, metadata: Optional[dict] = None
    ) -> str:
        embedding = self.model.encode(text).tolist()
        entry_id = str(uuid4())
        metadata = metadata or {}

        point = PointStruct(
            id=entry_id,
            vector=embedding,
            payload={"user_id": user_id, "text": text, "metadata": metadata},
        )

        self.client.upsert(collection_name=self.collection_name, points=[point])
        return entry_id

    def search(
        self, query_text: str, top_k: int = 5, user_id: Optional[str] = None
    ) -> List[LongTermMemoryEntry]:
        query_vector = self.model.encode(query_text).tolist()
        filters = None

        results = self.client.search(
            collection_name=self.collection_name, query_vector=query_vector, limit=top_k
        )

        memory_entries = []
        for result in results:
            payload = result.payload
            if user_id and payload.get("user_id") != user_id:
                continue

            memory_entries.append(
                LongTermMemoryEntry(
                    id=str(result.id),
                    user_id=payload["user_id"],
                    text=payload["text"],
                    metadata=payload.get("metadata", {}),
                    embedding=result.vector,
                )
            )

        return memory_entries
