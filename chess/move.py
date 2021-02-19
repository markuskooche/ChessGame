class Move:
    def __init__(self, start_position: tuple, end_position: tuple, board: object):
        self.start_row = start_position[0]
        self.start_column = start_position[1]

        self.end_row = end_position[0]
        self.end_column = end_position[1]

        self.moved_piece = board.get_piece(self.start_row, self.start_column)
        self.captured_piece = board.get_piece(self.end_row, self.end_column)

    def code(self) -> str:
        start = Move.get_position(self.start_row, self.start_column)
        end = Move.get_position(self.end_row, self.end_column)
        return f'{start}{end}'

    @staticmethod
    def get_position(row: int, column: int) -> str:
        return 'abcdefgh'[column] + '87654321'[row]

    def __repr__(self):
        return self.code()
