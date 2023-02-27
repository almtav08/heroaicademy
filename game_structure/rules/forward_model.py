from abc import ABC, abstractmethod
from typing import Union
import game_structure as gs

class ForwardModel(ABC):
    """Abstract class that will define the rules for the game"""

    @abstractmethod
    def step(self, game_state: Union['gs.GameState', 'gs.Observation'], action: 'gs.Action') -> bool:
        """Executes the action and moves the game to the next state."""
        pass

    @abstractmethod
    def on_turn_ended(self, game_state: Union['gs.GameState', 'gs.Observation']) -> None:
        """Moves the game to the next turn."""
        pass

    @abstractmethod
    def is_terminal(self, game_state: Union['gs.GameState', 'gs.Observation']) -> bool:
        """Checks if the game is ended."""
        pass

    @abstractmethod
    def is_turn_finished(self, game_state: Union['gs.GameState', 'gs.Observation']) -> bool:
        """Checks if the turn is ended."""
        pass