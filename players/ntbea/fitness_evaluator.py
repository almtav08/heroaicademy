from game_structure import Action, Unit, UnitType, Observation
from typing import List

class FitnessEvaluator:
    def __init__(self, heuristic):
        """Class used to calculate the fitness of a turn decided by NTBEA. It needs to translate between an Action list and the ints the Bandit1D and Bandit2D use."""
        self.heuristic = heuristic

# region Methods
    def evaluate(self, parameters: list[int], observation: "Observation") -> float:
        """Calculates the fitness of a turn given by NTBEA as a parameter list, playing it from the given Observation."""
        turn = self.ntbea_to_turn(parameters)
        for action in turn:
            observation.game_parameters.forward_model.step(observation, action)
        return self.heuristic.get_reward(observation)

    def ntbea_to_turn(self, ntbea_parameters: list[int]) -> "List[Action]":
        """Converts a list of int parameters from NTBEA to a list of Action representing a turn."""
        turn = []
        for parameter in ntbea_parameters:
            turn.append(self.get_action_from_parameter(parameter))
        return turn

    def get_action_from_parameter(self, parameter: int) -> "Action":
        """Converts an int parameter from NTBEA to an `ASMACAG.Game.Action.Action`."""
        #if parameter < 2:
        #    return Action(Card(CardType(parameter+2)))
        #elif parameter < 8:
        #    return Action(Card(CardType.NUMBER, 1), Card(CardType.NUMBER, parameter - 1))
        #elif parameter < 14:
        #    return Action(Card(CardType.NUMBER, 2), Card(CardType.NUMBER, parameter - 7))
        #elif parameter < 20:
        #    return Action(Card(CardType.NUMBER, 3), Card(CardType.NUMBER, parameter - 13))
        #elif parameter < 26:
        #    return Action(Card(CardType.NUMBER, 4), Card(CardType.NUMBER, parameter - 19))
        #elif parameter < 32:
        #    return Action(Card(CardType.NUMBER, 5), Card(CardType.NUMBER, parameter - 25))
        #elif parameter < 38:
        #    return Action(Card(CardType.NUMBER, 6), Card(CardType.NUMBER, parameter - 31))

    def get_parameter_from_action(self, action: "Action") -> int:
        """Converts an Action to an int parameter for NTBEA."""
        #if action.get_played_card().get_type() == CardType.DIV2 \
        #        or action.get_played_card().get_type() == CardType.MULT2:
        #    return action.get_played_card().get_type().value - 2
        #elif action.get_played_card().get_type() == CardType.NUMBER:
        #    return (action.get_played_card().get_number() - 1) * 6 + action.get_board_card().get_number() + 1
# endregion
