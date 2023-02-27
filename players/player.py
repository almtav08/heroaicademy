from abc import ABC, abstractmethod
import game_structure as gs

class Player(ABC):

    @abstractmethod
    def think(self, observation: 'gs.Observation', budget: float) -> 'gs.Action':
        pass
