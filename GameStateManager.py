class GameStateManager:
    def __init__(self):
        self.current_state = None
        self.shared_data = {} #dictionary that holds data that will be shared in different sections of the game

    def change_state(self, new_state):
        self.current_state = new_state #changes the current game state to the new state

    def get_shared_data(self):
        return self.shared_data #returns the shared dictionary data