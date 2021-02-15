from chess.figure import Figure


class Blank(Figure):
    def __init__(self, row: int, column: int):
        super().__init__(player=None, row=row, column=column, figure='blank', evaluation=0)

    def legal_moves(self, board: object) -> list[tuple]:
        return []

    def __repr__(self) -> str:
        return '-'


class Bishop(Figure):
    def __init__(self, player: object, row: int, column: int):
        super().__init__(player=player, row=row, column=column, figure='bishop', evaluation=1)

    def legal_moves(self, board: object) -> list[tuple]:
        positions: list[tuple] = []

        positions += [i for i in self.iterative_moves(1, 1, board)]
        positions += [i for i in self.iterative_moves(-1, -1, board)]
        positions += [i for i in self.iterative_moves(1, -1, board)]
        positions += [i for i in self.iterative_moves(-1, 1, board)]

        return positions

    def __repr__(self) -> str:
        return 'B' if self.player.color[0] == 'w' else 'b'


class King(Figure):
    def __init__(self, player: object, row: int, column: int):
        super().__init__(player=player, row=row, column=column, figure='king', evaluation=1)

    def legal_moves(self, board: object) -> list[tuple]:
        offsets: list[tuple] = [(0, 1), (0, -1), (1, 0), (-1, 0),
                                (1, 1), (-1, -1), (1, -1), (-1, 1)]

        # TODO: add 'castling'

        return self.offset_moves(offsets, board)

    def __repr__(self) -> str:
        return 'K' if self.player.color[0] == 'w' else 'k'


class Knight(Figure):
    def __init__(self, player: object, row: int, column: int):
        super().__init__(player=player, row=row, column=column, figure='knight', evaluation=1)

    def legal_moves(self, board: object) -> list[tuple]:
        offsets: list[tuple] = [(1, 2), (2, 1), (-1, 2), (-2, 1),
                                (1, -2), (2, -1), (-1, -2), (-2, -1)]

        return self.offset_moves(offsets, board)

    def __repr__(self) -> str:
        return 'N' if self.player.color[0] == 'w' else 'n'


class Pawn(Figure):
    def __init__(self, player: object, row: int, column: int):
        super().__init__(player=player, row=row, column=column, figure='pawn', evaluation=1)
        self.initial_position: bool = True

    # TODO: if position is end 'pawn_conversion'

    def legal_moves(self, board: object) -> list[tuple]:
        positions: list[tuple] = []

        direction: int = -1 if (self.player.color == 'white') else 1
        new_position: tuple = (self.row + 1 * direction, self.column)
        if new_position[0] in range(0, 8):
            if type(board.get_piece(new_position[0], new_position[1])) is Blank:
                positions.append(new_position)

            # If pawn is on starting position and there is no opponent in front of him
            if self.initial_position and ((self.row == 1) or (self.row == 6)):
                new_position: tuple = (self.row + 2 * direction, self.column)
                if type(board.get_piece(new_position[0], new_position[1])) is Blank:
                    positions.append(new_position)

        offsets: list[tuple] = [(direction, -1), (direction, 1)]

        for (row_off, column_off) in offsets:
            new_column: int = self.column + column_off
            new_row: int = self.row + row_off

            if (new_row in range(0, 8)) and (new_column in range(0, 8)):
                figure = board.get_piece(row=new_row, column=new_column)
                if (figure.player is not self.player) and (type(figure) != Blank):
                    positions.append((new_row, new_column))

        # TODO: add 'en passant'

        self.initial_position = False
        return positions

    def __repr__(self) -> str:
        return 'P' if self.player.color[0] == 'w' else 'p'


class Queen(Figure):
    def __init__(self, player: object, row: int, column: int):
        super().__init__(player=player, row=row, column=column, figure='queen', evaluation=1)

    def legal_moves(self, board: object) -> list[tuple]:
        positions: list[tuple] = []

        positions += [i for i in self.iterative_moves(1, 1, board)]
        positions += [i for i in self.iterative_moves(-1, -1, board)]
        positions += [i for i in self.iterative_moves(-1, 1, board)]
        positions += [i for i in self.iterative_moves(1, -1, board)]

        positions += [i for i in self.iterative_moves(1, 0, board)]
        positions += [i for i in self.iterative_moves(-1, 0, board)]
        positions += [i for i in self.iterative_moves(0, 1, board)]
        positions += [i for i in self.iterative_moves(0, -1, board)]

        return positions

    def __repr__(self) -> str:
        return 'Q' if self.player.color[0] == 'w' else 'q'


class Rook(Figure):
    def __init__(self, player: object, row: int, column: int):
        super().__init__(player=player, row=row, column=column, figure='rook', evaluation=1)

    def legal_moves(self, board: object) -> list[tuple]:
        positions: list[tuple] = []

        positions += [i for i in self.iterative_moves(1, 0, board)]
        positions += [i for i in self.iterative_moves(-1, 0, board)]
        positions += [i for i in self.iterative_moves(0, 1, board)]
        positions += [i for i in self.iterative_moves(0, -1, board)]

        return positions

    def __repr__(self) -> str:
        return 'R' if self.player.color[0] == 'w' else 'r'
