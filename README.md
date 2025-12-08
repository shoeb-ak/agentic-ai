🧠 GAME Agent Framework
A Modular, Extensible Agentic AI System Built on the GAME Architecture (Goals · Actions · Memory · Environment)

<!-- replace with your own -->

🚀 Overview

This repository implements a fully modular Agentic AI framework based on the G.A.M.E. architecture:

G → Goals  
A → Actions  
M → Memory  
E → Environment  


The framework integrates with Groq's Llama 3.3 70B for fast structured inference and supports JSON-based function calling, enabling reliable tool execution.

This project demonstrates:

Agent architecture design

Function calling with real environment actions

Modular tool registry

Memory-driven context

Pluggable language model interface

Clear abstractions for extensibility

It is an excellent foundation for DevOps agents, coding agents, file-processing agents, research agents, and multi-agent systems.

⭐ Features
🔧 Modular GAME Components

Goals: Define the high-level objectives of the agent

Actions: Tooling and capabilities accessible to the agent

Memory: Persistent contextual history

Environment: Safe execution of tools

⚙️ Pluggable LLM Backend

Currently includes:

Groq Llama 3.3 70B — ultra-fast inference
Easily extendable to:

OpenAI

Anthropic

Local models (Ollama / LM Studio)

LiteLLM routing

🛠 Extensible Tool Registry

Add new agent skills simply by registering a new Action.

🔄 Full Agent Loop

Implements:

Prompt construction

Tool selection

Environment execution

Memory updating

Iterative reasoning

🎯 Strict JSON Tool Calling

The agent always returns:

{
  "tool": "read_file",
  "args": { "file_name": "main.py" }
}


No hallucinated formats.

📦 Project Structure
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

🔍 Architecture Diagram
                ┌─────────────────────────────────┐
                │              Goals               │
                └─────────────────────────────────┘
                               │
                               ▼
┌────────────┐     ┌───────────────────┐     ┌────────────┐
│  Actions   │◄────┤     Agent Loop    ├────►│  Environment│
└────────────┘     └───────────────────┘     └────────────┘
                               │
                               ▼
                ┌─────────────────────────────────┐
                │             Memory               │
                └─────────────────────────────────┘
                               │
                               ▼
                ┌─────────────────────────────────┐
                │            LLM (Groq)           │
                └─────────────────────────────────┘

🧪 Example Use Case
Ask the agent to read or analyze files in the current directory:
=== GAME Agent (Groq-Powered) ===
You can ask me to list, read, or search files.
Example: "Read hello.txt"


Example interaction:

Task: search in file main.py for "class"
Agent Decision: {"tool": "search_in_file", "args": {"file_name": "main.py", "search_term": "class"}}
Action Result: {"tool_executed": true, "result": [...], "timestamp": "..."}

🚀 Getting Started
1️⃣ Install dependencies
pip install groq

2️⃣ Set your Groq API key
export GROQ_API_KEY="your_key_here"

3️⃣ Run the agent
python main.py

🧩 How the GAME Loop Works
1. Construct Prompt

Goals

Memory

Registered Actions

Environment info

2. LLM Decides Action

The model returns structured JSON specifying which tool to call.

3. Execute Action

Environment safely executes the tool.

4. Update Memory

Both decision + result stored.

5. Repeat

Until termination or max iterations reached.

🛠 Extending the Framework
Add New Actions
def delete_file(name: str):
    os.remove(name)
    return f"{name} deleted."

registry.register(Action(
    name="delete_file",
    function=delete_file,
    description="Delete a file",
    parameters={
        "type": "object",
        "properties": {"name": {"type": "string"}},
        "required": ["name"]
    }
))

Add New Agents

Swap Goals + Actions + Environment.

🔮 Roadmap

 Add RAG support

 Add DevOps tools (Kubernetes, GitHub, Docker)

 Build coding agent with file-editing

 Add multi-agent coordination

 Add Streamlit or FastAPI UI

 Add unit tests and CI

 Add LiteLLM fallback provider

🤝 Contributing

PRs welcome!
Feel free to propose new tools, agents, or environments.

📄 License

MIT License

🙌 Acknowledgements

This project was built as part of learning Agentic AI systems, focusing on modular architectures and real-world function execution using LLMs.
