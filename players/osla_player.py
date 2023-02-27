from heuristics import Heuristic
from players import Player
from game_structure import Observation, Action
import math

class OSLAPlayer(Player):
    def __init__(self, heuristic: 'Heuristic'):
        """Player class implemented for OSLA players."""
        self.heuristic = heuristic

# region Methods
    def think(self, observation: 'Observation', budget: float) -> 'Action':
        """Think about the next action to take."""
        best_reward = -math.inf
        best_action = None
        current_observation = observation.clone()
        actions = observation.get_actions()
        for action in actions:
            observation.copy_into(current_observation)
            observation.game_parameters.forward_model.step(current_observation, action)
            reward = self.heuristic.get_reward(current_observation)
            if reward >= best_reward:
                best_action = action
                best_reward = reward
        print(f"Best action: {best_action}")
        return best_action
# endregion

# region Override
    def __str__(self):
        return "OSLAPlayer"
# endregion
