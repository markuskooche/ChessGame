from chess.player import Player, ComputerizedPlayer
from random import choice
import sys


class HumanPlayer(Player):
    def __init__(self, color: str, name: str):
        super().__init__(color=color, name=name)


class RandomPlayer(ComputerizedPlayer):
    def __init__(self, color: str):
        super().__init__(color=color, name='RandomPlayer')

    def best_move(self, board: object) -> object:
        try:
            move = choice(self.legal_moves(board))
        except IndexError:
            print('There are no more figures that have legal moves!')
            sys.exit()

        return move
