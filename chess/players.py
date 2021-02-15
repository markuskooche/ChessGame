from chess.player import Player, ComputerizedPlayer
from chess.figures import Blank
from chess.move import Move
from random import choice


class HumanPlayer(Player):
    def __init__(self, color: str, name: str):
        super().__init__(color=color, name=name)


class RandomPlayer(ComputerizedPlayer):
    def __init__(self, color: str):
        super().__init__(color=color, name='RandomPlayer')

    def best_move(self, board: object) -> object:
        figures: list[object] = []

        for r in range(8):
            for c in range(8):
                actual_figure = board.get_piece(r, c)
                if type(actual_figure) != Blank:
                    # TODO: name is not possible by Computer vs. Computer
                    if actual_figure.player.name == self.name:
                        if len(actual_figure.legal_moves(board)) != 0:
                            figures.append(actual_figure)

        figure = choice(figures)
        start_position = (figure.row, figure.column)
        end_position = choice(figure.legal_moves(board))

        return Move(start_position, end_position, board)
