from abc import ABC, abstractmethod
import game_structure as gs

class Heuristic(ABC):

    @abstractmethod
    def get_reward(self, observation: 'gs.Observation') -> int:
        pass