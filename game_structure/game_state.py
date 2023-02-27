from typing import Dict, List, Tuple
from game_structure import GameParameters, Observation, TileType, CardCollection, UnitsCollection, CardValue, CardType, Card, Unit
import random

class GameState:
    """GameState class represents the state of the game."""

    def __init__(self, game_parameters: 'GameParameters') -> None:
        self.game_parameters = game_parameters
        self.current_turn = 0
        self.player_0_score = 0
        self.player_1_score = 0
        self.action_points_left = 0
        self.board = self.initiliaze_board_dict()
        self.player_0_deck: 'CardCollection' = self.initiliaze_deck()
        self.player_1_deck: 'CardCollection' = self.initiliaze_deck()
        self.player_0_discard: 'CardCollection' = []
        self.player_1_discard: 'CardCollection' = []
        self.player_0_cards: 'CardCollection' = self.initiliaze_cards(self.player_0_deck)
        self.player_1_cards: 'CardCollection' = self.initiliaze_cards(self.player_1_deck)
        self.player_0_units: 'UnitsCollection' = self.initiliaze_units()
        self.player_1_units: 'UnitsCollection' = self.initiliaze_units(False)

# region Methods
    def get_observation(self) -> 'Observation':
        """Return the observation of the game state."""
        return Observation(self, False)

    def reset(self) -> None:
        """Reset the game state."""
        self.current_turn = 0
        self.player_0_score = 0
        self.player_1_score = 0
        self.action_points_left = self.game_parameters.action_points_per_turn
        self.board = self.initiliaze_board_dict()
        self.player_0_deck = self.initiliaze_deck()
        self.player_1_deck = self.initiliaze_deck()
        self.player_0_discard: 'CardCollection' = []
        self.player_1_discard: 'CardCollection' = []
        self.player_0_cards: 'CardCollection' = self.initiliaze_cards(self.player_0_deck)
        self.player_1_cards: 'CardCollection' = self.initiliaze_cards(self.player_1_deck)
        self.player_0_units = self.initiliaze_units()
        self.player_1_units = self.initiliaze_units(False)
#endregion

#region Helpers
    def initiliaze_board_dict(self) -> Dict[Tuple[int, int], TileType]:
        """Initialize the board of the game."""
        board_size = self.game_parameters.board_size
        board = {(i, j): TileType.EMPTY for i in range(board_size[0]) for j in range(board_size[1])}
        for attack in self.game_parameters.attack_positions:
            board[attack] = TileType.ATTACK
            board[(attack[0], board_size[1] - attack[1] - 1)] = TileType.ATTACK
        for speed in self.game_parameters.speed_positions:
            board[speed] = TileType.SPEED
            board[(speed[0], board_size[1] - speed[1] - 1)] = TileType.SPEED
        return board

    def initiliaze_cards(self, deck: 'CardCollection') -> 'CardCollection':
        """Initialize the cards of the game."""
        cards = CardCollection()
        for _ in range(self.game_parameters.cards_on_hand):
            cards.add_card(deck.get_first_card())
        return cards

    def initiliaze_deck(self) -> 'CardCollection':
        """Initialize the deck of the game."""
        deck = CardCollection()
        for value in CardValue:
            if value is not CardValue.CRYSTAL:
                deck.add_card(Card(value, value.get_card_type()))
                deck.add_card(Card(value, value.get_card_type()))
                deck.add_card(Card(value, value.get_card_type()))
                if value.is_spell_value() or value.is_item_value():
                    deck.add_card(Card(value, value.get_card_type()))
                    deck.add_card(Card(value, value.get_card_type()))
        random.shuffle(deck.cards)
        return deck

    def initiliaze_units(self, player_1 = True) -> 'UnitsCollection':
        """Initialize the units of the game."""
        units = UnitsCollection()
        for crystal in self.game_parameters.crystal_positions:
            position = (crystal[0], crystal[1]) if player_1 else (crystal[0], self.game_parameters.board_size[1] - crystal[1] - 1)
            units.add_unit(Unit(Card(CardValue.CRYSTAL, CardType.UNIT), 4500, 4500, 0, 0, None, None, None, False, position, None))
        return units
#endregion

#region Override
    def __str__(self):
        return (f"TURN: {self.current_turn!s}\n"
                #f"BOARD: {self.board!s}\n"
                f"SCORE P1: {self.player_0_score!s}\n"
                f"SCORE P2: {self.player_1_score!s}\n"
                f"ACTION POINTS LEFT: {self.action_points_left!s}")
#endregion