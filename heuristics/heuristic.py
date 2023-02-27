from abc import ABC, abstractmethod
from game_structure import Observation

class Heuristic(ABC):

    @abstractmethod
    def get_reward(self, observation: 'Observation') -> int:
        pass