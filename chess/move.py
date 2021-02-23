import chess.pieces as p


class Move:
    """
    The Move class generates valid moves.
    """

    def __init__(self, start: tuple, end: tuple, board: object, en_passant: bool = False, castle_move: bool = False):
        # the current position of the piece
        self.start_row = start[0]
        self.start_column = start[1]

        # where the piece may move
        self.end_row = end[0]
        self.end_column = end[1]

        self.moved_piece = board.get_piece(self.start_row, self.start_column)
        self.captured_piece = board.get_piece(self.end_row, self.end_column)

        self.castle_move = castle_move

        self.is_pawn_promotion = False
        self.is_en_passant = en_passant

        # recognizes a pawn promotion move
        if isinstance(self.moved_piece, p.Pawn):
            color = self.moved_piece.player.color
            if (color == 'white' and self.end_row == 0) or (color == 'black' and self.end_row == 7):
                self.is_pawn_promotion = True

    def code(self) -> str:
        """
        Creates a code to compare two movements with each other.
        """

        start = Move.get_position(self.start_row, self.start_column)
        end = Move.get_position(self.end_row, self.end_column)
        return f'{start}{end}'

    @staticmethod
    def get_position(row: int, column: int) -> str:
        """
        Returns the position in the chess notation.
        """

        return 'abcdefgh'[column] + '87654321'[row]

    def __repr__(self):
        return self.code()
