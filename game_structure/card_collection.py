from typing import List
import game_structure as gs

class CardCollection:
    def __init__(self):
        self.cards: List['gs.Card'] = []

# region Methods
    def clone(self) -> 'CardCollection':
        """Create new collection with the same cards."""
        new_card_collection = CardCollection()
        for card in self.cards:
            new_card_collection.add_card(card.clone())
        return new_card_collection

    def add_card(self, card: 'gs.Card'):
        """Add a card to the collection."""
        self.cards.append(card)

    def add_cards(self, cards: List['gs.Card']):
        """Add a list of cards to the collection."""
        self.cards.extend(cards)

    def remove_card(self, card: 'gs.Card'):
        """Remove a card from the collection."""
        self.cards.remove(card)
# endregion

# region Getters
    def get_cards(self) -> List['gs.Card']:
        """Get all cards."""
        return self.cards
    
    def get_first_card(self) -> 'gs.Card':
        """Get the first card from the collection."""
        return self.cards.pop(0)
    
    def get_number_cards(self) -> bool:
        """Get the number of cards in the collection."""
        return len(self.cards)
    
    def get_playable_cards(self, units: 'gs.UnitsCollection') -> List['gs.Card']:
        """Get all cards that can be played."""
        return [card for card in self.cards if card.is_playable(units)]
# endregion

# region Helpers
    def is_empty(self) -> bool:
        """Check if the collection is empty."""
        return len(self.cards) == 0
# endregion

# region Override
    def __str__(self) -> str:
        """Get a string representation of the collection."""
        return f"CardCollection(cards={self.cards})"
# endregion