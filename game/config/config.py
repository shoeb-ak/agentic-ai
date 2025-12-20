from dataclasses import dataclass
from typing import Optional
import os

"""
Free tier models to use (sorted by best to worst for tool calling):
1. llama-3.3-70b-versatile
2. meta-llama/llama-4-scout-17b-16e-instruct
3. llama-3.1-8b-instant
4. qwen/qwen3-32b
5. meta-llama/llama-4-maverick-17b-128e-instruct
"""

# ------------------------
# Provider-specific config
# ------------------------

@dataclass(frozen=True)
class PortkeyConfig:
    api_key: str = os.getenv("PORTKEY_API_KEY", "")
    virtual_key: str = os.getenv("PORTKEY_VIRTUAL_KEY", "")


@dataclass(frozen=True)
class GroqConfig:
    api_key: str = os.getenv("GROQ_API_KEY", "")


# ------------------------
# LLM-level config
# ------------------------

@dataclass(frozen=True)
class LLMConfig:
    # Provider selection
    provider: str = "portkey"   # "groq" | "portkey"

    # Model selection strategy
    prefer_best_tool_model: bool = True
    pinned_model: Optional[str] = None

    # Generation params
    temperature: float = 0.0
    max_tokens: int = 1024


# ------------------------
# Agent-level config
# ------------------------

@dataclass(frozen=True)
class AgentConfig:
    max_iterations: int = 10
    verbose: bool = True


# ------------------------
# Root config
# ------------------------

@dataclass(frozen=True)
class Config:
    llm: LLMConfig = LLMConfig()
    agent: AgentConfig = AgentConfig()

    # Providers
    portkey: PortkeyConfig = PortkeyConfig()
    groq: GroqConfig = GroqConfig()


# ------------------------
# SINGLE GLOBAL INSTANCE
# ------------------------

CONFIG = Config()
