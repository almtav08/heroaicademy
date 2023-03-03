from typing import Tuple, Union
from copy import deepcopy
import game_structure as gs

class Action:
    def __init__(self, subject: Union['gs.Unit', 'gs.Card'], unit: 'gs.Unit' = None, position: Tuple[int, int] = None) -> None:
        """Actions stand for every possible action that can be taken per turn."""
        self.subject = subject
        self.unit = unit
        self.position = position

# region Methods
    def clone(self) -> 'Action':
        """Create new action with the same unit and pos."""
        return Action(self.subject.clone(), self.unit.clone() if self.unit is not None else None, deepcopy(self.position) if self.position is not None else None)

    def copy_into(self, other: 'Action') -> None:
        """Deep copies the `Action` contents into another one."""
        other.subject = self.subject.clone()
        if self.unit is not None:
            other.unit = self.unit.clone()
        else:
            other.unit = None
        if self.position is not None:
            other.position = deepcopy(self.position)
        else:
            other.position = None
# endregion

# region Getters
    def get_subject(self) -> Union['gs.Unit', 'gs.Card']:
        """Return subject."""
        return self.subject

    def get_unit(self) -> 'gs.Unit':
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
    
    def __eq__(self, __o: object) -> bool:
        return self.subject == __o.subject and self.unit == __o.unit and self.position == __o.position
# endregion