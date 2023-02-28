from typing import Dict, List, Tuple
from util.create_unit import create
import game_structure as gs
import random

class GameState:
    """GameState class represents the state of the game."""

    def __init__(self, game_parameters: 'gs.GameParameters') -> None:
        self.game_parameters = game_parameters
        self.current_turn = 0
        self.player_0_score = 0
        self.player_1_score = 0
        self.action_points_left = 0
        self.board = self.initiliaze_board_dict()
        self.player_0_deck: 'gs.CardCollection' = self.initiliaze_deck()
        self.player_1_deck: 'gs.CardCollection' = self.initiliaze_deck()
        self.player_0_discard: 'gs.CardCollection' = gs.CardCollection()
        self.player_1_discard: 'gs.CardCollection' = gs.CardCollection()
        self.player_0_cards: 'gs.CardCollection' = self.initiliaze_cards(self.player_0_deck)
        self.player_1_cards: 'gs.CardCollection' = self.initiliaze_cards(self.player_1_deck)
        self.player_0_units: 'gs.UnitsCollection' = self.initiliaze_units()
        self.player_1_units: 'gs.UnitsCollection' = self.initiliaze_units(False)

# region Methods
    def get_observation(self) -> 'gs.Observation':
        """Return the observation of the game state."""
        return gs.Observation(self, False)

    def reset(self) -> None:
        """Reset the game state."""
        self.current_turn = 0
        self.player_0_score = 0
        self.player_1_score = 0
        self.action_points_left = self.game_parameters.action_points_per_turn
        self.board = self.initiliaze_board_dict()
        self.player_0_deck = self.initiliaze_deck()
        self.player_1_deck = self.initiliaze_deck()
        self.player_0_discard: 'gs.CardCollection' = gs.CardCollection()
        self.player_1_discard: 'gs.CardCollection' = gs.CardCollection()
        self.player_0_cards: 'gs.CardCollection' = self.initiliaze_cards(self.player_0_deck)
        self.player_1_cards: 'gs.CardCollection' = self.initiliaze_cards(self.player_1_deck)
        self.player_0_units = self.initiliaze_units()
        self.player_1_units = self.initiliaze_units(False)
#endregion

#region Helpers
    def initiliaze_board_dict(self) -> Dict[Tuple[int, int], 'gs.TileType']:
        """Initialize the board of the game."""
        board_size = self.game_parameters.board_size
        board = {(i, j): gs.TileType.EMPTY for i in range(board_size[0]) for j in range(board_size[1])}
        for attack in self.game_parameters.attack_positions:
            board[attack] = gs.TileType.ATTACK
            board[(attack[0], board_size[1] - attack[1] - 1)] = gs.TileType.ATTACK
        for speed in self.game_parameters.speed_positions:
            board[speed] = gs.TileType.SPEED
            board[(speed[0], board_size[1] - speed[1] - 1)] = gs.TileType.SPEED
        return board

    def initiliaze_cards(self, deck: 'gs.CardCollection') -> 'gs.CardCollection':
        """Initialize the cards of the game."""
        cards = gs.CardCollection()
        for _ in range(self.game_parameters.cards_on_hand):
            cards.add_card(deck.get_first_card())
        return cards

    def initiliaze_deck(self) -> 'gs.CardCollection':
        """Initialize the deck of the game."""
        deck = gs.CardCollection()
        for value in gs.CardValue:
            if value is not gs.CardValue.CRYSTAL:
                deck.add_card(gs.Card(value, value.get_card_type()))
                deck.add_card(gs.Card(value, value.get_card_type()))
                deck.add_card(gs.Card(value, value.get_card_type()))
                if value.is_spell_value() or value.is_item_value():
                    deck.add_card(gs.Card(value, value.get_card_type()))
                    deck.add_card(gs.Card(value, value.get_card_type()))
        random.shuffle(deck.cards)
        return deck

    def initiliaze_units(self, player_1 = True) -> 'gs.UnitsCollection':
        """Initialize the units of the game."""
        units = gs.UnitsCollection()
        for crystal in self.game_parameters.crystal_positions:
            position = (crystal[0], crystal[1]) if player_1 else (crystal[0], self.game_parameters.board_size[1] - crystal[1] - 1)
            card = gs.Card(gs.CardValue.CRYSTAL, gs.CardType.UNIT)
            units.add_unit(create(card, position))
        return units
#endregion

#region Override
    def __str__(self):
        return (f"TURN: {self.current_turn!s}\n"
                #f"BOARD: {self.board!s}\n"
                f"SCORE P1: {self.player_0_score!s}\n"
                f"CARDS P1: {self.player_0_cards!s}\n"
                f"UNITS P1: {self.player_0_units!s}\n"
                f"SCORE P2: {self.player_1_score!s}\n"
                f"SCORE P2: {self.player_1_cards!s}\n"
                f"UNITS P2: {self.player_1_units!s}\n"
                f"ACTION POINTS LEFT: {self.action_points_left!s}")
#endregion