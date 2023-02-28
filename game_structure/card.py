import game_structure as gs

class Card:
    def __init__(self, value: 'gs.CardValue', card_type: 'gs.CardType'):
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
    def get_value(self) -> 'gs.CardValue':
        """Get value."""
        return self.value
    
    def get_card_type(self) -> 'gs.CardType':
        """Get card type."""
        return self.card_type
# endregion

# region Helpers
    def is_playable(self, units: 'gs.UnitsCollection') -> bool:
        """Check if card is playable."""
        return self.value.is_unit_value() or self.value.is_spell_value() or (self.value.is_item_value() and len(units.get_available_units()) > 0)
# endregion

# region Override
    def __str__(self) -> str:
        """Get string representation of card."""
        return f"Card[{self.value.name}]"
    
    def __eq__(self, __o: object) -> bool:
        return self.value.name == __o.value.name and self.card_type.name == __o.card_type.name
# endregion