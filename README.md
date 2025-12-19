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

The framework integrates with **Groq's Llama 3.3 70B** for fast structured inference and supports **JSON-based function calling**, enabling reliable tool execution.

This project demonstrates:

- Agent architecture design  
- Function calling with real environment actions  
- Modular tool registry  
- Memory-driven context  
- Pluggable language model interface  
- Extensibility for multiple agent types  

---

## ⭐ Features

### 🔧 Modular GAME Components
- **Goals** define high-level tasks  
- **Actions** define what the agent can execute  
- **Memory** stores past interactions  
- **Environment** performs real-world execution  

### ⚙️ Pluggable LLM Backend
- Groq Llama 3.3 70B included  
- Easily switch to OpenAI, Anthropic, or local models (Ollama, LM Studio)  

### 🛠 Extensible Tool Registry
Add new tools by simply registering a new `Action`.

### 🔄 Full Agent Loop
Includes:
- Prompt construction  
- Tool-call generation  
- Action execution  
- Memory update  
- Loop termination logic  

---

## 📦 Project Structure

```
game_agent/
│
├── main.py                    # Entry point
│
└── game/
    ├── goals/                # G: Goals
    ├── actions/              # A: Actions + registry
    ├── memory/               # M: Memory
    ├── environment/          # E: Environment executor
    ├── language/             # Prompt + parser
    ├── core/                 # Agent loop
    └── llm/                  # Groq client
```

---

## 🔍 Architecture Diagram

```
                ┌─────────────────────────────────┐
                │              Goals               │
                └─────────────────────────────────┘
                               │
                               ▼
┌────────────┐     ┌───────────────────┐     ┌────────────┐
│  Actions   │◄────┤     Agent Loop    ├────►│ Environment │
└────────────┘     └───────────────────┘     └────────────┘
                               │
                               ▼
                ┌─────────────────────────────────┐
                │             Memory               │
                └─────────────────────────────────┘
                               │
                               ▼
                ┌─────────────────────────────────┐
                │         LLM (Groq API)          │
                └─────────────────────────────────┘
```

---

## 🧪 Example Usage  

When you run:

```
python main.py
```

Example interaction:

```
Task: read main.py

Agent Decision: {"tool": "read_file", "args": {"file_name": "main.py"}}
Action Result: {"tool_executed": true, "result": "...file contents...", "timestamp": "..."}
```

---

## 🚀 Getting Started

### 1️⃣ Install dependencies

```bash
pip install groq
```

---

### 2️⃣ Export your Groq API key

```bash
export GROQ_API_KEY="your_api_key_here"
```

---

### 3️⃣ Run the agent

```bash
python main.py
```

---

## 🛠 Extending the Framework

### Add a new tool (Action)

```python
def delete_file(name: str):
    os.remove(name)
    return f"{name} deleted."

registry.register(Action(
    name="delete_file",
    function=delete_file,
    description="Delete a file",
    parameters={
        "type": "object",
        "properties": {
            "name": {"type": "string"}
        },
        "required": ["name"]
    }
))
```

---

### Create a new agent

```python
coding_agent = Agent(
    goals=[Goal(priority=1, name="coding", description="Write Python code")],
    agent_language=AgentLanguage(),
    action_registry=CodeRegistry(),
    generate_response=GroqClient(),
    environment=DevEnvironment(),
)
```

---

## 🔮 Roadmap

- [ ] Add RAG support  
- [ ] Add DevOps tools (Kubernetes, Docker, GitHub APIs)  
- [ ] Build a coding agent with file-editing abilities  
- [ ] Add multi-agent coordination  
- [ ] Add Streamlit/FastAPI UI  
- [ ] Add LiteLLM routing + fallback models  
- [ ] Add JSON repair and retry logic  
- [ ] Add CI + unit tests  

---

## 🤝 Contributing

PRs welcome!  
You can contribute new tools, environments, or agents.

---

## 📄 License
MIT License

---

## 🙌 Acknowledgements

Built as part of my journey to learn and master **Agentic AI architectures**, structured tool-calling, and LLM orchestration patterns.
