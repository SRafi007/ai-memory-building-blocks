# app/memory/long_term.py

from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance
from sentence_transformers import SentenceTransformer
from app.memory.schema import LongTermMemoryEntry
from uuid import uuid4
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

COLLECTION_NAME = "long_term_memory"


class LongTermMemory:
    def __init__(
        self,
        host="localhost",
        port=6333,
        model_name="all-MiniLM-L6-v2",
        vector_size=384,
    ):
        self.client = QdrantClient(host=host, port=port)
        self.model = SentenceTransformer(model_name)
        self.vector_size = vector_size
        self._ensure_collection()

    def _ensure_collection(self):
        if not self.client.collection_exists(collection_name=COLLECTION_NAME):
            self.client.recreate_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=self.vector_size, distance=Distance.COSINE
                ),
            )
            logger.info(f"Created Qdrant collection: {COLLECTION_NAME}")

    def _embed(self, text: str) -> List[float]:
        return self.model.encode(text).tolist()

    def add_entry(
        self, user_id: str, text: str, metadata: Optional[dict] = None
    ) -> str:
        embedding = self._embed(text)
        point_id = str(uuid4())
        entry = LongTermMemoryEntry(
            id=point_id,
            user_id=user_id,
            text=text,
            metadata=metadata or {},
            embedding=embedding,
        )
        point = PointStruct(
            id=point_id,
            vector=embedding,
            payload={
                "user_id": entry.user_id,
                "text": entry.text,
                "metadata": entry.metadata,
                "timestamp": entry.timestamp.isoformat(),
            },
        )
        self.client.upsert(collection_name=COLLECTION_NAME, points=[point])
        logger.info(f"Added entry to LTM: {point_id}")
        return point_id

    def query(self, user_id: str, query_text: str, top_k: int = 5) -> List[dict]:
        query_vector = self._embed(query_text)
        results = self.client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            limit=top_k,
            query_filter={"must": [{"key": "user_id", "match": {"value": user_id}}]},
        )
        return [
            {
                "text": hit.payload["text"],
                "score": hit.score,
                "metadata": hit.payload.get("metadata", {}),
            }
            for hit in results
        ]
