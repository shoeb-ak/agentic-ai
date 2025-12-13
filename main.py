from game.agents.agent_factory import AgentFactory
from game.memory.memory import Memory


def main():
    print("Available agents: file | readme")
    agent_type = input("Select agent: ").strip()

    agent = AgentFactory.create(agent_type)
    memory = Memory()

    task = input("Task: ")
    agent.run(task, memory)


if __name__ == "__main__":
    main()
