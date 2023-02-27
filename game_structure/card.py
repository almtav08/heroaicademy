from game_structure import CardType, CardValue

class Card:
    def __init__(self, value: 'CardValue', card_type: 'CardType'):
        """Card is a base class for all cards that a player can use in the game."""
        self.value = value
        self.card_type = card_type

# region Methods
    def clone(self) -> 'Card':
        """Create new card with the same info."""
        return Card(self.value, self.card_type)

    def copy_into(self, other: 'Card') -> None:
        """Copies the card contents into another one."""
        other.value = self.value
        other.card_type = self.card_type
# endregion

# region Getters
    def get_value(self) -> 'CardValue':
        """Get value."""
        return self.value
    
    def get_card_type(self) -> 'CardType':
        """Get card type."""
        return self.card_type
# endregion

# region Override
    def __str__(self) -> str:
        """Get string representation of card."""
        return f"Card[{self.value.name}, {self.card_type.name}]"
# endregion