from typing import Tuple, List
from copy import deepcopy
import game_structure as gs

class Unit:
    def __init__(
        self,
        card: 'gs.Card',
        hp: int,
        max_hp: int,
        speed: int,
        power: int,
        range: int,
        resistance: int,
        pos: Tuple[int, int],
        equipement: List['gs.Card']
    ) -> None:
        """Unit is a base class for all units that a player can use in the game."""
        self.card = card
        self.hp = hp
        self.max_hp = max_hp
        self.speed = speed
        self.power = power
        self.range = range
        self.resistance = resistance
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
            self.range,
            self.resistance,
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
        other.range = self.range
        other.resistance = self.resistance   
        other.pos = self.pos
        other.equipement = deepcopy(self.equipement)
# endregion

# region Getters
    def get_card(self) -> 'gs.Card':
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
    
    def get_range(self) -> int:
        """Get unit range."""
        return self.range

    def get_resistance(self) -> int:
        """Get unit resistance."""
        return self.resistance
    
    def get_equipement(self) -> List['gs.Card']:
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
                if x >= 0 and x < board_size[0] and y >= 0 and y < board_size[1] and (x, y) != self.pos:
                    moves.append((x, y))
        return moves
    
    def is_in_range(self, other: 'Unit') -> bool:
        """Check if the unit is in range of the other unit."""
        return other.get_range() >= abs(self.pos[0] - other.pos[0]) + abs(self.pos[1] - other.pos[1])
    
    def attack_unit(self, other: 'Unit') -> None:
        """Attack other unit."""
        damage = int(self.power * (100 - other.resistance) / 100)
        other.set_hp(other.get_hp() - damage)
# endregion

# region Override
    def __str__(self) -> str:
        """Return string representation of unit."""""
        return (
            f"Unit[{self.card.get_value().name}, HP: {self.hp} / {self.max_hp}, POS: {self.pos}]"
            #f"Speed: {self.speed}\n"
            #f"Power: {self.power}\n"
            #f"{self.card}\n"
            #f"{self.resistance}\n"
            #f"Pos: {self.pos}\n"
            #f"Equipement: {self.equipement}"
        )
# endregion