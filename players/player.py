from abc import ABC, abstractmethod
from game_structure import Observation, Action

class Player(ABC):

    @abstractmethod
    def think(self, observation: 'Observation', budget: float) -> 'Action':
        pass
