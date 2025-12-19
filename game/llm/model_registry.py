from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class ModelSpec:
    name: str
    provider: str
    max_tokens: int
    cost_tier: str           # free / paid

MODEL_REGISTRY: List[ModelSpec] = [
    ModelSpec("llama-3.3-70b-versatile", "groq", 8192, "free"),
    ModelSpec("meta-llama/llama-4-scout-17b-16e-instruct", "groq", 8192, "free"),
    ModelSpec("llama-3.1-8b-instant", "groq", 4096, "free"),
    ModelSpec("qwen/qwen3-32b", "groq", 8192, "free"),
    ModelSpec("meta-llama/llama-4-maverick-17b-128e-instruct", "groq", 8192, "free"),
]