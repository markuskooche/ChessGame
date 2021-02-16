import chess.figures as figure
import numpy


class Board:
    def __init__(self, players: dict):
        self.move_log = []
        self.white_move = True
        self.board = numpy.empty((8, 8), dtype=object)

        white: object = players.get('1')
        black: object = players.get('2')

        self.board[0][0] = figure.Rook(player=black, row=0, column=0)
        self.board[0][1] = figure.Knight(player=black, row=0, column=1)
        self.board[0][2] = figure.Bishop(player=black, row=0, column=2)
        self.board[0][3] = figure.Queen(player=black, row=0, column=3)
        self.board[0][4] = figure.King(player=black, row=0, column=4)
        self.board[0][5] = figure.Bishop(player=black, row=0, column=5)
        self.board[0][6] = figure.Knight(player=black, row=0, column=6)
        self.board[0][7] = figure.Rook(player=black, row=0, column=7)

        for r in range(1, 7):
            for c in range(8):
                self.board[r][c] = figure.Blank(row=r, column=c)

        for c in range(8):
            self.board[1][c] = figure.Pawn(player=black, row=1, column=c)
            self.board[6][c] = figure.Pawn(player=white, row=6, column=c)

        self.board[7][0] = figure.Rook(player=white, row=7, column=0)
        self.board[7][1] = figure.Knight(player=white, row=7, column=1)
        self.board[7][2] = figure.Bishop(player=white, row=7, column=2)
        self.board[7][3] = figure.Queen(player=white, row=7, column=3)
        self.board[7][4] = figure.King(player=white, row=7, column=4)
        self.board[7][5] = figure.Bishop(player=white, row=7, column=5)
        self.board[7][6] = figure.Knight(player=white, row=7, column=6)
        self.board[7][7] = figure.Rook(player=white, row=7, column=7)

    def get_piece(self, row: int, column: int) -> str:
        return self.board[row][column]

    def move_piece(self, move: object):
        """
        Executes the move and updates the board and the position of the figure.
        """
        self.board[move.start_row][move.start_column] = figure.Blank(move.start_row, move.start_column)
        self.board[move.end_row][move.end_column] = move.moved_piece
        move.moved_piece.set_position(move.end_row, move.end_column)
        if isinstance(move.moved_piece, figure.King):
            move.moved_piece.player.king_position = (move.end_row, move.end_column)
        if isinstance(move.moved_piece, figure.Pawn):
            move.moved_piece.initial_position = False
        self.white_move = not self.white_move
        self.move_log.append(move)

    def undo_move(self):
        """
        Undoes the move and resets the board and the position of the figure.
        """
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_column] = move.moved_piece
            self.board[move.end_row][move.end_column] = move.captured_piece
            move.moved_piece.set_position(move.start_row, move.start_column)
            if isinstance(move.moved_piece, figure.King):
                move.moved_piece.player.king_position = (move.start_row, move.start_column)
            if isinstance(move.moved_piece, figure.Pawn):
                if move.moved_piece.player.color == 'white':
                    if move.start_row == 6:
                        move.moved_piece.initial_position = True
                else:
                    if move.start_row == 1:
                        move.moved_piece.initial_position = True

            self.white_move = not self.white_move

    def print_console(self):
        for r in range(8):
            for c in range(8):
                print(self.board[r][c], end=' ')
            print()
