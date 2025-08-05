# AI Memory System

A modular, scalable memory framework for AI systems — designed to manage **Short-Term** and **Long-Term** memory contexts independently of any specific agent. This project provides a robust foundation for memory in chatbots, planners, task managers, and autonomous agents.

---

## Features

- **Short-Term Memory (STM)**: Fast, temporary context storage using in-memory or Redis backends.
- **Long-Term Memory (LTM)**: Persistent semantic memory using vector databases like ChromaDB or Qdrant.
- **Memory Manager**: Central interface for memory operations, routing intelligently between STM and LTM.
- **Pluggable Architecture**: Swap out storage, embedding models, or TTL logic easily.
- **Reusable**: Can be embedded into larger AI systems or used as a standalone memory module.

---

## Project Structure

```
ai_memory_system/
│
├── app/
│   ├── memory/                # STM, LTM, Memory Manager, Schemas
│   ├── storage/               # Storage backends: Redis, ChromaDB, Files
│   ├── utils/                 # Embeddings, Logging, Timers
│   └── config/                # Environment/config management
├── data/                      # Local file-based memory (for prototyping)
├── examples/                  # Demos using STM/LTM
├── tests/                     # Unit and integration tests
├── scripts/                   # Setup and seeding scripts
├── main.py                    # Entrypoint (for testing and demo)
└── README.md                  # You're here!
```

---

## Memory Concepts

| Type               | Role                                                                 |
|--------------------|----------------------------------------------------------------------|
| **Short-Term**     | Temporary memory (current session/task). Low-latency access.         |
| **Long-Term**      | Persistent memory across sessions. Supports vector similarity search.|
| **Memory Manager** | Orchestrates what to store/retrieve from STM or LTM.                 |

---

## Data Flow

Here's how memory flows between components in the system:

```text
                ┌──────────────────────────────┐
                │      Input from Agent        │
                └────────────┬─────────────────┘
                             │
                             ▼
              ┌─────────────────────────────┐
              │  Memory Manager (Router)    │
              └────────────┬────────────────┘
         ┌─────────────────┴────────────┐
         ▼                              ▼
┌──────────────────────┐     ┌────────────────────────┐
│ Short-Term Memory    │     │   Long-Term Memory     │
│ (in-memory or Redis) │     │ (Vector DB, e.g. Chroma│
└─────────┬────────────┘     └──────────┬─────────────┘
          │                             │
     Recent task,                      Stored facts,
     conversation,                     knowledge, history,
     or user session                   embeddings
          │                             │
          └────────────┬───────────────┘
                       ▼
              ┌────────────────────┐
              │   Memory Output    │
              └────────────────────┘
                       │
                       ▼
         Injected into agent, prompt, planner, etc.
```

## Setup Instructions

### 1. Clone the Repo
```bash
git clone https://github.com/yourusername/ai_memory_system.git
cd ai_memory_system
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
Edit the `.env` file (or `config/settings.py`) with the correct paths for:

- Redis or in-memory STM
- ChromaDB or Qdrant LTM
- Embedding model path/name

### 4. Run a Demo
```bash
python examples/chat_simulation.py
```

## Testing
```bash
pytest tests/
```

## Integration Use Cases

This memory system can be embedded into:

- Chatbots with memory and context
- Task planners or productivity agents
- Knowledge-based agents (RAG, AutoGPT clones)
- Multi-session user interaction platforms

## Future Enhancements

- Memory summarization (auto-condense STM for LTM)
- TTL policies for STM cleanup
- Embedding model plug-and-play via config
- Multi-user memory isolation

## Author

Built by Rafi Coding — AI systems explorer and engineer in progress