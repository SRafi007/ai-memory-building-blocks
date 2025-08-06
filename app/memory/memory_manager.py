# app/memory/memory_manager.py

from app.memory.short_term import ShortTermMemory
from app.memory.long_term import LongTermMemory
from typing import Optional, Dict, List
from app.memory.schema import LongTermMemoryEntry
from app.config import settings


class MemoryManager:
    def __init__(
        self,
        stm_ttl_minutes: int = settings.STM_TTL_MINUTES,
        collection_name: str = settings.LTM_COLLECTION_NAME,
        embedding_model: str = settings.LTM_EMBEDDING_MODEL,
    ):
        self.stm = ShortTermMemory(ttl_minutes=stm_ttl_minutes)
        self.ltm = LongTermMemory(
            collection_name=collection_name, embedding_model=embedding_model
        )

    # ===== STM Functions =====
    def set_short_term(self, session_id: str, key: str, value: str):
        self.stm.set(session_id, key, value)

    def get_short_term(self, session_id: str, key: str) -> str:
        return self.stm.get(session_id, key)

    def get_all_short_term(self, session_id: str) -> Dict[str, str]:
        return self.stm.get_all(session_id)

    def clear_short_term(self, session_id: str):
        self.stm.clear(session_id)

    # ===== LTM Functions =====
    def add_long_term(
        self, user_id: str, text: str, metadata: Optional[dict] = None
    ) -> str:
        return self.ltm.add_entry(user_id=user_id, text=text, metadata=metadata)

    def search_long_term(
        self, query: str, user_id: Optional[str] = None, top_k: int = 5
    ) -> List[LongTermMemoryEntry]:
        return self.ltm.search(query_text=query, user_id=user_id, top_k=top_k)

    # ===== Promotion Logic =====
    def promote_stm_to_ltm(self, session_id: str, user_id: str):
        """
        Save all STM key-values for this session as one LTM entry.
        """
        stm_data = self.stm.get_all(session_id)
        if not stm_data:
            return None

        combined_text = "\n".join([f"{k}: {v}" for k, v in stm_data.items()])
        metadata = {"source": "STM", "keys": list(stm_data.keys())}

        ltm_id = self.add_long_term(
            user_id=user_id, text=combined_text, metadata=metadata
        )
        self.clear_short_term(session_id)
        return ltm_id
