# examples/ltm_demo.py

import uuid
from app.memory.long_term import LongTermMemory
from app.memory.schema import LongTermMemoryEntry
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

# Initialize embedding function
embedding_fn = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

# Create LTM instance
ltm = LongTermMemory(embedding_function=embedding_fn)

# Add a memory
entry = LongTermMemoryEntry(
    id=str(uuid.uuid4()),
    user_id="user_001",
    text="User prefers meetings in the morning.",
    metadata={"type": "preference"},
)
ltm.add(entry)
ltm.persist()

# Query it back
results = ltm.query("When does the user prefer meetings?")
print("🔍 Query Results:")
for res in results:
    print("-", res.text)
