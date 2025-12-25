from game.core.agent import Agent
from game.language.agent_language import AgentLanguage
from game.memory.memory import Memory
from game.environment.environment import Environment
from game.llm.llm_factory import LLMFactory
from game.config.config import CONFIG

from game.actions.registry import ActionRegistry
import game.actions  
from . import actions 

from .goals import file_management_goals

def create_agent():
    llm = LLMFactory.create()
    action_registry = ActionRegistry(tags=["file_operations","system"])

    return Agent(
        goals=file_management_goals,
        agent_language=AgentLanguage(),
        action_registry=action_registry,
        environment=Environment(),
        generate_response=llm
    )
