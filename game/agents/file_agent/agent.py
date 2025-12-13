from game.core.agent import Agent
from game.language.agent_language import AgentLanguage
from game.memory.memory import Memory
from game.environment.environment import Environment
from game.llm.groq_client import GroqClient
from game.config.config import CONFIG

from .goals import file_management_goals
from .actions import registry

def create_agent():
    llm = GroqClient(
        model=CONFIG.llm.model,
        temperature=CONFIG.llm.temperature,
        max_tokens=CONFIG.llm.max_tokens
    )

    return Agent(
        goals=file_management_goals,
        agent_language=AgentLanguage(),
        action_registry=registry,
        environment=Environment(),
        generate_response=llm
    )