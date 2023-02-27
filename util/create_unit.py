from game_structure import CardValue, Card, Unit
from typing import Tuple
from copy import deepcopy

def create(card: 'Card', position: Tuple[int, int]) -> 'Unit':
    if card.get_value() == CardValue.ARCHER:
        return Unit(card, 700, 700, 2, 200, 4, 5, deepcopy(position), [])
    elif card.get_value() == CardValue.KNIGHT:
        return Unit(card, 1000, 1000, 1, 250, 1, 20, deepcopy(position), [])
    elif card.get_value() == CardValue.CLERIC:
        return Unit(card, 600, 600, 1, 150, 2, 0, deepcopy(position), [])
    elif card.get_value() == CardValue.WIZARD:
        return Unit(card, 800, 800, 2, 200, 2, 10, deepcopy(position), [])
    elif card.get_value() == CardValue.NINJA:
        return Unit(card, 700, 700, 3, 200, 1, 5, deepcopy(position), [])
    else:
        return None