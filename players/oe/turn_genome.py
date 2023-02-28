from typing import List
import game_structure as gs
import random

class TurnGenome:
    def __init__(self):
        self.actions = []
        self.reward = 0

# region Methods
    def random(self, observation: "gs.Observation"):
        """Fills up this genome with random valid actions"""
        self.actions.clear()
        self.reward = 0
        while not observation.game_parameters.forward_model.is_terminal(observation) and not observation.game_parameters.forward_model.is_turn_finished(observation):
            action = observation.get_random_action()
            self.actions.append(action)
            observation.game_parameters.forward_model.step(observation, action)

    def crossover(self, parent_a: "TurnGenome", parent_b: "TurnGenome", observation: "gs.Observation"):
        """Fills up this genome with a crossover of the two parents"""
        self.reward = 0
        actions_count = min(observation.game_parameters.action_points_per_turn, len(self.actions))
        for i in range(actions_count):
            # choose a random parent and add action at index if valid, otherwise use the other parent
            added = False
            if bool(random.getrandbits(1)):
                if observation.is_action_valid(parent_a.actions[i]):
                    parent_a.actions[i].copy_into(self.actions[i])
                    added = True
                elif observation.is_action_valid(parent_b.actions[i]):
                    parent_b.actions[i].copy_into(self.actions[i])
                    added = True
            else:
                if observation.is_action_valid(parent_b.actions[i]):
                    parent_b.actions[i].copy_into(self.actions[i])
                    added = True
                elif observation.is_action_valid(parent_a.actions[i]):
                    parent_a.actions[i].copy_into(self.actions[i])
                    added = True

            # if no action was added, add a random one
            if not added:
                self.actions[i] = observation.get_random_action()

            observation.game_parameters.forward_model.step(observation, self.actions[i])

    def mutate_at_random_index(self, observation: "gs.Observation") -> None:
        """Mutates this genome at a random action of the turn while keeping the whole turn valid. Note that the gs.observation state is not preserved."""
        mutation_index = random.randrange(len(self.actions))
        for i in range(len(self.actions)):
            if i == mutation_index:
                self.actions[i] = observation.get_random_action()
            elif i > mutation_index:
                if not observation.is_action_valid(self.actions[i]):
                    self.actions[i] = observation.get_random_action()

            observation.game_parameters.forward_model.step(observation, self.actions[i])

    def clone(self) -> "TurnGenome":
        """Returns a clone of this genome"""
        clone = TurnGenome()
        clone.set_reward(self.get_reward())
        for action in self.get_actions():
            clone.actions.append(action.clone())
        return clone

    def copy_into(self, other: "TurnGenome") -> None:
        """Copies this genome into another one."""
        other.set_reward(self.get_reward())
        for i in range(len(self.get_actions())):
            if i < len(other.get_actions()):
                self.get_actions()[i].copy_into(other.get_actions()[i])
            else:
                other.get_actions().append(self.get_actions()[i].clone())
# endregion

# region Getters
    def get_actions(self) -> List["gs.Action"]:
        """Returns the list of actions of this genome."""
        return self.actions

    def get_reward(self) -> float:
        """Returns the reward of this genome."""
        return self.reward

    def set_reward(self, reward: float) -> None:
        """Sets the reward of this genome."""
        self.reward = reward
# endregion

# region Override
    def __str__(self):
        return f"TurnGenome [actions={self.actions}, reward={self.reward}]"
# endregion