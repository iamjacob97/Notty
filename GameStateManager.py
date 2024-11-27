class GameStateManager:
    def __init__(self):
        self.current_state = None
        self.shared_data = {}

    def change_state(self, new_state):
        self.current_state = new_state

    def get_shared_data(self):
        return self.shared_data