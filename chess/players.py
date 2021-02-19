from chess.player import Player, ComputerizedPlayer
from random import choice
import sys


class HumanPlayer(Player):
    def __init__(self, color: str, name: str):
        super().__init__(color=color, name=name)

    # pins are not checked at a HumanPlayer
    # the player is responsible for this himself
    def legal_moves(self, board: object) -> object:
        return self.legal_moves_simple(board)


class RandomPlayer(ComputerizedPlayer):
    def __init__(self, color: str):
        super().__init__(color=color, name='Random')

    def best_move(self, board: object) -> object:
        try:
            move = choice(self.legal_moves(board))
        except IndexError:
            print('There are no more figures that have legal moves!')
            sys.exit()

        return move
