# 🧠 GAME Agent Framework  
### *A Modular, Extensible Agentic AI System Built on the GAME Architecture (Goals · Actions · Memory · Environment)*

---

## 🚀 Overview

This repository implements a **modular Agentic AI framework** based on the **G.A.M.E. architecture**:

```
G → Goals  
A → Actions  
M → Memory  
E → Environment  
```


The framework is designed to build **tool-driven autonomous agents** that operate through **structured decision loops**, rather than free-form text generation.

It supports **multiple LLM providers**, **agent specialization**, **model routing**, and **safe tool execution**, making it suitable for real-world agentic systems—not just demos.

---

## 🧩 Key Ideas

- Agents **never act directly** — they reason → choose tools → observe results
- Behavior is shaped primarily by **Goals**, not hard-coded logic
- Tools are **first-class primitives**, not prompt hacks
- LLMs are **pluggable infrastructure**, not embedded assumptions

## 🔐 Design Guarantees

- No side-effects without tools
- No implicit actions
- Deterministic agent loop
- Centralized model selection

---

## ⭐ Features

### 🔧 Modular GAME Components

- **Goals**  
  Define *what* the agent should achieve and *how* it should behave

- **Actions**  
  Explicit capabilities implemented as plain Python functions, registered via decorators

- **Memory**  
  Memory is append-only and scoped per agent execution unless explicitly persisted.

- **Environment**  
  Executes real side-effects (filesystem, outputs, APIs)

---

### 🧠 Multi-Agent Architecture

Agents are **specialized**, not generic:

- **File Agent**
  - Explore project files
  - Read & search code
  - Explain structure and behavior

- **README Agent**
  - Inspect project files  
  - Infer architecture and purpose  
  - Generate a structured README  
  - Write it to the `output/` directory
  - This demonstrates **agent-driven content creation with real side-effects**, not just text output.

Agents are created via a central **AgentFactory**, making it easy to add new agent types without touching the core loop.


---

### ⚙️ Pluggable LLM Backends

Supported via a unified interface:

- **Groq**  
  - Fast inference
  - Tool-calling capable models (Llama / Qwen)

- **Portkey**
  - Used with **`gpt-4o-mini`**
  - Reliable function calling
  - Ideal for complex multi-step agents

LLM selection is controlled centrally via config and routing logic — **no agent hard-codes a model**.

---

### 🧭 Model Routing & Registry

- Central **model registry** with metadata (provider, cost tier, capabilities)
- Router selects the best model based on:
  - Provider
  - Tool-calling reliability
  - User preference (pinned vs automatic)

This avoids scattering model decisions across agents.

---

### 🛠 Tool Registration Model

Tools are defined as **plain Python functions** and registered globally via decorators.

```python
@register_tool(tags=["file_operations", "read"])
def read_file(file_path: str) -> str:
    """Reads and returns the content of a file."""
    with open(file_path) as f:
        return f.read()
```
Key properties:
- Single source of truth (function + docstring + type hints)
- Automatic schema generation
- No manual registries or merging
- Tools become available only **when imported**

### 🔄 Agent Execution Loop
Each agent runs a structured loop:

- Construct prompt from Goals + Memory + Tools
- Ask LLM to choose **exactly one tool**
- Execute tool via the Environment
- Store result in Memory
- Repeat until the agent signals completion
- This enforces **predictability, safety, and debuggability**.  

### ⛔ Termination & Safety Guarantees

- Agents have a maximum iteration limit
- Only one tool call is allowed per step
- Invalid tool calls immediately halt execution
- Agents must explicitly emit a TERMINATE decision

---

## 📦 Project Structure

```
game-framework/
│
├── main.py                     # Entry point
├── output/                     # Agent-generated artifacts (gitignored)
│
└── game/
    ├── agents/                 # AgentFactory + agent implementations
    │   ├── file_agent/
    │   └── readme_agent/
    │
    ├── actions/                # Action definitions + registries
    │   └── core/
    │
    ├── goals/                  # Goal definitions
    ├── memory/                 # Memory abstraction
    ├── environment/            # Action executor
    ├── language/               # Prompt + parsing logic
    ├── core/                   # Agent loop
    ├── llm/                    # LLM clients, routing, registry
    └── config/                 # Global configuration
```

---

## 🔍 Architecture Diagram

```
            ┌───────────────────────┐
            │      AgentFactory     │
            │ (selects agent type)  │
            └───────────┬───────────┘
                        │
                        ▼
            ┌───────────────────────┐
            │        Agent          │
            │     (GAME Loop)       │
            └───────────┬───────────┘
                        │
        ┌───────────────┼──────────────────┐
        │               │                  │
        ▼               ▼                  ▼
┌────────────┐   ┌────────────┐     ┌────────────┐
│   Goals    │   │   Memory   │     │   Actions  │
│ (what/how) │   │ (context)  │     │  (tools)   │
└────────────┘   └────────────┘     └────────────┘
                        │
                        ▼
              ┌──────────────────┐
              │        LLM       │
              │  (Groq / Portkey)│
              └──────────┬───────┘
                         │
                         ▼
              ┌──────────────────┐
              │   Environment    │
              │ (FS / output /   │
              │  side-effects)   │
              └──────────────────┘
```

---

## 🧪 Example Usage  

When you run:

```
python main.py
```

Example interaction:

```
Available agents: file | readme
Select agent: readme
[LLM] Provider=Portkey | Model=gpt-4o-mini
Task: Analyze the .py files in the project and generate a README

Agent thinking...
Agent Decision: {'tool': 'list_project_files', 'args': {'dir_path': ''}}
Action Result: {'tool_executed': True, 'result': ['.gitignore', 'main.py', '.git', '.gitattributes', 'README.md', 'game', 'output', '__pycache__'], 'timestamp': '2025-12-19T19:07:16+0000'}
....

Agent thinking...
Agent Decision: {'tool': 'read_file', 'args': {'file_name': 'game/actions/action.py'}}
Action Result: {'tool_executed': True, 'result': 'from typing import Callable, Dict, Any\n\nclass Action:\n ..... return self.function(**args)\n\n', 'timestamp': '2025-12-19T19:07:26+0000'}
....
Agent thinking...
Agent Decision: {'tool': 'terminate', 'args': {'message': 'The README has been fully generated and written to disk.'}}
Action Result: {'tool_executed': True, 'result': 'The README has been fully generated and written to disk.', 'timestamp': '2025-12-19T19:07:46+0000'}
Agent requested termination
```
---

## ⚙️ Configuration

All runtime behavior is controlled via a **global config**:

- LLM provider (Groq / Portkey)  
- Model selection strategy  
- Token limits  
- Agent verbosity & iteration limits  

This allows changing behavior **without touching agent code**.

The active LLM provider (Groq or Portkey) is selected via configuration and routing logic — no agent hardcodes credentials or models.

---

## 🚀 Getting Started

### 1️⃣ Install dependencies

```bash
pip install groq portkey-ai
```

---

### 2️⃣ Export your Groq API key

```bash
export GROQ_API_KEY="your_api_key_here"
export PORTKEY_API_KEY="your_portkey_api_key"
export PORTKEY_VIRTUAL_KEY="your_virtual_key"
```

---

### 3️⃣ Run the agent

```bash
python main.py
```

---

## 🛠 Extending the Framework

### Create a new agent
1. Create a new folder under game/agents/
2. Define:
    - Goals
    - Optional agent-specific tools (via decorators)
3. Register the agent in AgentFactory

No changes to the core loop required.

```python
coding_agent = Agent(
    goals=[Goal(priority=1, name="coding", description="Write Python code")],
    agent_language=AgentLanguage(),
    action_registry=ActionRegistry(tags=["file_operations", "coding", "system"]),
    generate_response=llm,
    environment=Environment(),
)
```

---

## 🔮 Roadmap
- [ ] Multi-agent coordination
- [ ] RAG integration
- [ ] DevOps / GitHub / CI tools
- [ ] Policy & approval-gated tools
- [ ] Web UI (Streamlit / FastAPI)
- [ ] Evaluation & tracing hooks

---

## 🤝 Contributing

PRs welcome!  
If you’re exploring:

- Agentic architectures
- Tool-calling correctness
- LLM orchestration patterns

…this project is intentionally structured for learning and extension.
---

## 📄 License
MIT License

---

## 🙌 Acknowledgements

Built as part of my journey to learn and master **Agentic AI architectures**, structured tool-calling, and LLM orchestration patterns.
