# app/memory/long_term.py

import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import EmbeddingFunction
from typing import List, Optional
from app.memory.schema import LongTermMemoryEntry


class LongTermMemory:
    def __init__(
        self,
        collection_name: str = "long_term_memory",
        persist_dir: str = "./data/chroma",
        embedding_function: Optional[EmbeddingFunction] = None,
    ):
        self.client = chromadb.PersistentClient(path=persist_dir)

        self.embedding_function = embedding_function
        self.collection = self.client.get_or_create_collection(
            name=collection_name, embedding_function=embedding_function
        )

    def add(self, entry: LongTermMemoryEntry):
        if entry.embedding is None and self.embedding_function is not None:
            entry.embedding = self.embedding_function([entry.text])[0]

        self.collection.add(
            ids=[entry.id],
            documents=[entry.text],
            metadatas=[{"user_id": entry.user_id, **(entry.metadata or {})}],
            embeddings=[entry.embedding] if entry.embedding else None,
        )

    def query(self, query_text: str, n_results: int = 5) -> List[LongTermMemoryEntry]:
        if not self.embedding_function:
            raise ValueError("No embedding function provided for querying")

        query_embedding = self.embedding_function([query_text])[0]
        results = self.collection.query(
            query_embeddings=[query_embedding], n_results=n_results
        )

        entries = []
        for i in range(len(results["ids"][0])):
            entry = LongTermMemoryEntry(
                id=results["ids"][0][i],
                text=results["documents"][0][i],
                metadata=results["metadatas"][0][i],
                embedding=None,  # Embeddings not returned by default
            )
            entries.append(entry)

        return entries

    def delete(self, doc_id: str):
        self.collection.delete(ids=[doc_id])

    def list_ids(self) -> List[str]:
        return self.collection.peek()["ids"]

    def persist(self):
        self.client.persist()
