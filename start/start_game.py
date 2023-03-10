from typing import List, Tuple
from game_structure import GameParameters, Game
from game_structure.rules import SimpleForwardModel
from players import Player, OEPlayer, MCTSPlayer, OSLAPlayer
from heuristics import SimpleHeuristic
import players as pl

def start_game() -> Tuple['Game', List[Player]]:
    forward_model = SimpleForwardModel()
    parameters = GameParameters()
    parameters.forward_model = forward_model
    players = [MCTSPlayer(SimpleHeuristic(), 8), OEPlayer(SimpleHeuristic(), 125, 0.15, 0.15)]
    game = Game(parameters)
    budget = 6
    return (game, players, budget)