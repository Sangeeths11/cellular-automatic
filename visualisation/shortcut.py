class Shortcut:
    def __init__(self, name: str, key: int, modifiers: int, action, toggable: bool = False, initial_state: bool = True):
        self.name = name
        self.key = key
        self.modifiers = modifiers
        self.action = action
        self.code = Shortcut.calculate_code(key, modifiers)
        self._is_toggle = toggable
        self._state = initial_state

    @staticmethod
    def calculate_code(key: int, modifiers: int):
        return (modifiers & 0xFF) | (key << 8)

    def get_code(self):
        return self.code

    def execute(self):
        if self._is_toggle:
            self._state = not self._state
            self.action(self._state)
        else:
            self.action()

    def is_toggle(self):
        return self._is_toggle

    def get_state(self):
        return self._state

    def get_action(self):
        return self.action

    def set_action(self, action):
        self.action = action

    def get_text(self):
        return self.name