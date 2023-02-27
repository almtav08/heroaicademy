class Resistance:
    def __init__(self, physical: int, magical: int):
        """Resistance is a base class for all resistances that a unit can have in the game."""
        self.physical = physical
        self.magical = magical

# region Methods    
    def clone(self) -> 'Resistance':
        """Create new resistance with the same info."""
        return Resistance(self.physical, self.magical)

    def copy_into(self, other: 'Resistance') -> None:
        """Copies the resistance contents into another one."""
        other.physical = self.physical
        other.magical = self.magical
# endregion

# region Getters
    def get_physical(self) -> int:
        """Get physical resistance."""
        return self.physical

    def get_magical(self) -> int:
        """Get magical resistance."""
        return self.magical
# endregion

# region Override
    def __str__(self) -> str:
        """Get string representation of resistance."""
        return f"Resistance[{self.physical}, {self.magical}]"
# endregion