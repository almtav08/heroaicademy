from typing import List, Tuple
from copy import deepcopy
import game_structure as gs
import random

class Observation:
    def __init__(self, game_state: 'gs.GameState', randomise_hidden_info: bool = False):
        if game_state is not None:
            self.game_parameters = game_state.game_parameters
            self.current_turn = game_state.current_turn
            self.action_points_left = game_state.action_points_left
            self.board = game_state.board.copy()
            self.player_0_score = game_state.player_0_score
            self.player_1_score = game_state.player_1_score
            self.player_0_deck = game_state.player_0_deck.clone()
            self.player_1_deck = game_state.player_1_deck.clone()
            self.player_0_discard = game_state.player_0_discard.clone()
            self.player_1_discard = game_state.player_1_discard.clone()
            self.player_0_cards = game_state.player_0_cards.clone()
            self.player_1_cards = game_state.player_1_cards.clone()
            self.player_0_units = game_state.player_0_units.clone()
            self.player_1_units = game_state.player_1_units.clone()
            self.randomise_hidden_info = randomise_hidden_info

# region Methods
    def clone(self) -> 'gs.Observation':
        """Clone the observation."""
        new_observation = Observation(None)
        new_observation.game_parameters = self.game_parameters
        new_observation.current_turn = self.current_turn
        new_observation.action_points_left = self.action_points_left
        new_observation.board = self.board.copy()
        new_observation.player_0_score = self.player_0_score
        new_observation.player_1_score = self.player_1_score
        new_observation.player_0_deck = self.player_0_deck.clone()
        new_observation.player_1_deck = self.player_1_deck.clone()
        new_observation.player_0_discard = self.player_0_discard.clone()
        new_observation.player_1_discard = self.player_1_discard.clone()
        new_observation.player_0_cards = self.player_0_cards.clone()
        new_observation.player_1_cards = self.player_1_cards.clone()
        new_observation.player_0_units = self.player_0_units.clone()
        new_observation.player_1_units = self.player_1_units.clone()
        return new_observation

    def copy_into(self, other: 'Observation') -> None:
        """Copy the observation into another one."""
        other.game_parameters = self.game_parameters
        other.current_turn = self.current_turn
        other.action_points_left = self.action_points_left
        other.board = self.board.copy()
        other.player_0_score = self.player_0_score
        other.player_1_score = self.player_1_score
        other.player_0_deck = self.player_0_deck.clone()
        other.player_1_deck = self.player_1_deck.clone()
        other.player_0_discard = self.player_0_discard.clone()
        other.player_1_discard = self.player_1_discard.clone()
        other.player_0_cards = self.player_0_cards.clone()
        other.player_1_cards = self.player_1_cards.clone()
        other.player_0_units = self.player_0_units.clone()
        other.player_1_units = self.player_1_units.clone()

    def is_action_valid(self, action: 'gs.Action') -> bool:
        """Checks if the given action is currently valid."""
        if type(action.get_subject()) is gs.Unit:
            units = self.player_0_units if self.current_turn == 0 else self.player_1_units
            if action.get_subject() not in units.get_available_units():
                return False
            if action.get_unit() is None:
                # Unit is moving
                enemy_units = self.player_1_units if self.current_turn == 0 else self.player_0_units
                return action.get_position() in action.get_subject().possible_moves(self.game_parameters.board_size) \
                    and action.get_position() not in enemy_units.get_unit_positions()
            else:
                # Unit is attacking or healing
                units = self.player_0_units if self.current_turn == 0 else self.player_1_units
                return action.get_unit() in units.get_units_in_range(action.get_subject())
        else:
            cards = self.player_0_cards if self.current_turn == 0 else self.player_1_cards
            if action.get_subject() not in cards.get_cards():
                return False
            if action.get_unit() is None:
                # Inferno spell or heal potion is used or unit is summoned
                if action.get_subject().get_value() == gs.CardValue.INFERNO:
                    enemy_units = self.player_1_units if self.current_turn == 0 else self.player_0_units
                    return action.get_position() in enemy_units.get_unit_positions()
                elif action.get_subject().get_value() == gs.CardValue.HEAL_POTION:
                    units = self.player_0_units if self.current_turn == 0 else self.player_1_units
                    return action.get_position() in units.get_unit_positions()
                else:
                    units = self.player_0_units if self.current_turn == 0 else self.player_1_units
                    enemy_units = self.player_1_units if self.current_turn == 0 else self.player_0_units
                    player_1 = True if self.current_turn == 1 else False
                    return action.get_position() in units.get_avalible_positions_for_spawn(player_1, self.game_parameters.board_size) \
                        and action.get_position() not in enemy_units.get_unit_positions()
            else:
                # Equipment given to unit
                units = self.player_0_units if self.current_turn == 0 else self.player_1_units
                return action.get_unit().get_pos() in units.get_unit_positions()

# endregion

# region Getters
    def get_actions(self) -> List['gs.Action']:
        """Get all the possible actions for the current player."""
        actions = []
        units = self.player_0_units if self.current_turn == 0 else self.player_1_units
        cards = self.player_0_cards if self.current_turn == 0 else self.player_1_cards
        enemy_units = self.player_1_units if self.current_turn == 0 else self.player_0_units

        for unit in units.get_available_units():
            if unit.get_card().get_value() == gs.CardValue.CLERIC:
                for target in units.get_units_in_range(unit):
                    actions.append(gs.Action(unit.clone(), target.clone(), None))
                for position in unit.possible_moves(self.game_parameters.board_size):
                    actions.append(gs.Action(unit.clone(), None, deepcopy(position)))
                    if position not in enemy_units.get_unit_positions():
                        actions.append(gs.Action(unit.clone(), None, deepcopy(position)))
            else:
                for enemy in enemy_units.get_units_in_range(unit):
                    actions.append(gs.Action(unit.clone(), enemy.clone(), None))
                for position in unit.possible_moves(self.game_parameters.board_size):
                    if position not in enemy_units.get_unit_positions():
                        actions.append(gs.Action(unit.clone(), None, deepcopy(position)))

        for card in cards.get_cards():
            actions.append(gs.Action(card.clone(), None, None))
            if card.get_value() == gs.CardValue.INFERNO:
                for enemy in enemy_units.get_units():
                    actions.append(gs.Action(card.clone(), None, deepcopy(enemy.get_pos())))
            elif card.get_value() == gs.CardValue.HEAL_POTION:
                for unit in units.get_available_units():
                    actions.append(gs.Action(card.clone(), None, deepcopy(unit.get_pos())))
            elif card.get_value().is_unit_value():
                player_1 = True if self.current_turn == 1 else False
                for position in units.get_avalible_positions_for_spawn(player_1, self.game_parameters.board_size):
                    if position not in enemy_units.get_unit_positions():
                        actions.append(gs.Action(card.clone(), None, deepcopy(position)))
            else:
                for unit in units.get_available_units():
                    actions.append(gs.Action(card.clone(), unit.clone(), None))
        
        return actions

    def get_random_action(self) -> 'gs.Action':
        """Gets a random action that is currently valid."""
        units = self.player_0_units if self.current_turn == 0 else self.player_1_units
        cards = self.player_0_cards if self.current_turn == 0 else self.player_1_cards
        move = bool(random.getrandbits(1)) and len(units.get_available_units()) > 0
        if not move:
            # Play with a card
            card = random.choice(cards.get_cards())

            discard = bool(random.getrandbits(1))
            if discard:
                return gs.Action(card.clone(), None, None)
            
            if card.get_value() == gs.CardValue.INFERNO:
                enemy_units = self.player_1_units if self.current_turn == 0 else self.player_0_units
                enemy = random.choice(enemy_units.get_units())
                return gs.Action(card.clone(), None, deepcopy(enemy.get_pos()))
            elif card.get_value() == gs.CardValue.HEAL_POTION:
                units = self.player_0_units if self.current_turn == 0 else self.player_1_units
                unit = random.choice(units.get_units())
                return gs.Action(card.clone(), None, deepcopy(unit.get_pos()))
            elif card.get_value().is_unit_value():
                units = self.player_0_units if self.current_turn == 0 else self.player_1_units
                player_1 = True if self.current_turn == 1 else False
                spawns = units.get_avalible_positions_for_spawn(player_1, self.game_parameters.board_size)
                position = random.choice(spawns)
                enemy_units = self.player_1_units if self.current_turn == 0 else self.player_0_units
                while position in enemy_units.get_unit_positions():
                    position = random.choice(spawns)
                return gs.Action(card.clone(), None, deepcopy(position))
            else:
                units = self.player_0_units if self.current_turn == 0 else self.player_1_units
                unit = random.choice(units.get_units())
                return gs.Action(card.clone(), unit.clone(), None)
        else:
            # Play with a unit
            unit = random.choice(units.get_available_units())
            if unit.get_card().get_value() == gs.CardValue.CLERIC:
                move = bool(random.getrandbits(1))
                if not move:
                    # No move, heal
                    units = self.player_0_units if self.current_turn == 0 else self.player_1_units
                    target = random.choice(units.get_units_in_range(unit))
                    return gs.Action(unit.clone(), target.clone(), None)
                else:
                # Move
                    moves = unit.possible_moves(self.game_parameters.board_size)
                    position = random.choice(moves)
                    enemy_units = self.player_1_units if self.current_turn == 0 else self.player_0_units
                    while position in enemy_units.get_unit_positions():
                        position = random.choice(moves)
                    return gs.Action(unit.clone(), None, deepcopy(position))
            else:
                move = bool(random.getrandbits(1))
                enemy_units = self.player_1_units if self.current_turn == 0 else self.player_0_units
                enemies_in_range = enemy_units.get_units_in_range(unit)
                if not move and len(enemies_in_range) > 0:
                    # No move, attack
                    target = random.choice(enemies_in_range)
                    return gs.Action(unit.clone(), target.clone(), None)
                else:
                # Move
                    moves = unit.possible_moves(self.game_parameters.board_size)
                    position = random.choice(moves)
                    enemy_units = self.player_1_units if self.current_turn == 0 else self.player_0_units
                    while position in enemy_units.get_unit_positions():
                        position = random.choice(moves)
                    return gs.Action(unit.clone(), None, deepcopy(position))
# endregion

#region Override
    def __str__(self):
        return (f"TURN: {self.current_turn!s}\n"
                f"SCORE P1: {self.player_0_score!s}\n"
                f"CARDS P1: {self.player_0_cards!s}\n"
                f"SCORE P2: {self.player_1_score!s}\n"
                f"SCORE P2: {self.player_1_cards!s}\n"
                f"ACTION POINTS LEFT: {self.action_points_left!s}")
#endregion