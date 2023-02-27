from start.start_game import start_game

if __name__ == "__main__":
    game, players, budget = start_game()
    game.run(players[0], players[1], budget, True, False)