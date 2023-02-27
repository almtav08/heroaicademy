from typing import List, Tuple
from copy import deepcopy
import game_structure as gs

class UnitsCollection:
    """A collection of units the player will use during the game."""

    def __init__(self) -> None:
        self.units: List['gs.Unit'] = []

# region Methods
    def clone(self) -> 'UnitsCollection':
        """Create new collection with the same units."""
        new_units_collection = UnitsCollection()
        for unit in self.units:
            new_units_collection.add_unit(unit.clone())
        return new_units_collection

    def add_unit(self, unit: 'gs.Unit'):
        """Add a unit to the collection."""
        self.units.append(unit)

    def add_units(self, units: List['gs.Unit']):
        """Add a list of units to the collection."""
        self.units.extend(units)

    def remove_unit(self, unit: 'gs.Unit'):
        """Remove a unit from the collection."""
        self.units.remove(unit)

    def move_unit(self, unit: 'gs.Unit', pos: Tuple[int, int]):
        """Move a unit to a new position."""
        unit.pos = deepcopy(pos)
# endregion

# region Getters
    def get_units(self) -> List['gs.Unit']:
        """Get all units."""
        return self.units
    
    def get_crystals(self) -> List['gs.Unit']:
        """Get all crystals."""
        return [unit for unit in self.units if unit.get_card().get_value().is_crystal_value()]
    
    def get_unit_positions(self) -> List[Tuple[int, int]]:
        """Get all unit positions."""
        return [unit.pos for unit in self.units]

    def get_available_units(self) -> List['gs.Unit']:
        """Get all units that are not dead."""
        return [unit for unit in self.units if not unit.get_card().get_value().is_unit_value()]
        
    def get_units_in_range(self, other: 'gs.Unit') -> List['gs.Unit']:
        """Return a list of units in range of the unit."""
        return [unit for unit in self.units if unit.is_in_range(other)]
    
    def get_avalible_positions_for_spawn(self) -> List[Tuple[int, int]]:
        """Return a list of positions where a unit can be spawned."""
        taken_positions = self.get_unit_positions()
        return [(x, y) for x in range(4) for y in range(4) if (x, y) not in taken_positions]
    
    def get_unit_in_position(self, pos: Tuple[int, int]) -> 'gs.Unit':
        """Return the unit in the given position."""
        return next((unit for unit in self.units if unit.pos == pos), None)
    
    def get_units_alive(self) -> List['gs.Unit']:
        """Return a list of all units that are not dead."""
        return len(self.units)
# endregion

# region Helpers
    def crystals_alive(self) -> bool:
        """Return True if there are crystals alive."""
        return len(self.get_crystals()) > 0
# endregion

# region Override
    def __str__(self) -> str:
        """Get a string representation of the collection."""
        return f"UnitsCollection(units={self.units})"
# endregion