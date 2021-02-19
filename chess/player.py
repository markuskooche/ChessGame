from abc import ABC, abstractmethod
import chess.figures as figure
import base64
import sys
import os

COLORS: list[str] = ['white', 'black']


class Player(ABC):
    def __init__(self, color: str, name: str):
        self.code = base64.b32encode(os.urandom(4))[:6].decode('UTF-8')
        self.opponent: object = None
        self.name = name
        self.color = color
        if color not in COLORS:
            raise Exception(f"Player color must be in {COLORS} but color is '{color}'")
        else:
            if color == 'white':
                self.king_position = (7, 4)
            elif color == 'black':
                self.king_position = (0, 4)

    def set_opponent(self, board):
        if self.opponent is None:
            for r in range(8):
                for c in range(8):
                    possible_opponent: object = board.get_piece(row=r, column=c)
                    if not isinstance(possible_opponent, figure.Blank):
                        if possible_opponent.player.code != self.code:
                            self.opponent = possible_opponent.player
                            break

            if self.opponent is None:
                raise Exception('It is not possible to set the player!')

    def get_figures(self, board: object) -> list[object]:
        pieces: list[object] = []

        for r in range(8):
            for c in range(8):
                piece = board.get_piece(row=r, column=c)
                if not isinstance(piece, figure.Blank):
                    if piece.player.code == self.code:
                        pieces.append(piece)

        return pieces

    # this allows the 'HumanPlayer' to move pieces that protect the king
    def legal_moves_simple(self, board: object, pins: list = ()) -> list[object]:
        moves: list[object] = []

        for piece in self.get_figures(board):
            for move in piece.legal_moves(board, pins):
                if move is not []:
                    moves.append(move)

        return moves

    @abstractmethod
    def legal_moves(self, board: object) -> object:
        pass


class ComputerizedPlayer(Player, ABC):
    def __init__(self, color: str, name: str):
        super().__init__(color=color, name=name)
        self.in_check = False
        self.checks = []
        self.pins = []

    def legal_moves(self, board: object) -> list[object]:
        self.update_pins_and_checks(board)
        valid_moves: list[object] = self.legal_moves_simple(board=board, pins=self.pins)

        king_column = self.king_position[1]
        king_row = self.king_position[0]
        king = board.get_piece(king_row, king_column)

        if self.in_check:
            # if it's in one check
            if len(self.checks) == 1:
                check = self.checks[0]
                check_row = check[0]
                check_column = check[1]

                piece_checking = board.get_piece(check_row, check_column)
                valid_squares = []

                if isinstance(piece_checking, figure.Knight):
                    # if it's a knight, king must move or other piece must capture knight
                    valid_squares = [(check_row, check_column)]
                else:
                    # allows moves to any square between the king and the attacking piece
                    for i in range(1, 8):
                        valid_column = self.king_position[1] + (i * check[3])
                        valid_row = self.king_position[0] + (i * check[2])
                        valid_squares.append((valid_row, valid_column))

                        if (valid_row == check_row) and (valid_column == check_column):
                            break

                # get rid of any moves that do not block check or move king
                for i in range((len(valid_moves) - 1), -1, -1):
                    piece_type = valid_moves[i].moved_piece

                    # if the checking piece is a king do not delete this move
                    if not isinstance(piece_type, figure.King):
                        if not (valid_moves[i].end_row, valid_moves[i].end_column) in valid_squares:
                            valid_moves.remove(valid_moves[i])

            # if it's in double check, king has to move
            else:
                valid_moves = king.legal_moves(board)

        if len(valid_moves) == 0:
            if self.in_check:
                print('CHECKMATE')
            else:
                print('STALEMATE')

            board.print_console()
            sys.exit()

        return valid_moves

    def update_pins_and_checks(self, board: object):
        # [4] [0] [5]   -> the numbers represents the values in the array
        # [3]  K  [1]   -> [0] to [3] inclusive represents orthogonally moves
        # [7] [2] [6]   -> [4] to [7] inclusive represents diagonally moves
        king_offsets: list[tuple] = [(-1, 0), (0, 1), (1, 0), (0, -1), (-1, -1), (-1, 1), (1, 1), (1, -1)]

        # resets the check controlling
        self.in_check = False
        self.checks = []
        self.pins = []

        for j in range(len(king_offsets)):
            king_offset = king_offsets[j]
            possible_pin = ()

            # starts at 1 because 0 would not change the position of the king
            for i in range(1, 8):
                end_column = self.king_position[1] + (i * king_offset[1])
                end_row = self.king_position[0] + (i * king_offset[0])

                # checks if the moves are on the board
                if (end_row in range(0, 8)) and (end_column in range(0, 8)):
                    end_piece = board.get_piece(end_row, end_column)

                    if not isinstance(end_piece, figure.Blank):
                        # own pieces must be tested for 'pins'
                        if end_piece.player.code == self.code:
                            if possible_pin == ():
                                possible_pin = (end_row, end_column, king_offset[0], king_offset[1])
                            else:
                                break

                        # opponent's pieces must be tested for 'checks'
                        elif end_piece.player != self.code:
                            # THERE ARE FIVE CONDITIONS TO CONTROL
                            # 1.) orthogonally away from king and piece is a rook
                            cond_rook = (j in range(0, 4) and isinstance(end_piece, figure.Rook))

                            # 2.) diagonally away from king and piece is a bishop
                            cond_bishop = (j in range(4, 8) and isinstance(end_piece, figure.Bishop))

                            # 3.) one square away diagonally from king and piece is a pawn
                            cond_pawn = (i == 1 and (isinstance(end_piece, figure.Pawn)) and
                                         ((self.opponent.color == 'white' and j in range(6, 8)) or
                                          (self.opponent.color == 'black' and j in range(4, 6))))

                            # 4.) any direction and piece is a queen
                            cond_queen = isinstance(end_piece, figure.Queen)

                            # 5.) any direction one square away and piece is a king
                            cond_king = (i == 1 and isinstance(end_piece, figure.King))

                            if cond_rook or cond_bishop or cond_pawn or cond_queen or cond_king:
                                if possible_pin == ():
                                    self.in_check = True
                                    self.checks.append((end_row, end_column, king_offset[0], king_offset[1]))
                                    break
                                else:
                                    self.pins.append(possible_pin)
                                    break
                            else:
                                break

        # knight offsets listed clockwise starting at 1 o'clock
        #  -  [7]  -  [0]  -
        # [6]  -   -   -  [1]
        #  -   -   N   -   -
        # [5]  -   -   -  [2]
        #  -  [4]  -  [3]  -
        knight_offsets: list[tuple] = [(-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1)]

        # the opponent's knight moves must be tested for 'checks'
        for knight_offset in knight_offsets:
            end_column = self.king_position[1] + knight_offset[1]
            end_row = self.king_position[0] + knight_offset[0]

            if (end_row in range(0, 8)) and (end_column in range(0, 8)):
                end_piece = board.get_piece(end_row, end_column)

                if not isinstance(end_piece, figure.Blank):
                    if (end_piece.player.code != self.code) and (isinstance(end_piece, figure.Knight)):
                        self.checks.append((end_row, end_column, knight_offset[0], knight_offset[1]))
                        self.in_check = True

    @abstractmethod
    def best_move(self, board: object) -> object:
        pass
