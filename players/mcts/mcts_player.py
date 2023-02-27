"""Entity that plays a game by using the Monte Carlo Tree Search algorithm to choose all actions in a turn."""
from players.mcts.mcts_node import MCTSNode
from players import Player
from heuristics import Heuristic
import time
import game_structure as gs

class MCTSPlayer(Player):
    """Entity that plays a game by using the Monte Carlo Tree Search algorithm to choose all actions in a turn."""
    def __init__(self, heuristic: "Heuristic", c_value: float):
        self.heuristic = heuristic
        self.c_value = c_value
        self.turn = []
        super().__init__()

# region Methods
    def think(self, observation: "gs.Observation", budget: float) -> "gs.Action":
        """Computes a list of actions for a complete turn using the Monte Carlo Tree Search algorithm and returns them in order each time it's called during the turn."""
        if observation.action_points_left == observation.game_parameters.action_points_per_turn:
            self.turn.clear()
            self.compute_turn(observation, budget)
        return self.turn.pop(0)

    def compute_turn(self, observation: "gs.Observation", budget: float) -> None:
        """Computes a list of action for a complete turn using the Monte Carlo Tree Search algorithm and sets it as the turn."""
        t0 = time.time()
        root = MCTSNode(observation, self.heuristic, None)
        root.extend()
        current_node = root

        while time.time() - t0 < budget - 0.12:
            best_child = current_node.get_best_child_by_ucb(self.c_value)
            if best_child.get_amount_of_children() > 0:
                current_node = best_child
            else:
                if not best_child.get_is_unvisited() and not best_child.get_is_terminal():
                    best_child.extend()
                    best_child = best_child.get_random_child()
                best_child.backpropagate(best_child.rollout())
                current_node = root

        # retrieve the turn
        current_node = root
        for i in range(observation.game_parameters.action_points_per_turn):
            best_child = current_node.get_best_child_by_average()
            if best_child is None:
                self.turn.append(None)
                continue
            self.turn.append(best_child.get_action() if best_child is not None else None)
            current_node = best_child
# endregion

# region Override
    def __str__(self):
        return f"MCTSPlayer[{self.c_value}]"
# endregion