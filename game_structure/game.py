import random
import sys
import func_timeout
from typing import Optional
import game_structure as gs
from players import Player


class Game:
    """Contains the logic for playing the Tank War game """

    def __init__(self, parameters: "gs.GameParameters"):
        self.save_file = None
        self.game_state = gs.GameState(parameters)

# region Methods
    def reset(self) -> None:
        """Resets the gamestate so that is ready for a new game."""
        self.game_state.reset()

    def run(self, player_0: "Player", player_1: "Player", budget: float, verbose: bool, enforce_time: bool) -> None:
        """Runs a game."""
        save_str = ""

        #if self.game_state.game_parameters.seed is None:
        #    seed = random.randrange(sys.maxsize)
        #else:
        #    seed = self.game_state.game_parameters.seed

        #random.seed(seed)
        #if self.save_file is not None:
        #    save_str += f"{seed}\n"
        #if verbose:
        #    print("")
        #    print("*** ------------------------------------------------- ")
        #    print(f"*** Game started with seed {seed}")
        #    print("*** ------------------------------------------------- ")

        self.reset()

        if self.save_file is not None:
            save_str += f"{self.game_state.game_parameters}\n"
            save_str += f"{player_0!s} {player_1!s}\n"
            save_str += f"{self.game_state.board!s}\n"
            save_str += f"{self.game_state.player_0_units!s}\n"
            save_str += f"{self.game_state.player_1_units!s}\n"

        players = [player_0, player_1]

        # Run players' turns while the game is not finished
        while not self.game_state.game_parameters.forward_model.is_terminal(self.game_state):
            action = self.play_turn(players[self.game_state.current_turn], budget, verbose, enforce_time)

            if self.save_file is not None:
                save_str += f"{self.game_state.current_turn!s} {action!s}\n"

            self.game_state.game_parameters.forward_model.on_turn_ended(self.game_state)

        if self.save_file is not None:
            self.save_file.write(save_str)
            self.save_file.close()

    def play_turn(self, player: "Player", budget: float, verbose: bool,enforce_time: bool) -> "gs.Action":
        """Performs a player turn."""
        if verbose:
            print("")
            print("---------------------------------------- ")
            print(f"Player {self.game_state.current_turn} [{player!s}] turn")
            print("---------------------------------------- ")
            print(f"{self.game_state}\n")

        while not self.game_state.game_parameters.forward_model.is_turn_finished(self.game_state):
            # Observable part of the GameState
            observation = self.game_state.get_observation()

            # When enforce_time is True, the player has budget seconds to think.
            # If they take more than that, a random action is played instead.
            if enforce_time:
                try:
                    action = func_timeout.func_timeout(budget, self.think, args=[player, observation, budget])
                except func_timeout.FunctionTimedOut:
                    if verbose:
                        print("Too much time thinking. A random action was selected!")
                    action = self.think(player, observation, budget)
            else:
                action = self.think(player, observation, budget)

            if action is None:
                if verbose:
                    print("Player didn't return an action. A random action was selected!")
                action = self.random_action(observation)

            if verbose:
                print(f"Player {self.game_state.current_turn} selects {action!s}.")

            self.game_state.game_parameters.forward_model.step(self.game_state, action)

            if verbose:
                print(f"Score: [{self.game_state.player_0_score}] - [{self.game_state.player_1_score}]")
            return action

    def think(self, player: "Player", observation: "gs.Observation", budget: float) -> "gs.Action":
        """Requires the player to decide, given an observation, what action to play and returns it."""
        return player.think(observation, budget)

    def random_action(self, observation: "gs.Observation") -> "gs.Action":
        """Returns a random valid action for the state defined in the given observation."""
        actions = observation.get_actions()
        return random.choice(actions)
# endregion

# region Getters and Setters
    def set_save_file(self, filename: "Optional[str]") -> None:
        """Sets the file that the `Game` is saved to."""
        self.save_file = open(filename, "w") if filename is not None else None

    def get_winner(self) -> int:
        """Returns the index of the `ASMACAG.Players.Player.Player` that is winning the `Game`."""
        if self.game_state.player_0_score > self.game_state.player_1_score:
            return 0
        elif self.game_state.player_1_score > self.game_state.player_0_score:
            return 1
        else:
            return -1
# endregion
