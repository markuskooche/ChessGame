from chess.player import ComputerizedPlayer
from chess.piece import Piece
from chess.move import Move


class Blank(Piece):
    """
    An empty spot is represented by a 'Blank' piece.
    """

    def __init__(self, row: int, column: int):
        super().__init__(player=None, row=row, column=column, name='blank', evaluation=0)

    def legal_moves(self, board: object, pins=()) -> list[object]:
        """
        A 'Blank' piece has no legal moves.
        """

        return []

    def __repr__(self) -> str:
        return '-'


class Bishop(Piece):
    """
    A 'Bishop' moves any distance in all diagonal directions.\n
    The bishop always remains on squares of the same color during a game. That is why each player has a white-squared
    bishop and a black-squared bishop at the beginning. Both together (the bishop pair) can be a particularly great
    power, as they complement each other well and can dominate the whole board.
    """

    def __init__(self, player: object, row: int, column: int):
        super().__init__(player=player, row=row, column=column, name='bishop', evaluation=3)

    def legal_moves(self, board: object, pins: list = ()) -> list[object]:
        """
        Creates all legal moves.

        :param board: The current chessboard.
        :param pins: A list of pinned spots.
        :return: A list of all legal moves.
        """

        unprepared_directions: list[tuple] = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
        moves: list[object] = []

        # revision of directions is only important for 'ComputerizedPlayer'
        directions = self.prepare_directions(unprepared_directions, pins)

        for direction in directions:
            moves += [i for i in self.iterative_moves(direction, board)]

        return moves

    def __repr__(self) -> str:
        return 'B' if self.player.color[0] == 'w' else 'b'


class King(Piece):
    """
    He may only move one square at a time from his location, in any direction.\n
    He is the most important piece in chess. Capturing him is the goal of the game. However, he is by no means the
    strongest piece in combat, and especially as long as there are many other pieces on the board, he must usually
    stand well guarded in a safe place.

    CASTLING\n
    1. The king and the rook involved must not have moved yet. Even if the king or rook has moved, but later returns
       to its starting squares, castling is no longer possible. If only one rook has moved, but not the king, the
       king may still castling with the other rook.
    2. The squares between the king and the rook must be free.
    3. The king must not be under attack. If only the rook to be castled is threatened, castling is allowed.
    4. The square to which the king moves, and also the square it crosses, must not be threatened.
    """

    def __init__(self, player: object, row: int, column: int):
        super().__init__(player=player, row=row, column=column, name='king', evaluation=0)

    def is_check(self, board: object) -> bool:
        """
        Returns true or false whether the king is in check.
        """

        return self.__square_under_attack(self.row, self.column, board)

    def __square_under_attack(self, row: int, column: int, board: object) -> bool:
        """
        A private method which returns true or false whether a square is attachable by an enemy piece.\n
        This method is only callable inside of a 'King' object.
        """

        enemy_pieces: list[object] = self.player.enemy.get_pieces(board)
        enemy_moves: list[object] = []

        for enemy_piece in enemy_pieces:
            # between two ComputerizedPlayers required to avoid
            #  'RecursionError: maximum recursion depth exceeded in comparison'
            if not isinstance(enemy_piece, King):
                enemy_moves += [i for i in enemy_piece.legal_moves(board)]

        for enemy_move in enemy_moves:
            if (enemy_move.end_row == row) and (enemy_move.end_column == column):
                return True

        return False

    def legal_moves(self, board: object, pins: list = ()) -> list[object]:
        """
        Creates all legal moves.

        :param board: The current chessboard.
        :param pins: A list of pinned spots.
        :return: A list of all legal moves.
        """

        offsets: list[tuple] = [(-1, 0), (0, 1), (1, 0), (0, -1), (-1, -1), (-1, 1), (1, 1), (1, -1)]
        moves: list[object] = []

        for (row_off, column_off) in offsets:
            new_column: int = self.column + column_off
            new_row: int = self.row + row_off

            if (new_row in range(0, 8)) and (new_column in range(0, 8)):
                piece = board.get_piece(row=new_row, column=new_column)
                if piece.player is not self.player:
                    move = Move(self.position(), (new_row, new_column), board)

                    # a ComputerizedPlayer must check if a move ends in check
                    if isinstance(self.player, ComputerizedPlayer):
                        board.move_piece(move)

                        if not self.__square_under_attack(move.end_row, move.end_column, board):
                            moves.append(move)
                        board.undo_move()

                    # a HumanPlayer has to do it itself
                    else:
                        moves.append(move)

        # remove moves that the enemy's king can also reach
        enemy_king = self.player.enemy.king_position
        for (row_off, column_off) in offsets:
            enemy_column = enemy_king[1] + column_off
            enemy_row = enemy_king[0] + row_off

            if (enemy_row in range(0, 8)) and (enemy_column in range(0, 8)):
                for i in range((len(moves) - 1), -1, -1):
                    move = moves[i]

                    if (enemy_row == move.end_row) and (enemy_column == move.end_column):
                        moves.remove(move)

        queen_side_castling = False
        king_side_castling = False

        # check if castling is allowed
        if self.player.color == 'white':
            # [-1] returns the last castling log
            queen_side_castling = board.castling_log[-1][0]
            king_side_castling = board.castling_log[-1][1]
        elif self.player.color == 'black':
            # [-1] returns the last castling log
            queen_side_castling = board.castling_log[-1][2]
            king_side_castling = board.castling_log[-1][3]

        if queen_side_castling:
            # check if all spots are blank
            if isinstance(board.get_piece(self.row, (self.column - 1)), Blank) and \
                    isinstance(board.get_piece(self.row, (self.column - 2)), Blank) and \
                    isinstance(board.get_piece(self.row, (self.column - 3)), Blank):
                # check if the spots are not under attack
                if not self.__square_under_attack(self.row, self.column, board) and \
                        not self.__square_under_attack(self.row, (self.column - 1), board) and \
                        not self.__square_under_attack(self.row, (self.column - 2), board):
                    moves.append(Move((self.row, self. column), (self.row, (self.column - 2)), board, castle_move=True))

        if king_side_castling:
            # check if all spots are blank
            if isinstance(board.get_piece(self.row, (self.column + 1)), Blank) and \
                    isinstance(board.get_piece(self.row, (self.column + 2)), Blank):
                # check if the spots are not under attack
                if not self.__square_under_attack(self.row, self.column, board) and \
                        not self.__square_under_attack(self.row, (self.column + 1), board) and \
                        not self.__square_under_attack(self.row, (self.column + 2), board):
                    moves.append(Move(self.position(), (self.row, (self.column + 2)), board, castle_move=True))

        return moves

    def __repr__(self) -> str:
        return 'K' if self.player.color[0] == 'w' else 'k'


class Knight(Piece):
    """
    Learning its gait is usually the most difficult because it makes such "crooked" jumps.
    In the diagram, the squares to which the knight can move are marked with X.\n
     - X - X -  \n
     X - - - X  \n
     - - N - -  \n
     X - - - X  \n
     - X - X -  \n
    The 'Knight' is the only piece that can jump over others!
    The 'Knight' moves to exactly those squares, which the 'Queen' cannot reach from the starting square.
    'Queen' and 'Knight' therefore often form a good complement.
    """

    # The upper diagram is for documentation purposes only.
    # Here the diagram can be viewed better.
    # - X - X -
    # X - - - X
    # - - N - -
    # X - - - X
    # - X - X -

    def __init__(self, player: object, row: int, column: int):
        super().__init__(player=player, row=row, column=column, name='knight', evaluation=3)

    def legal_moves(self, board: object, pins: list = ()) -> list[object]:
        """
        Creates all legal moves.

        :param board: The current chessboard.
        :param pins: A list of pinned spots.
        :return: A list of all legal moves.
        """
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
                piece = board.get_piece(row=new_row, column=new_column)
                if piece.player is not self.player:
                    moves.append(Move(self.position(), (new_row, new_column), board))

        return moves

    def __repr__(self) -> str:
        return 'N' if self.player.color[0] == 'w' else 'n'


class Pawn(Piece):
    """
    He is the weakest chess piece, but his move still has a few peculiarities.
    One square moves straight forward (never back). From its basic position, it may also move forward two squares.
    You have the choice of moving forward only one square or two. A double move may not be made up later.\n
    The 'Pawn' moves differently than it moves, namely one square forward diagonally to the right or left.\n

    1. PAWN PROMOTION
        When the 'Pawn' reaches the other edge of the board, it turns into another piece of the same color.
        You have the choice between 'Queen', 'Rook', 'Bishop' or 'Knight'. In almost all cases, of course, the 'Queen'
        is chosen as the strongest piece, but there are rare exceptions where the 'Knight' transformation is better,
        because the 'Knight' can reach other squares than the queen.\n

    2. EN PASSANT
        To prevent cheating past, the capture en passant was introduced in France (French: in passing).
        If a 'Pawn' is next to an enemy's 'Pawn' after the double step,
        the enemy can capture it as if it had gone forward only one square.
    """

    def __init__(self, player: object, row: int, column: int):
        super().__init__(player=player, row=row, column=column, name='pawn', evaluation=1)
        self.initial_position: bool = True

    def legal_moves(self, board: object, pins: list = ()) -> list[object]:
        """
        Creates all legal moves.

        :param board: The current chessboard.
        :param pins: A list of pinned spots.
        :return: A list of all legal moves.
        """
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
            piece = board.get_piece(new_position[0], new_position[1])
            if isinstance(piece, Blank):
                # pinned is only significant for ComputerizedPlayer
                if (not pinned) or (pinned_direction == pinning_direction):
                    moves.append(Move(self.position(), new_position, board))

                    # if pawn is on starting position and there is no enemy in front of him
                    if ((self.row == 6) and (direction == -1)) or ((self.row == 1) and (direction == 1)):
                        new_position: tuple = (self.row + (2 * direction), self.column)
                        if type(board.get_piece(new_position[0], new_position[1])) is Blank:
                            moves.append(Move(self.position(), new_position, board))

        # a pawn captures diagonally forward one square to the left or right
        offsets: list[tuple] = [(direction, -1), (direction, 1)]

        for (row_off, column_off) in offsets:
            new_column: int = self.column + column_off
            new_row: int = self.row + row_off

            end: tuple[int, int] = (new_row, new_column)

            if (new_row in range(0, 8)) and (new_column in range(0, 8)):
                piece = board.get_piece(row=new_row, column=new_column)

                # if pawn is a pinned piece it is only allowed to capture vertically checking pieces
                if piece.player is not self.player:
                    if type(piece) != Blank:
                        # TODO: I think i should disable en passant here completely
                        if pinned:
                            # if the pawn can capture the checking piece, it is a legal move
                            capturing_column = self.column + pinned_direction[1]
                            capturing_row = self.row + pinned_direction[0]

                            if (capturing_row == new_row) and (capturing_column == new_column):
                                moves.append(Move(self.position(), end, board))
                        elif not pinned:
                            moves.append(Move(self.position(), end, board))
                    else:
                        # if a pawn is not pinned and the enemy pawn is able to capture because of en passant
                        if (not pinned) and (self.player.enemy.en_passant == end):
                            moves.append(Move(self.position(), end, board, en_passant=True))

        return moves

    def __repr__(self) -> str:
        return 'P' if self.player.color[0] == 'w' else 'p'


class Queen(Piece):
    """
    The 'Queen' is the most powerful piece and may move in all directions as far as she likes.\n
    She has less choice at the edge or in the corner.
    """

    def __init__(self, player: object, row: int, column: int):
        super().__init__(player=player, row=row, column=column, name='queen', evaluation=9)

    def legal_moves(self, board: object, pins: list = ()) -> list[object]:
        """
        Creates all legal moves.

        :param board: The current chessboard.
        :param pins: A list of pinned spots.
        :return: A list of all legal moves.
        """

        unprepared_directions: list[tuple] = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)]
        moves: list[object] = []

        # revision of directions is only important for 'ComputerizedPlayer'
        directions = self.prepare_directions(unprepared_directions, pins)

        for direction in directions:
            moves += [i for i in self.iterative_moves(direction, board)]

        return moves

    def __repr__(self) -> str:
        return 'Q' if self.player.color[0] == 'w' else 'q'


class Rook(Piece):
    """
    It is the second strongest piece after the 'Queen' and moves as far as it wants in a straight line
    (horizontally or vertically). It has the same number of moves from any square, at least when the board is empty,
    so it doesn't mind being on the edge or in the corner.
    """

    def __init__(self, player: object, row: int, column: int):
        super().__init__(player=player, row=row, column=column, name='rook', evaluation=5)

    def legal_moves(self, board: object, pins: list = ()) -> list[object]:
        """
        Creates all legal moves.

        :param board: The current chessboard.
        :param pins: A list of pinned spots.
        :return: A list of all legal moves.
        """

        unprepared_directions: list[tuple] = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        moves: list[object] = []

        # revision of directions is only important for 'ComputerizedPlayer'
        directions = self.prepare_directions(unprepared_directions, pins)

        for direction in directions:
            moves += [i for i in self.iterative_moves(direction, board)]

        return moves

    def __repr__(self) -> str:
        return 'R' if self.player.color[0] == 'w' else 'r'
