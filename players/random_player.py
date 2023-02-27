from players import Player
import game_structure as gs

class RandomPlayer(Player):
    def __init__(self):
        """Player class implemented for Random players."""
        super().__init__()

# region Methods
    def think(self, observation: 'gs.Observation', budget: float) -> 'gs.Action':
        """Think about the next action to take."""
        return observation.get_random_action()
# endregion

# region Override
    def __str__(self):
        return "RandomPlayer"
# endregion
