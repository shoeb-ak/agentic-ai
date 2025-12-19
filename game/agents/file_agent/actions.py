from game.actions.registry import ActionRegistry
from game.actions.core.actions_registry import core_registry

registry = ActionRegistry()

registry.merge(core_registry)