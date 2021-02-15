from chess.player import Player


class HumanPlayer(Player):
    def __init__(self, color: str, name: str):
        super().__init__(color=color, name=name)
