import json
from typing import List, Callable

from game.goals.goal import Goal
from game.actions.registry import ActionRegistry
from game.language.agent_language import AgentLanguage
from game.environment.environment import Environment
from game.memory.memory import Memory
from game.language.prompt import Prompt
from game.llm.llm_factory import LLMFactory


class Agent:
    def __init__(self,
                 goals: List[Goal],
                 agent_language: AgentLanguage,
                 action_registry: ActionRegistry,
                 generate_response: Callable[[Prompt], str],
                 environment: Environment):
        """
        Initialize an agent with its core GAME components
        """
        self.goals = goals
        self.generate_response = generate_response
        self.agent_language = agent_language
        self.actions = action_registry
        self.environment = environment

    def construct_prompt(self, goals: List[Goal], memory: Memory, actions: ActionRegistry) -> Prompt:
        """Build prompt with memory context."""
        return self.agent_language.construct_prompt(
            actions=actions.get_openai_schema(),
            environment=self.environment,
            goals=goals,
            memory=memory
        )

    def get_action(self, response: str):
        """Parse response → determine which tool and arguments to execute."""
        invocation = self.agent_language.parse_response(response)
        tool = self.actions.get_tool(invocation["tool"])
        return tool, invocation

    def should_terminate(self, response: str) -> bool:
        action_def, _ = self.get_action(response)
        return action_def["terminal"]

    def set_current_task(self, memory: Memory, task: str):
        memory.add_memory({"role": "user", "content": task})

    def update_memory(self, memory: Memory, response: str, result: dict):
        """Update memory with the agent's decision and the environment's response."""
        new_memories = [
            {"role": "assistant", "content": response},
            {"role": "user", "content": json.dumps(result)}
        ]
        for m in new_memories:
            memory.add_memory(m)

    def prompt_llm_for_action(self, full_prompt: Prompt) -> str:
        """Call the LLM and return its raw response."""
        response = self.generate_response(full_prompt)
        return response

    def run(self, user_input: str, memory=None, max_iterations: int = 50) -> Memory:
        """
        Execute the GAME loop for this agent with a maximum iteration limit.
        """
        memory = memory or Memory()
        self.set_current_task(memory, user_input)

        for step in range(max_iterations):

            # 1. Build GAME prompt
            prompt = self.construct_prompt(self.goals, memory, self.actions)

            print("\nAgent thinking...")
            response = self.prompt_llm_for_action(prompt)
            print(f"Agent Decision: {response}")

            # 2. Identify intended action
            tool, invocation = self.get_action(response)

            # Prevent premature termination
            if tool["tool_name"] == "terminate" and step == 0:
                memory.add_memory({
                    "role": "system",
                    "content": "Termination is not allowed as the first action. Execute the required tool instead."
                })
                continue

            # 3. Execute the action
            result = self.environment.execute_action(
                tool["function"],
                invocation["args"]
            )

            print(f"Action Result: {result}")

            # 4. Update memory
            self.update_memory(memory, response, result)

            # 5. Terminate?
            if self.should_terminate(response):
                print("Agent requested termination.")
                break

        return memory

