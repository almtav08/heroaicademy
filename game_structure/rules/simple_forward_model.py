from typing import Union, Tuple
from copy import deepcopy
from game_structure.rules import ForwardModel
from game_structure import GameState, Observation, Action, Card, CardValue, Unit
from util.create_unit import create

class SimpleForwardModel(ForwardModel):
    def __init__(self):
        super().__init__()

# region Methods
    def step(self, game_state: Union['GameState', 'Observation'], action: 'Action') -> bool:
        """Perform an action on the game state."""
        if action is None:
            return False
        
        cards = game_state.player_0_cards if game_state.current_turn == 0 else game_state.player_1_cards
        units = game_state.player_0_units if game_state.current_turn == 0 else game_state.player_1_units
        enemy_units = game_state.player_1_units if game_state.current_turn == 0 else game_state.player_0_units
        discard = game_state.player_0_discard if game_state.current_turn == 0 else game_state.player_1_discard

        if type(action.get_subject()) is Card:
            card = action.get_subject()

            if card.get_value() == CardValue.INFERNO:
                target = enemy_units.get_unit_in_position(action.get_position())
                if target is None:
                    return False
                target.set_hp(target.get_hp() - 200)
            elif card.get_value() == CardValue.HEAL_POTION:
                target = units.get_unit_in_position(action.get_position())
                if target is None:
                    return False
                target.set_hp(target.get_hp() + 100)
            elif card.get_value().is_unit_value():
                units.add_unit(create(card, action.get_position()))
            else:
                units.get_unit_in_position(action.get_unit().get_pos()).get_equipement().append(card)
            
            cards.remove_card(card)
            discard.add_card(card)
            self.update_score(game_state)
            return True
        else:
            unit = action.get_subject()
            if action.get_position() is None:
                if unit.get_card().get_value() == CardValue.CLERIC:
                    target = units.get_unit_in_position(action.get_unit().get_pos())
                    if target is None:
                        return False
                    target.set_hp(target.get_hp() + unit.get_power())
                else:
                    target = enemy_units.get_unit_in_position(action.get_unit().get_pos())
                    if target is None:
                        return False
                    unit.attack_unit(target)
                    if target.get_hp() <= 0:
                        enemy_units.remove_unit(target)
            else:
                target = units.get_unit_in_position(unit.get_pos())
                if target is None:
                    return False
                target.set_pos(action.get_position())

            self.update_score(game_state)
            return True

    def on_turn_ended(self, game_state: Union['GameState', 'Observation']) -> None:
        if self.is_turn_finished(game_state):
            player_cards = game_state.player_0_cards if game_state.current_turn == 0 else game_state.player_1_cards
            deck = game_state.player_0_deck if game_state.current_turn == 0 else game_state.player_1_deck
            while player_cards.get_number_cards() < game_state.game_parameters.cards_on_hand:
                player_cards.add_card(deck.get_first_card())
            game_state.current_turn = (game_state.current_turn + 1) % 2
            game_state.action_points_left = game_state.game_parameters.action_points_per_turn

    def is_terminal(self, game_state: Union['GameState', 'Observation']) -> bool:
        return game_state.player_0_units.crystals_alive() is False or game_state.player_1_units.crystals_alive() is False \
            or (game_state.player_0_units.get_units_alive() == 0 and game_state.player_0_cards.is_empty()) \
            or (game_state.player_1_units.get_units_alive() == 0 and game_state.player_1_cards.is_empty())

    def is_turn_finished(self, game_state: Union['GameState', 'Observation']) -> bool:
        return game_state.action_points_left == 0
# endregion

# region Helpers
    def update_score(self, game_state: Union['GameState', 'Observation']) -> None:
        """Update score."""
        if game_state.current_turn == 0:
            current_hp = sum(map(lambda unit: unit.get_hp(), game_state.player_0_units.get_units()))
            enemy_hp = sum(map(lambda unit: unit.get_hp(), game_state.player_1_units.get_units()))
            score = current_hp - enemy_hp
            score += game_state.player_0_cards.get_playable_cards(game_state.player_0_units)
            game_state.player_0_score += score
        else:
            current_hp = sum(map(lambda unit: unit.get_hp(), game_state.player_1_units.get_units()))
            enemy_hp = sum(map(lambda unit: unit.get_hp(), game_state.player_0_units.get_units()))
            score = current_hp - enemy_hp
            score += game_state.player_1_cards.get_playable_cards(game_state.player_1_units)
            game_state.player_1_score += score
# endregion    