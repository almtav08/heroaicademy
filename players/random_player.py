from players import Player
from game_structure import Observation, Action

class RandomPlayer(Player):
    def __init__(self):
        """Player class implemented for Random players."""
        super().__init__()

# region Methods
    def think(self, observation: 'Observation', budget: float) -> 'Action':
        """Think about the next action to take."""
        return observation.get_random_action()
# endregion

# region Override
    def __str__(self):
        return "RandomPlayer"
# endregion
