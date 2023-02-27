from typing import Tuple, List
from copy import deepcopy
from game_structure import Card, Resistance, Attack, Heal

class Unit:
    def __init__(
        self,
        card: 'Card',
        hp: int,
        max_hp: int,
        speed: int,
        power: int,
        resistance: 'Resistance',
        attack: 'Attack',
        heal: 'Heal',
        swap: bool,
        pos: Tuple[int, int],
        equipement: List['Card']
    ) -> None:
        """Unit is a base class for all units that a player can use in the game."""
        self.card = card
        self.hp = hp
        self.max_hp = max_hp
        self.speed = speed
        self.power = power
        self.resistance = resistance
        self.attack = attack
        self.heal = heal
        self.swap = swap
        self.pos = pos
        self.equipement = equipement

# region Methods
    def clone(self) -> 'Unit':
        """Create new unit with the same info."""
        return Unit(
            self.card.clone(),
            self.hp,
            self.max_hp,
            self.speed,
            self.power,
            self.resistance.clone(),
            self.attack.clone(),
            self.heal.clone(),
            self.swap,
            self.pos,
            deepcopy(self.equipement)
        )

    def copy_into(self, other: 'Unit') -> None:
        """Copies the unit contents into another one."""
        other.card = self.card.clone()
        other.hp = self.hp
        other.max_hp = self.max_hp
        other.speed = self.speed
        other.power = self.power
        other.resistance = self.resistance.clone()    
        other.attack = self.attack.clone()
        other.heal = self.heal.clone()
        other.swap = self.swap
        other.pos = self.pos
        other.equipement = deepcopy(self.equipement)
# endregion

# region Getters
    def get_card(self) -> 'Card':
        """Get unit card."""
        return self.card

    def get_pos(self) -> Tuple[int, int]:
        """Get unit position."""
        return self.pos

    def get_hp(self) -> int:
        """Get unit hp."""
        return self.hp

    def get_max_hp(self) -> int:
        """Get unit max hp."""
        return self.max_hp

    def get_speed(self) -> int:
        """Get unit speed."""
        return self.speed

    def get_power(self) -> int:
        """Get unit power."""
        return self.power

    def get_resistance(self) -> 'Resistance':
        """Get unit resistance."""
        return self.resistance

    def get_attack(self) -> 'Attack':
        """Get unit attack."""
        return self.attack

    def get_heal(self) -> 'Heal':
        """Get unit heal."""
        return self.heal

    def get_swap(self) -> bool:
        """Get unit swap."""
        return self.swap
    
    def get_equipement(self) -> List['Card']:
        """Get unit equipement."""
        return self.equipement
# endregion

# region Setters
    def set_hp(self, hp: int) -> None:
        """Set unit hp."""
        self.hp = min(hp, self.max_hp)

    def set_pos(self, pos: Tuple[int, int]) -> None:
        """Set unit position."""
        self.pos = deepcopy(pos)
# endregion

# region Helpers
    def possible_moves(self, board_size: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Return a list of possible moves for the unit."""
        moves = []
        for x in range(self.pos[0] - self.speed, self.pos[0] + self.speed + 1):
            for y in range(self.pos[1] - self.speed, self.pos[1] + self.speed + 1):
                if x >= 0 and x < board_size[0] and y >= 0 or y < board_size[1]:
                    moves.append((x, y))
        return moves
    
    def is_in_range(self, other: 'Unit') -> bool:
        """Check if the unit is in range of the other unit."""
        return other.get_attack().get_range() >= abs(self.pos[0] - other.pos[0]) + abs(self.pos[1] - other.pos[1])
# endregion

# region Override
    def __str__(self) -> str:
        """Return string representation of unit."""""
        return (
            f"HP: {self.hp} / {self.max_hp}\n"
            f"Speed: {self.speed}\n"
            f"Power: {self.power}\n"
            f"{self.card}\n"
            f"{self.resistance}\n"
            f"{self.attack}\n"
            f"{self.heal}\n"
            f"Swap: {self.swap}\n"
            f"Pos: {self.pos}\n"
            f"Equipement: {self.equipement}"
        )
# endregion