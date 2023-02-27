class Heal:
    def __init__(self, range: int, heal: int, revive: int) -> None:
        """Heal is a base class for all heals that a unit can use in the game."""
        self.range = range
        self.heal = heal
        self.revive = revive

# region Methods
    def clone(self) -> 'Heal':
        """Create new heal with the same info."""
        return Heal(self.range, self.heal, self.revive)
    
    def copy_into(self, other: 'Heal') -> None:
        """Copies the heal contents into another one."""
        other.range = self.range
        other.heal = self.heal
        other.revive = self.revive
# endregion

# region Getters
    def get_range(self) -> int:
        """Get range."""
        return self.range

    def get_heal(self) -> int:
        """Get heal."""
        return self.heal

    def get_revive(self) -> int:
        """Get revive."""
        return self.revive
# endregion

# region Override
    def __str__(self) -> str:
        """Get string representation of heal."""
        return f"Heal[{self.range}, {self.heal}, {self.revive}]"
# endregion