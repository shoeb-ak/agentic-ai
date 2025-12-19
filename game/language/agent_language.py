import json
from typing import List

from game.language.prompt import Prompt
from game.language.function_call_parser import FunctionCallParser


class AgentLanguage:
    """
    Responsible for:
    - Building a structured prompt from Goals, Actions, Memory, Environment
    - Parsing LLM responses to extract function calls
    """

    def __init__(self):
        pass

    # ------------------------------------------------------------------
    # PROMPT CONSTRUCTION LOGIC
    # ------------------------------------------------------------------
    def construct_prompt(self, actions, environment, goals, memory) -> Prompt:
        """
        Build the full prompt delivered to the LLM.
        """
        system_message = self.build_system_message(goals, environment)
        memory_messages = memory.get_memories(limit=None)

        tools_schema = self.build_tools_schema(actions)
        
        return Prompt(
            system=system_message,
            messages=memory_messages,
            tools=tools_schema
        )

    def build_system_message(self, goals, environment) -> str:
        goals_text = "\n".join(f"- {g.description}" for g in goals)

        return f"""
You are an autonomous agent. 
YOU MUST ALWAYS return a JSON OBJECT containing exactly two fields:

1. "tool": the name of the tool to call (string)
2. "args": the argument object for that tool (dictionary)

VALID FORMAT (MANDATORY):
{{
"tool": "<tool_name>",
"args": {{
    "param1": "...",
    "param2": "..."
}}
}}

Rules:
- NEVER return anything except this JSON.
- NEVER respond in natural language.
- NEVER respond with plain text.
- NEVER invent tools.
- NEVER skip tool invocation.
- NEVER use XML, angle brackets, markdown, or natural language.
- NEVER wrap JSON in code blocks.
- NEVER hallucinate unknown tools.
- ONLY use tools provided in the tool list.
- If you want to give an explanation: DO NOT. Tool call JSON ONLY.

IMPORTANT TOOL USE RULES:
- You MUST return ONLY ONE tool call per message.
- Never return an array of tool calls.
- Never attempt multiple actions in the same step.
- If you need to perform multiple actions, do them one by one, in separate messages.
- After executing one action, wait for the environment’s response BEFORE deciding the next tool.
- Use `terminate` ONLY when the task is fully complete.

Your goals:
{goals_text}

Environment: {environment.__class__.__name__}
"""


    # ------------------------------------------------------------------
    # TOOL SCHEMA FOR FUNCTION CALLING
    # ------------------------------------------------------------------
    def build_tools_schema(self, actions) -> List[dict]:
        """
        Build the OpenAI/Groq-style tool schema.
        """
        tool_list = []

        for action in actions:
            tool_list.append({
                "type": "function",
                "function": {
                    "name": action.name,
                    "description": action.description,
                    "parameters": action.parameters
                }
            })

        return tool_list

    # ------------------------------------------------------------------
    # RESPONSE PARSING
    # ------------------------------------------------------------------
    def parse_response(self, response):
        """
        Parse an LLM response into a tool invocation.
        Supports both:
        - dict (Groq-native tool calls)
        - JSON string (fallback / non-tool models)
        """
        if isinstance(response, dict):
            return response

        if isinstance(response, str):
            return FunctionCallParser.parse(response)

        raise TypeError(f"Unsupported response type: {type(response)}")

