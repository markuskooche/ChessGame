from abc import ABC, abstractmethod
from chess.figures import Blank, King
import base64
import sys
import os


COLORS: list[str] = ['white', 'black']


class Player(ABC):
    def __init__(self, color: str, name: str):
        self.code = base64.b32encode(os.urandom(4))[:6].decode('UTF-8')
        self.opponent: object = None
        self.name = name
        if color not in COLORS:
            raise Exception(f"Player color must be in {COLORS} but color is '{color}'")
        else:
            if color == 'white':
                self.king_position = (7, 4)
            else:
                self.king_position = (0, 4)
            self.color = color

    def set_opponent(self, board):
        if self.opponent is None:
            for r in range(8):
                for c in range(8):
                    possible_opponent: object = board.get_piece(row=r, column=c)
                    if not isinstance(possible_opponent, Blank):
                        if possible_opponent.player.code != self.code:
                            self.opponent = possible_opponent.player
                            break

            if self.opponent is None:
                raise Exception('It is not possible to set the player!')

    def get_figures(self, board: object) -> list[object]:
        figures: list[object] = []

        for r in range(8):
            for c in range(8):
                figure = board.get_piece(row=r, column=c)
                if not isinstance(figure, Blank):
                    if figure.player.code == self.code:
                        figures.append(figure)

        return figures

    # This allows the HumanPlayer to move pieces that protect the king
    def legal_moves_simple(self, board) -> list[object]:
        moves: list[object] = []

        for figure in self.get_figures(board):
            for move in figure.legal_moves(board):
                if move is not []:
                    moves.append(move)

        return moves

    @abstractmethod
    def legal_moves(self, board: object) -> object:
        pass


class ComputerizedPlayer(Player, ABC):
    def __init__(self, color: str, name: str):
        super().__init__(color=color, name=name)

    def is_check(self, board: object) -> bool:
        return self.__square_under_attack(row=self.king_position[0], column=self.king_position[1], board=board)

    def __square_under_attack(self, row: int, column: int, board: object) -> bool:
        opponent_figures: list[object] = self.opponent.get_figures(board)
        opponent_moves: list[object] = []

        for opponent_figure in opponent_figures:
            if not isinstance(opponent_figure, King):
                opponent_moves += [i for i in opponent_figure.legal_moves(board)]

        for opponent_move in opponent_moves:
            if (opponent_move.end_row == row) and (opponent_move.end_column == column):
                return True

        return False

    # This algorithm detects protective pieces and removes his moves
    def legal_moves(self, board: object) -> list[object]:
        own_moves: list[object] = self.legal_moves_simple(board)

        for i in range((len(own_moves) - 1), -1, -1):
            board.move_piece(own_moves[i])

            if self.is_check(board):
                own_moves.remove(own_moves[i])
            board.undo_move()

        if len(own_moves) == 0:
            if self.is_check(board):
                print('CHECKMATE')
            else:
                print('STALEMATE')
            sys.exit()

        return own_moves

    @abstractmethod
    def best_move(self, board: object) -> object:
        pass
