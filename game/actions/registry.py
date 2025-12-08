class ActionRegistry:
    def __init__(self):
        self.actions = {}

    def register(self, action):
        self.actions[action.name] = action

    def get_action(self, name):
        return self.actions.get(name)

    def get_actions(self):
        return list(self.actions.values())

