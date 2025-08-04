# app/memory/schema.py

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timezone


def now_utc():
    return datetime.now(timezone.utc)


class ShortTermMemoryEntry(BaseModel):
    session_id: str
    key: str
    value: str
    timestamp: datetime = Field(default_factory=now_utc)


class LongTermMemoryEntry(BaseModel):
    id: str
    user_id: str
    text: str
    metadata: Optional[dict] = {}
    embedding: Optional[List[float]] = None
    timestamp: datetime = Field(default_factory=now_utc)
