import os

from game.core.agent import Agent
from game.goals.predefined_goals import file_management_goal
from game.language.agent_language import AgentLanguage
from game.actions.register_file_actions import registry
from game.environment.environment import Environment
from game.memory.memory import Memory
from game.llm.groq_client import GroqClient


def main():
    # Load Groq key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("Please set GROQ_API_KEY environment variable.")

    # Instantiate LLM backend
    groq_llm = GroqClient(api_key=api_key)

    # Create Agent
    agent = Agent(
        goals=[file_management_goal],
        agent_language=AgentLanguage(),
        action_registry=registry,
        generate_response=groq_llm,
        environment=Environment()
    )

    print("=== GAME Agent (Groq-Powered) ===")
    print("You can ask me to list, read, or search files.")
    print("Example: 'Read the file hello.txt'")
    print("----------------------------------")

    user_input = input("Task: ")

    memory = agent.run(user_input=user_input, memory=Memory(), max_iterations=10)

    print("\n=== FINAL MEMORY ===")
    for m in memory.items:
        print(m)


if __name__ == "__main__":
    main()

