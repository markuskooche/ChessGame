from chess.figure import Figure


class Blank(Figure):
    def __init__(self, row: int, column: int):
        super().__init__(player=None, row=row, column=column, figure='blank', evaluation=0)

    def legal_moves(self, board: object) -> list[tuple]:
        return []


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


class King(Figure):
    def __init__(self, player: object, row: int, column: int):
        super().__init__(player=player, row=row, column=column, figure='king', evaluation=1)

    def legal_moves(self, board: object) -> list[tuple]:
        offsets: list[tuple] = [(0, 1), (0, -1), (1, 0), (-1, 0),
                                (1, 1), (-1, -1), (1, -1), (-1, 1)]

        # TODO: add 'castling'

        return self.offset_moves(offsets, board)


class Knight(Figure):
    def __init__(self, player: object, row: int, column: int):
        super().__init__(player=player, row=row, column=column, figure='knight', evaluation=1)

    def legal_moves(self, board: object) -> list[tuple]:
        offsets: list[tuple] = [(1, 2), (2, 1), (-1, 2), (-2, 1),
                                (1, -2), (2, -1), (-1, -2), (-2, -1)]

        return self.offset_moves(offsets, board)


class Pawn(Figure):
    def __init__(self, player: object, row: int, column: int):
        super().__init__(player=player, row=row, column=column, figure='pawn', evaluation=1)

    # TODO: if position is end 'pawn_conversion'

    def legal_moves(self, board: object) -> list[tuple]:
        positions: list[tuple] = []

        direction: int = -1 if (self.player.color == 'white') else 1
        new_position: tuple = (self.row + 1 * direction, self.column)
        if type(board.get_piece(new_position[0], new_position[1])) is Blank:
            positions.append(new_position)

        if (self.row == 1) or (self.row == 6):
            new_position: tuple = (self.row + 2 * direction, self.column)
            if type(board.get_piece(new_position[0], new_position[1])) is Blank:
                positions.append(new_position)

        # TODO: add diagonal chess move
        # TODO: add 'en passant'

        return positions


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
