import game_structure.rules as rl

class GameParameters:
    """Class that holds all the game parameters."""
    
    def __init__(self,
            board_size=(5, 9),
            action_points_per_turn=5,
            cards_on_deck = 45,
            cards_on_hand = 5,
            crystal_positions = [(1, 2), (3, 1)],
            forward_model: 'rl.ForwardModel' = rl.SimpleForwardModel()) -> None:
        self.board_size = board_size
        self.action_points_per_turn = action_points_per_turn
        self.cards_on_deck = cards_on_deck
        self.cards_on_hand = cards_on_hand
        self.crystal_positions = crystal_positions
        self.attack_positions = [(2, 2)]
        self.speed_positions = [(0, 0), (4, 0)]
        self.forward_model = forward_model

    def __str__(self) -> str:
        return (
            f"GameParameters("
            f"board_size={self.board_size}, "
            f"action_points_per_turn={self.action_points_per_turn}, "
            f"attack_positions={self.attack_positions}, "
            f"speed_positions={self.speed_positions}, "
            f"forward_model={self.forward_model}"
            f")")