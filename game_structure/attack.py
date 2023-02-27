from game_structure import AttackType

class Attack:
    def __init__(self, range: int, type: 'AttackType', mele_multiplier: float, range_multiplier: float, chain: bool, push: bool):
        """Attack is a base class for all attacks that a unit can use in the game."""
        self.range = range
        self.type = type
        self.mele_multiplier = mele_multiplier
        self.range_multiplier = range_multiplier
        self.chain = chain
        self.push = push

# region Methods
    def clone(self) -> 'Attack':
        """Create new attack with the same info."""
        return Attack(
            self.range,
            self.type,
            self.mele_multiplier,
            self.range_multiplier,
            self.chain,
            self.push,
        )
    
    def copy_into(self, other: 'Attack') -> None:
        """Copies the attack contents into another one."""
        other.range = self.range
        other.type = self.type
        other.mele_multiplier = self.mele_multiplier
        other.range_multiplier = self.range_multiplier
        other.chain = self.chain
        other.push = self.push
# endregion

# region Getters
    def get_range(self) -> int:
        """Get range."""
        return self.range

    def get_type(self) -> 'AttackType':
        """Get type."""
        return self.type

    def get_mele_multiplier(self) -> float:
        """Get mele multiplier."""
        return self.mele_multiplier

    def get_range_multiplier(self) -> float:
        """Get range multiplier."""
        return self.range_multiplier

    def get_chain(self) -> bool:
        """Get chain."""
        return self.chain

    def get_push(self) -> bool:
        """Get push."""
        return self.push
# endregion

# region Override
    def __str__(self) -> str:
        """Get string representation of attack."""
        return f"Attack[{self.range}, {self.type.name}, {self.mele_multiplier}, {self.range_multiplier}, {self.chain}, {self.push}]"
# endregion