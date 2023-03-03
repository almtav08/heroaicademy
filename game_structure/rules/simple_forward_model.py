from typing import Union, Tuple
from copy import deepcopy
from util.create_unit import create
import game_structure as gs
import game_structure.rules as rl

class SimpleForwardModel(rl.ForwardModel):
    def __init__(self):
        super().__init__()

# region Methods
    def step(self, game_state: Union['gs.GameState', 'gs.Observation'], action: 'gs.Action') -> bool:
        """Perform an action on the game state."""
        game_state.action_points_left -= 1

        if action is None:
            return False
        
        action_pos = deepcopy(action.get_position()) if action.get_position() is not None else None
        unit = deepcopy(action.get_unit()) if action.get_unit() is not None else None
        
        cards = game_state.player_0_cards if game_state.current_turn == 0 else game_state.player_1_cards
        units = game_state.player_0_units if game_state.current_turn == 0 else game_state.player_1_units
        enemy_units = game_state.player_1_units if game_state.current_turn == 0 else game_state.player_0_units
        #discard = game_state.player_0_discard if game_state.current_turn == 0 else game_state.player_1_discard

        if type(action.get_subject()) is gs.Card:
            card = action.get_subject().clone()
            if unit is None and action_pos is None:
                cards.remove_card(card)
                self.update_score(game_state)
                return True
            elif unit is not None:

                units.get_unit_in_position(deepcopy(unit.get_pos())).get_equipement().append(card)
                cards.remove_card(card)
                self.update_score(game_state)
                return True
            elif action_pos is not None:
                if card.get_value().is_spell_value():
                    target = enemy_units.get_unit_in_position(action_pos)
                    if target is None:
                        return False
                    target.set_hp(target.get_hp() - 400)
                    if target.get_hp() <= 0:
                        enemy_units.remove_unit(target)
                elif card.get_value() == gs.CardValue.HEAL_POTION:
                    target = units.get_unit_in_position(action_pos)
                    if target is None:
                        return False
                    target.set_hp(target.get_hp() + 300)
                else:
                    units.add_unit(create(card, action_pos))
                cards.remove_card(card)
                self.update_score(game_state)
                return True
            else:
                return False
        else:
            subject = action.get_subject().clone()
            if action_pos is None:
                if subject.get_card().get_value() == gs.CardValue.CLERIC and unit in units.get_units():
                    target = units.get_unit_in_position(unit.get_pos())
                    if target is None:
                        return False
                    target.set_hp(target.get_hp() + unit.get_power())
                else:
                    target = enemy_units.get_unit_in_position(unit.get_pos())
                    if target is None:
                        return False
                    subject.attack_unit(target, game_state.board[subject.get_pos()] == gs.TileType.ATTACK)
                    if target.get_hp() <= 0:
                        enemy_units.remove_unit(target)
            else:
                target = units.get_unit_in_position(subject.get_pos())
                if target is None:
                    return False
                target.set_pos(action_pos)

            self.update_score(game_state)
            return True

    def on_turn_ended(self, game_state: Union['gs.GameState', 'gs.Observation']) -> None:
        if self.is_turn_finished(game_state):
            player_cards = game_state.player_0_cards if game_state.current_turn == 0 else game_state.player_1_cards
            deck = game_state.player_0_deck if game_state.current_turn == 0 else game_state.player_1_deck
            for _ in range(game_state.game_parameters.cards_on_hand - player_cards.get_number_cards()):
                card_add = deck.get_first_card()
                if card_add is not None:
                    player_cards.add_card(card_add)
            game_state.current_turn = (game_state.current_turn + 1) % 2
            game_state.action_points_left = game_state.game_parameters.action_points_per_turn

    def is_terminal(self, game_state: Union['gs.GameState', 'gs.Observation']) -> bool:
        if self.current_player_cant_play(game_state) and self.next_player_has_units(game_state):
            if game_state.current_turn == 0:
                game_state.player_1_score += game_state.player_0_score * 2
            else:
                game_state.player_0_score += game_state.player_1_score * 2

        return not game_state.player_0_units.crystals_alive() or not game_state.player_1_units.crystals_alive() \
            or self.current_player_cant_play(game_state)

    def is_turn_finished(self, game_state: Union['gs.GameState', 'gs.Observation']) -> bool:
        return game_state.action_points_left == 0
# endregion

# region Helpers
    def current_player_cant_play(self, game_state: Union['gs.GameState', 'gs.Observation']) -> bool:
        """Return if the player can't play."""
        current_units = game_state.player_0_units if game_state.current_turn == 0 else game_state.player_1_units
        current_cards = game_state.player_0_cards if game_state.current_turn == 0 else game_state.player_1_cards

        return current_units.get_units_alive() == 0 and current_cards.is_empty()
    
    def next_player_has_units(self, game_state: Union['gs.GameState', 'gs.Observation']) -> bool:
        """Return if the player can't play."""
        next_units = game_state.player_1_units if game_state.current_turn == 0 else game_state.player_0_units
        next_cards = game_state.player_1_cards if game_state.current_turn == 0 else game_state.player_0_cards
        next_deck = game_state.player_1_deck if game_state.current_turn == 0 else game_state.player_0_deck

        return next_units.get_units_alive() > 0 or next_cards.get_unit_cards() > 0 or next_deck.get_unit_cards() > 0

    def update_score(self, game_state: Union['gs.GameState', 'gs.Observation']) -> None:
        """Update score."""
        if game_state.current_turn == 0:
            current_hp = sum(map(lambda unit: unit.get_hp(), game_state.player_0_units.get_crystals()))
            enemy_hp = sum(map(lambda unit: unit.get_hp(), game_state.player_1_units.get_crystals()))
            score = max((int((current_hp - enemy_hp) / 100)), 0)
            current_attack = sum(map(lambda unit: unit.get_bonus_attack(), game_state.player_0_units.get_units()))
            enemy_attack = sum(map(lambda unit: unit.get_bonus_attack(), game_state.player_1_units.get_units()))
            score += max((int((current_attack - enemy_attack) / 10)), 0)
            #playable_cards = game_state.player_0_cards.get_playable_cards(game_state.player_0_units)
            #score += (game_state.game_parameters.cards_on_hand - len(playable_cards)) * 10
            score += max((game_state.player_0_units.get_units_alive() - game_state.player_1_units.get_units_alive()), 0) * 10
            game_state.player_0_score += score
        else:
            current_hp = sum(map(lambda unit: unit.get_hp(), game_state.player_1_units.get_crystals()))
            enemy_hp = sum(map(lambda unit: unit.get_hp(), game_state.player_0_units.get_crystals()))
            score = max((int((current_hp - enemy_hp) / 100)), 0)
            current_attack = sum(map(lambda unit: unit.get_bonus_attack(), game_state.player_1_units.get_units()))
            enemy_attack = sum(map(lambda unit: unit.get_bonus_attack(), game_state.player_0_units.get_units()))
            score += max((int((current_attack - enemy_attack) / 10)), 0)
            #playable_cards = game_state.player_1_cards.get_playable_cards(game_state.player_1_units)
            #score += (game_state.game_parameters.cards_on_hand - len(playable_cards)) * 10
            score += max((game_state.player_1_units.get_units_alive() - game_state.player_0_units.get_units_alive()), 0) * 10
            game_state.player_1_score += score
# endregion    