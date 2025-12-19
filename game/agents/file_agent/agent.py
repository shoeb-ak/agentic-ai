from game.core.agent import Agent
from game.language.agent_language import AgentLanguage
from game.memory.memory import Memory
from game.environment.environment import Environment
from game.llm.llm_factory import LLMFactory
from game.config.config import CONFIG

from .goals import file_management_goals
from .actions import registry

def create_agent():
    llm = LLMFactory.create()

    return Agent(
        goals=file_management_goals,
        agent_language=AgentLanguage(),
        action_registry=registry,
        environment=Environment(),
        generate_response=llm
    )
