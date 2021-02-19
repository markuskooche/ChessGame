from chess.player import ComputerizedPlayer
from chess.figure import Figure
from chess.move import Move


class Blank(Figure):
    def __init__(self, row: int, column: int):
        super().__init__(player=None, row=row, column=column, figure='blank', evaluation=0)

    def legal_moves(self, board: object, pins=()) -> list[object]:
        return []

    def __repr__(self) -> str:
        return '-'


class Bishop(Figure):
    def __init__(self, player: object, row: int, column: int):
        super().__init__(player=player, row=row, column=column, figure='bishop', evaluation=3)

    def legal_moves(self, board: object, pins: list = ()) -> list[object]:
        unprepared_directions: list[tuple] = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
        moves: list[object] = []

        # revision of directions is only important for 'ComputerizedPlayer'
        directions = self.prepare_directions(unprepared_directions, pins)

        for direction in directions:
            moves += [i for i in self.iterative_moves(direction, board)]

        return moves

    def __repr__(self) -> str:
        return 'B' if self.player.color[0] == 'w' else 'b'


class King(Figure):
    def __init__(self, player: object, row: int, column: int):
        super().__init__(player=player, row=row, column=column, figure='king', evaluation=9)

    def is_check(self, board: object) -> bool:
        return self.__square_under_attack(row=self.row, column=self.column, board=board)

    def __square_under_attack(self, row: int, column: int, board: object) -> bool:
        opponent_figures: list[object] = self.player.opponent.get_figures(board)
        opponent_moves: list[object] = []

        for opponent_figure in opponent_figures:
            # between two ComputerizedPlayers required to avoid
            #  'RecursionError: maximum recursion depth exceeded in comparison'
            if not isinstance(opponent_figure, King):
                opponent_moves += [i for i in opponent_figure.legal_moves(board)]

        for opponent_move in opponent_moves:
            if (opponent_move.end_row == row) and (opponent_move.end_column == column):
                return True

        return False

    def legal_moves(self, board: object, pins: list = ()) -> list[object]:
        offsets: list[tuple] = [(-1, 0), (0, 1), (1, 0), (0, -1), (-1, -1), (-1, 1), (1, 1), (1, -1)]

        # TODO: add 'castling'

        positions: list[object] = []

        for (row_off, column_off) in offsets:
            new_column: int = self.column + column_off
            new_row: int = self.row + row_off

            if (new_row in range(0, 8)) and (new_column in range(0, 8)):
                figure = board.get_piece(row=new_row, column=new_column)
                if figure.player is not self.player:
                    move = Move((self.row, self.column), (new_row, new_column), board)
                    if isinstance(self.player, ComputerizedPlayer):
                        board.move_piece(move)

                        if not self.__square_under_attack(move.end_row, move.end_column, board):
                            positions.append(move)
                        board.undo_move()
                    else:
                        positions.append(move)

        # TODO: add 'checked moves by king'
        """
        for (row_off, column_off) in offsets:
            offset_column = self.column + 2 * row_off
            offset_row = self.row + 2 * column_off

            if (offset_row in range(0, 8)) and (offset_column in range(0, 8)):
                figure = board.get_piece(offset_row, offset_column)
                if isinstance(figure, King):
                    print('NOT ALLOWED:', offset_row, offset_column)
        """

        return positions

    def __repr__(self) -> str:
        return 'K' if self.player.color[0] == 'w' else 'k'


class Knight(Figure):
    def __init__(self, player: object, row: int, column: int):
        super().__init__(player=player, row=row, column=column, figure='knight', evaluation=3)

    def legal_moves(self, board: object, pins: list = ()) -> list[object]:
        offsets: list[tuple] = [(-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1)]
        moves: list[object] = []

        for pin in pins:
            # if the position of the knight is a pin, there are no valid moves
            if (self.row == pin[0]) and (self.column == pin[1]):
                return []

        for (row_off, column_off) in offsets:
            new_column: int = self.column + column_off
            new_row: int = self.row + row_off

            if (new_row in range(0, 8)) and (new_column in range(0, 8)):
                figure = board.get_piece(row=new_row, column=new_column)
                if figure.player is not self.player:
                    moves.append(Move((self.row, self.column), (new_row, new_column), board))

        return moves

    def __repr__(self) -> str:
        return 'N' if self.player.color[0] == 'w' else 'n'


class Pawn(Figure):
    def __init__(self, player: object, row: int, column: int):
        super().__init__(player=player, row=row, column=column, figure='pawn', evaluation=1)
        self.initial_position: bool = True

    # TODO: add 'pawn_conversion'
    # TODO: add 'en passant'

    def legal_moves(self, board: object, pins: list = ()) -> list[object]:
        direction: int = -1 if (self.player.color == 'white') else 1
        new_position: tuple = (self.row + direction, self.column)
        moves: list[object] = []

        pinning_direction: tuple = (direction, 0)
        pinned_direction: tuple = ()
        pinned: bool = False

        if len(pins) != 0:
            for pin in pins:
                if (self.row == pin[0]) and (self.column == pin[1]):
                    pinned_direction = (pin[2], pin[3])
                    pinned = True
                    break

        if new_position[0] in range(0, 8):
            figure = board.get_piece(new_position[0], new_position[1])
            if isinstance(figure, Blank):
                # pinned is only significant for ComputerizedPlayer
                if (not pinned) or (pinned_direction == pinning_direction):
                    moves.append(Move((self.row, self.column), new_position, board))

                    # if pawn is on starting position and there is no opponent in front of him
                    if ((self.row == 6) and (direction == -1)) or ((self.row == 1) and (direction == 1)):
                        new_position: tuple = (self.row + (2 * direction), self.column)
                        if type(board.get_piece(new_position[0], new_position[1])) is Blank:
                            moves.append(Move((self.row, self.column), new_position, board))

        # a pawn captures diagonally forward one square to the left or right
        offsets: list[tuple] = [(direction, -1), (direction, 1)]

        for (row_off, column_off) in offsets:
            new_column: int = self.column + column_off
            new_row: int = self.row + row_off

            if (new_row in range(0, 8)) and (new_column in range(0, 8)):
                figure = board.get_piece(row=new_row, column=new_column)

                # if pawn is a pinned piece it is only allowed to capture vertically checking pieces
                if (figure.player is not self.player) and (type(figure) != Blank):
                    capture_pinning = False

                    if pinned:
                        # if the pawn can capture the checking piece, it is a legal move
                        capturing_column = self.column + pinned_direction[1]
                        capturing_row = self.row + pinned_direction[0]
                        capture_pinning = (capturing_row == new_row) and (capturing_column == new_column)

                    if (not pinned) or (pinned_direction == pinning_direction) or capture_pinning:
                        moves.append(Move((self.row, self.column), (new_row, new_column), board))

        return moves

    def __repr__(self) -> str:
        return 'P' if self.player.color[0] == 'w' else 'p'


class Queen(Figure):
    def __init__(self, player: object, row: int, column: int):
        super().__init__(player=player, row=row, column=column, figure='queen', evaluation=10)

    def legal_moves(self, board: object, pins: list = ()) -> list[object]:
        unprepared_directions: list[tuple] = [(1, 0), (0, 1), (-1, 0), (0, -1),
                                              (1, 1), (-1, -1), (-1, 1), (1, -1)]
        moves: list[object] = []

        # revision of directions is only important for 'ComputerizedPlayer'
        directions = self.prepare_directions(unprepared_directions, pins)

        for direction in directions:
            moves += [i for i in self.iterative_moves(direction, board)]

        return moves

    def __repr__(self) -> str:
        return 'Q' if self.player.color[0] == 'w' else 'q'


class Rook(Figure):
    def __init__(self, player: object, row: int, column: int):
        super().__init__(player=player, row=row, column=column, figure='rook', evaluation=5)

    def legal_moves(self, board: object, pins: list = ()) -> list[object]:
        unprepared_directions: list[tuple] = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        moves: list[object] = []

        # revision of directions is only important for 'ComputerizedPlayer'
        directions = self.prepare_directions(unprepared_directions, pins)

        for direction in directions:
            moves += [i for i in self.iterative_moves(direction, board)]

        return moves

    def __repr__(self) -> str:
        return 'R' if self.player.color[0] == 'w' else 'r'
