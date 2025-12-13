from dataclasses import dataclass

'''
Free tier models to use (sorted by best to worst for tool calling):
    1. llama-3.3-70b-versatile
    2. meta-llama/llama-4-scout-17b-16e-instruct
    3. llama-3.1-8b-instant
    4. qwen/qwen3-32b
    5. meta-llama/llama-4-maverick-17b-128e-instruct
'''

@dataclass(frozen=True)
class LLMConfig:
    provider: str = "groq"
    model: str = "meta-llama/llama-4-scout-17b-16e-instruct"
    temperature: float = 0.0
    max_tokens: int = 1024


@dataclass(frozen=True)
class AgentConfig:
    max_iterations: int = 10
    verbose: bool = True


@dataclass(frozen=True)
class Config:
    llm: LLMConfig = LLMConfig()
    agent: AgentConfig = AgentConfig()


# SINGLE GLOBAL INSTANCE (import this everywhere)
CONFIG = Config()
