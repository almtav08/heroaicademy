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
        other.player_0_cards = self.player_0_cards.clone()
        other.player_1_cards = self.player_1_cards.clone()
        other.player_0_units = self.player_0_units.clone()
        other.player_1_units = self.player_1_units.clone()

    def is_action_valid(self, action: 'gs.Action') -> bool:
        """Checks if the given action is currently valid."""
        units = self.player_0_units if self.current_turn == 0 else self.player_1_units
        enemy_units = self.player_1_units if self.current_turn == 0 else self.player_0_units
        cards = self.player_0_cards if self.current_turn == 0 else self.player_1_cards

        if action is None and (len(units.get_available_units()) > 0 or len(enemy_units.get_available_units()) > 0):
            return True
        if action.get_subject() is None:
            return False

        if type(action.get_subject()) is gs.Unit:
            unit = action.get_subject()
            if unit not in units.get_available_units():
                return False
            if action.get_unit() is None:
                # Unit is moving
                units_positions = units.get_unit_positions()
                units_positions.extend(enemy_units.get_unit_positions())
                return action.get_position() in unit.possible_moves(self.game_parameters.board_size, self.board[unit.get_pos()] == gs.TileType.SPEED, units_positions)
            else:
                # Unit is attacking or healing
                return action.get_unit() in units.get_units_in_range(unit) or action.get_unit() in enemy_units.get_units_in_range(unit)
        else:
            if action.get_subject() not in cards.get_cards():
                return False
            if action.get_unit() is None and action.get_position() is None:
                return True
            if action.get_unit() is not None and action.get_position() is not None:
                return False
            elif action.get_unit() is None:
                # Inferno spell or heal potion is used or unit is summoned
                if action.get_subject().get_value().is_spell_value():
                    enemy_units = self.player_1_units if self.current_turn == 0 else self.player_0_units
                    return action.get_position() in enemy_units.get_unit_positions()
                elif action.get_subject().get_value().is_item_value():
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
                return units.get_unit_in_position(action.get_unit().get_pos()) is not None

# endregion

# region Getters
    def get_actions(self) -> List['gs.Action']:
        """Get all the possible actions for the current player."""
        actions = []
        units = self.player_0_units if self.current_turn == 0 else self.player_1_units
        cards = self.player_0_cards if self.current_turn == 0 else self.player_1_cards
        enemy_units = self.player_1_units if self.current_turn == 0 else self.player_0_units
        units_positions = units.get_unit_positions()
        units_positions.extend(enemy_units.get_unit_positions())

        for unit in units.get_available_units():
            if unit.get_card().get_value() == gs.CardValue.CLERIC:
                for target in units.get_units_in_range(unit):
                    actions.append(gs.Action(unit.clone(), target.clone(), None))
            for enemy in enemy_units.get_units_in_range(unit):
                actions.append(gs.Action(unit.clone(), enemy.clone(), None))
            for position in unit.possible_moves(self.game_parameters.board_size, self.board[unit.get_pos()] == gs.TileType.SPEED, units_positions):
                actions.append(gs.Action(unit.clone(), None, deepcopy(position)))

        for card in cards.get_cards():
            if not card.is_playable(units, enemy_units):
                actions.append(gs.Action(card.clone(), None, None))
            elif card.get_value().is_spell_value():
                for enemy in enemy_units.get_units():
                    actions.append(gs.Action(card.clone(), None, deepcopy(enemy.get_pos())))
            elif card.get_value().is_item_value() and card.get_value() == gs.CardValue.HEAL_POTION:
                for unit in units.get_available_units():
                    actions.append(gs.Action(card.clone(), None, deepcopy(unit.get_pos())))
            elif card.get_value().is_item_value() and not card.get_value() == gs.CardValue.HEAL_POTION:
                for unit in units.get_available_units():
                    actions.append(gs.Action(card.clone(), unit.clone(), None))
            else:
                player_1 = True if self.current_turn == 1 else False
                spawns = units.get_avalible_positions_for_spawn(player_1, self.game_parameters.board_size, enemy_units.get_unit_positions())
                for position in spawns:
                    actions.append(gs.Action(card.clone(), None, deepcopy(position)))
        return actions
    
    def get_random_action(self) -> 'gs.Action':
        """Gets a random action that is currently valid."""
        units = self.player_0_units if self.current_turn == 0 else self.player_1_units
        cards = self.player_0_cards if self.current_turn == 0 else self.player_1_cards
        enemy_units = self.player_1_units if self.current_turn == 0 else self.player_0_units
        
        # Check possibilities for a unit to use it
        playable_units = units.get_playable_units(units, enemy_units, self.game_parameters.board_size, self.board)
        use_unit = len(playable_units) > 0
        use_card = len(cards.get_cards()) > 0

        if not use_unit and not use_card:
            return None
        
        if use_unit and use_card:
            use_unit = bool(random.getrandbits(1))

        if use_unit:
            # Play with a unit
            option = random.choice(playable_units)
            possible_actions = []
            if len(option[1]) > 0:
                possible_actions.append('move')
            if option[2]:
                possible_actions.append('attack')
            if option[3]:
                possible_actions.append('heal')

            action = random.choice(possible_actions)
            if action == 'move':
                return gs.Action(option[0].clone(), None, deepcopy(random.choice(option[1])))
            elif action == 'attack':
                return gs.Action(option[0].clone(), random.choice(enemy_units.get_units_in_range(option[0].clone())).clone(), None)
            else:
                return gs.Action(option[0].clone(), random.choice(units.get_units_in_range(option[0].clone())).clone(), None)
        else:
            # Play with a card
            avaliable_cards = cards.get_playable_cards(units, enemy_units)
            if len(avaliable_cards) == 0:
                return gs.Action(random.choice(cards.get_cards()).clone(), None, None)
            card = random.choice(avaliable_cards)
            
            if card.get_value().is_spell_value():
                return gs.Action(card.clone(), None, deepcopy(random.choice(enemy_units.get_units()).clone().get_pos()))
            elif card.get_value().is_item_value() and card.get_value() == gs.CardValue.HEAL_POTION:
                return gs.Action(card.clone(), None, deepcopy(random.choice(units.get_available_units()).clone().get_pos()))
            elif card.get_value().is_item_value() and not card.get_value() == gs.CardValue.HEAL_POTION:
                return gs.Action(card.clone(), random.choice(units.get_available_units()).clone(), None)
            else:
                player_1 = True if self.current_turn == 1 else False
                spawns = units.get_avalible_positions_for_spawn(player_1, self.game_parameters.board_size, enemy_units.get_unit_positions())
                return gs.Action(card.clone(), None, deepcopy(random.choice(spawns)))
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