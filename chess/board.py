import numpy


class Board:
    def __init__(self):
        self.move_log = []
        self.white_move = True
        self.board = numpy.array([
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]
        )

    def get_piece(self, row, column) -> str:
        return self.board[row][column]

    def move_piece(self, move):
        self.board[move.start_row][move.start_column] = '--'
        self.board[move.end_row][move.end_column] = move.moved_piece
        self.white_move = not self.white_move
        self.move_log.append(move)

    def undo_move(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_column] = move.moved_piece
            self.board[move.end_row][move.end_column] = move.captured_piece
            self.white_move = not self.white_move

    def print_console(self):
        for r in range(8):
            for c in range(8):
                print(self.board[r][c], end=' ')
            print()
