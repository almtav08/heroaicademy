from typing import Tuple, Union
from copy import deepcopy
from game_structure import Unit, Card

class Action:
    def __init__(self, subject: Union['Unit', 'Card'], unit: 'Unit' = None, position: Tuple[int, int] = None) -> None:
        """Actions stand for every possible action that can be taken per turn."""
        self.subject = subject
        self.unit = unit
        self.position = position

# region Methods
    def clone(self) -> 'Action':
        """Create new action with the same unit and pos."""
        return Action(self.subject.clone(), self.unit.clone(), deepcopy(self.position))

    def copy_into(self, other: 'Action') -> None:
        """Deep copies the `Action` contents into another one."""
        other.subject = self.subject.clone()
        other.unit = self.unit.clone()
        other.position = deepcopy(self.position)
# endregion

# region Getters
    def get_subject(self) -> Union['Unit', 'Card']:
        """Return subject."""
        return self.subject

    def get_unit(self) -> 'Unit':
        """Return option."""
        return self.unit

    def get_position(self) -> Tuple[int, int]:
        """Return position."""
        return self.position
# endregion

# region Override
    def __str__(self) -> str:
        """Return string representation of action."""
        return f"Action(subject={self.subject!s}, option={self.unit!s}, position={self.position})"
# endregion