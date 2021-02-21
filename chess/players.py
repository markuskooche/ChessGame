from chess.player import Player, ComputerizedPlayer
from random import choice


class HumanPlayer(Player):
    """
    A 'HumanPlayer' is controlled by a human and reacts to inputs on the board.
    It is only as smart as the human player behind it. It allows only legal moves but does not test whether a 'King'
    is in check after this move or whether a piece is pinned due to a check.
    The player behind the computer is responsible for these operations.
    """

    def __init__(self, color: str, name: str):
        super().__init__(color=color, name=name)
        self.next_move = None

    # pins are not checked at a HumanPlayer
    # the player is responsible for this himself
    def legal_moves(self, board: object) -> object:
        """
        Returns allowed moves but does not recognize chess or pinned pieces.
        """

        return self.legal_moves_simple(board)

    def best_move(self, board: object) -> object:
        if self.next_move is not None:
            return self.next_move
        else:
            return None

    def set_move(self, move: object):
        self.next_move = move


class RandomPlayer(ComputerizedPlayer):
    """
    A 'RandomPlayer' is a computerized player and inherits from 'ComputerizedPlayer'.
    It calculates a random allowed move.
    """

    def __init__(self, color: str):
        super().__init__(color=color, name='Random')

    def best_move(self, board: object) -> object:
        """
        Returns a random legal move.
        """

        move = None

        try:
            move = choice(self.legal_moves(board))
        except IndexError:
            print('There are no more figures that have legal moves!')
            # sys.exit()

        return move
