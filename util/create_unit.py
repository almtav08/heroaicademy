from typing import Tuple
from copy import deepcopy
import game_structure as gs

def create(card: 'gs.Card', position: Tuple[int, int]) -> 'gs.Unit':
    if card.get_value() == gs.CardValue.ARCHER:
        return gs.Unit(card.clone(), 700, 700, 2, 200, 4, 5, deepcopy(position), [])
    elif card.get_value() == gs.CardValue.KNIGHT:
        return gs.Unit(card.clone(), 1000, 1000, 1, 250, 1, 20, deepcopy(position), [])
    elif card.get_value() == gs.CardValue.CLERIC:
        return gs.Unit(card.clone(), 600, 600, 1, 150, 2, 0, deepcopy(position), [])
    elif card.get_value() == gs.CardValue.WIZARD:
        return gs.Unit(card.clone(), 800, 800, 2, 200, 2, 10, deepcopy(position), [])
    elif card.get_value() == gs.CardValue.NINJA:
        return gs.Unit(card.clone(), 700, 700, 3, 200, 1, 5, deepcopy(position), [])
    elif card.get_value() == gs.CardValue.CRYSTAL:
        return gs.Unit(card.clone(), 4500, 4500, 0, 0, 0, 30, deepcopy(position), [])
    else:
        return None