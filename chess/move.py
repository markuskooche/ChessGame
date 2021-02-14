class Move:
    ROW = '87654321'
    COLUMN = 'ABCDEFGH'

    def __init__(self, start_position, end_position, board):
        self.start_row = start_position[0]
        self.start_column = start_position[1]

        self.end_row = end_position[0]
        self.end_column = end_position[1]

        self.moved_piece = board.get_piece(self.start_row, self.start_column)
        self.captured_piece = board.get_piece(self.end_row, self.end_column)

    def get_notation(self) -> str:
        start = self.get_position(self.start_row, self.start_column)
        end = self.get_position(self.end_row, self.end_column)
        return start + end

    def get_position(self, row, column) -> str:
        return self.COLUMN[column] + self.ROW[row]

    def __repr__(self):
        start = self.get_position(self.start_row, self.start_column)
        end = self.get_position(self.end_row, self.end_column)
        return f'{start}->{end}'
