# 🧠 GAME Agent Framework  
### Deterministic, Tool-Driven Agentic AI Systems

> A minimal framework for building **controlled, debuggable, tool-calling agents** using the GAME architecture:  
> **Goals · Actions · Memory · Environment**

---

## Why This Exists

Most "agentic AI" systems blur together:
- reasoning
- execution
- side-effects
- and control flow

That makes them:
- hard to debug
- unsafe to run
- brittle across LLM providers
- unsuitable for real systems

This framework explores a **different approach**:

> **Agents reason, but only tools act.**  
> **The agent loop is deterministic.**  
> **Side-effects are explicit and auditable.**

The goal is **reliability over cleverness**.

---

## Core Design Principles

### 1. Agents Do Not Act Directly
Agents never modify the world on their own.

All side-effects happen via **explicit tools**, executed by the environment.

```
Reason → Select Tool → Execute → Observe → Repeat
```

---

### 2. Tools Are Plain Python Functions
There is no "Action" class hierarchy.

A tool is just:

```python
@register_tool(tags=["file_operations", "read"])
def read_file(path: str) -> str:
    ...
```

- Function signature defines inputs
- Docstring defines intent
- Type hints define schema
- Decorators handle registration

**One source of truth.**

---

### 3. Tool Availability Is Agent-Scoped
Tools are registered **globally**, but agents see only a **filtered view**.

```python
ActionRegistry(tags=["file_operations"])
```

This enables:
- least-privilege agents
- safe specialization
- predictable capabilities

---

### 4. The Agent Loop Is Deterministic
Every agent run follows a strict loop:

1. Construct prompt from **Goals + Memory + Tools**
2. LLM selects **exactly one tool**
3. Environment executes the tool
4. Result is appended to memory
5. Agent decides next step or completion

There is:
- no implicit branching
- no hidden retries
- no background execution

---

### 5. Termination Is an Agent Decision
Termination is **not a tool**.

The LLM may signal completion, but the **Agent** decides when to stop.

This avoids:
- provider-specific failures
- malformed "terminate" calls
- LLMs controlling lifecycle

---

## Architecture Overview

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

## Project Structure

```
game-framework/
│
├── main.py                     # Entry point
├── output/                     # Agent-generated artifacts
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

## Supported LLM Providers

### Groq
- Extremely fast inference
- Strict tool-calling enforcement
- Ideal for deterministic agents

### Portkey
- Used with `gpt-4o-mini`
- More tolerant tool calling
- Useful for exploratory agents

---

## Agents Included

### File Agent
- Explore repository structure
- Read files
- Explain code behavior

### README Agent
- Inspect project structure
- Infer architecture
- Generate documentation
- Write output to disk

---

## Getting Started

### 1️⃣ Install dependencies

```bash
pip install groq portkey-ai
```

### 2️⃣ Set up API keys

```bash
export GROQ_API_KEY="your_api_key_here"
export PORTKEY_API_KEY="your_portkey_api_key"
export PORTKEY_VIRTUAL_KEY="your_virtual_key"
```

### 3️⃣ Run an agent

```bash
python main.py
```

Example interaction:

```
Available agents: file | readme
Select agent: readme

Agent thinking...
Agent Decision: {'tool': 'list_project_files', 'args': {'dir_path': ''}}
Action Result: {'tool_executed': True, 'result': ['main.py', 'game/', ...]}

Agent thinking...
Agent Decision: {'tool': 'read_file', 'args': {'file_name': 'game/core/agent.py'}}
...

Agent Decision: {'tool': 'terminate', 'args': {'message': 'README generated'}}
Agent requested termination
```

---

## Extending the Framework

### Adding a New Agent

1. Create a folder under `game/agents/`
2. Define the agent's goals
3. Register any agent-specific tools via decorators
4. Add the agent to `AgentFactory`

Example:

```python
coding_agent = Agent(
    goals=[
        Goal(priority=1, name="coding", description="Write Python code")
    ],
    agent_language=AgentLanguage(),
    action_registry=ActionRegistry(tags=["file_operations", "coding"]),
    generate_response=llm,
    environment=Environment(),
)
```

No changes to the core loop required.

### Adding a New Tool

Define a plain Python function with a decorator:

```python
@register_tool(tags=["network", "api"])
def fetch_url(url: str) -> str:
    """Fetches content from a URL."""
    import requests
    return requests.get(url).text
```

The tool becomes available to any agent with the matching tags.

---

## Philosophy

This project is not about making agents *smarter*.

It is about making them:
- **safer**
- **predictable**
- **inspectable**
- **useful in real systems**

---

## License

MIT License

---

## Acknowledgements

Built as part of exploring **Agentic AI architectures**, structured tool-calling, and LLM orchestration patterns.
