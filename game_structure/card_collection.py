from typing import List
from game_structure import Card

class CardCollection:
    def __init__(self):
        self.cards: List['Card'] = []

# region Methods
    def clone(self) -> 'CardCollection':
        """Create new collection with the same cards."""
        new_card_collection = CardCollection()
        for card in self.cards:
            new_card_collection.add_card(card.clone())
        return new_card_collection

    def add_card(self, card: 'Card'):
        """Add a card to the collection."""
        self.cards.append(card)

    def add_cards(self, cards: List['Card']):
        """Add a list of cards to the collection."""
        self.cards.extend(cards)

    def remove_card(self, card: 'Card'):
        """Remove a card from the collection."""
        self.cards.remove(card)

    def get_first_card(self) -> 'Card':
        """Get the first card from the collection."""
        return self.cards.pop(0)
# endregion

# region Getters
    def get_cards(self) -> List['Card']:
        """Get all cards."""
        return self.cards
# endregion

# region Override
    def __str__(self) -> str:
        """Get a string representation of the collection."""
        return f"CardCollection(cards={self.cards})"
# endregion