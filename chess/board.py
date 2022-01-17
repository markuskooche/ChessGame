from chess.player import ComputerizedPlayer
import chess.pieces as p
import numpy


class Board:
    """
    Board is an 8×8 set of boxes containing all active chess pieces.
    This class controls the flow of a game. It keeps track of all the game moves.
    """

    def __init__(self, players: dict):
        self.move_log = []
        self.white_move = True
        self.board = numpy.empty((8, 8), dtype=object)

        # [i][0] = white_queen_side_castling, [i][1] = white_king_side_castling
        # [i][2] = black_queen_side_castling, [i][3] = clack_king_side_castling
        self.castling_log: list[tuple] = [(True, True, True, True)]

        white: object = players.get('1')
        black: object = players.get('2')

        for r in range(1, 7):
            for c in range(8):
                self.board[r][c] = p.Blank(row=r, column=c)

        for c in range(8):
            self.board[1][c] = p.Pawn(player=black, row=1, column=c)
            self.board[6][c] = p.Pawn(player=white, row=6, column=c)

        for r in (0, 7):
            player = white if r == 7 else black
            self.board[r][0] = p.Rook(player=player, row=r, column=0)
            self.board[r][1] = p.Knight(player=player, row=r, column=1)
            self.board[r][2] = p.Bishop(player=player, row=r, column=2)
            self.board[r][3] = p.Queen(player=player, row=r, column=3)
            self.board[r][4] = p.King(player=player, row=r, column=4)
            self.board[r][5] = p.Bishop(player=player, row=r, column=5)
            self.board[r][6] = p.Knight(player=player, row=r, column=6)
            self.board[r][7] = p.Rook(player=player, row=r, column=7)

    def get_piece(self, row: int, column: int) -> object:
        """
        When row and column are passed, the corresponding piece is returned.
        """

        return self.board[row][column]

    def set_piece(self, row: int, column: int, piece: object):
        """
        When row, column and piece are passed, the position is overwritten with the passed piece.
        """

        self.board[row][column] = piece

    def move_piece(self, move: object, move_finding: bool = False):
        """
        Executes the move and updates the board and the position of the piece.
        Set move_finding to true if you call this method by a computerized player.
        """

        self.board[move.start_row][move.start_column] = p.Blank(move.start_row, move.start_column)
        self.board[move.end_row][move.end_column] = move.moved_piece
        move.moved_piece.set_position(move.end_row, move.end_column)
        player = move.moved_piece.player

        # updating the kings position
        if isinstance(move.moved_piece, p.King):
            move.moved_piece.player.king_position = (move.end_row, move.end_column)

        # pawn promotion
        if move.is_pawn_promotion:
            # TODO: detect which promotion is the best [Knight or Queen]
            if isinstance(player, ComputerizedPlayer) or move_finding:
                self.board[move.end_row][move.end_column] = p.Queen(player, move.end_row, move.end_column)
            else:
                entry = None

                # TODO: create a popup window where you can select a figure
                while entry not in ['N', 'B', 'R', 'Q']:
                    entry = input('Enter Pawn Promotion [N, B, R, Q]: ').upper()

                if entry == 'N':
                    self.board[move.end_row][move.end_column] = p.Knight(player, move.end_row, move.end_column)
                elif entry == 'B':
                    self.board[move.end_row][move.end_column] = p.Bishop(player, move.end_row, move.end_column)
                elif entry == 'R':
                    self.board[move.end_row][move.end_column] = p.Rook(player, move.end_row, move.end_column)
                elif entry == 'Q':
                    self.board[move.end_row][move.end_column] = p.Queen(player, move.end_row, move.end_column)

        # update player.en_passant on 2 square pawn moves
        if isinstance(move.moved_piece, p.Pawn) and abs(move.start_row - move.end_row):
            player.en_passant = ((move.start_row + move.end_row) // 2, move.end_column)
        else:
            player.en_passant = ()

        # en passant move
        if move.is_en_passant:
            self.board[move.start_row][move.end_column] = p.Blank(move.start_row, move.end_column)

        # castling move
        self.castling_move(move)

        # update castling rights
        self.update_castling(move, player)

        self.white_move = not self.white_move
        self.move_log.append(move)

    def undo_move(self) -> bool:
        """
        Undoes the move and resets the board and the position of the piece.
        """

        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_column] = move.moved_piece
            self.board[move.end_row][move.end_column] = move.captured_piece
            move.moved_piece.set_position(move.start_row, move.start_column)
            if isinstance(move.moved_piece, p.King):
                move.moved_piece.player.king_position = (move.start_row, move.start_column)
            self.white_move = not self.white_move

            # resets the captured pawn
            if move.is_en_passant:
                enemy = move.moved_piece.player.enemy
                pawn = p.Pawn(enemy, move.start_row, move.end_column)
                self.board[move.start_row][move.end_column] = pawn

            # castling move
            self.castling_move(move)

            # reset castling rights
            self.reset_castling(move)

            return True

        # important for setting the player back to 1
        else:
            return False

    def update_castling(self, move: object, player: object):
        """
        If the movement is from a 'Rook' or a 'King', a new castling_log' is created.
        """

        white_queen_side = self.castling_log[-1][0]
        white_king_side = self.castling_log[-1][1]
        black_queen_side = self.castling_log[-1][2]
        black_king_side = self.castling_log[-1][3]

        if isinstance(move.moved_piece, p.King):
            if player.color == 'white':
                white_queen_side = False
                white_king_side = False
            elif player.color == 'black':
                black_queen_side = False
                black_king_side = False

            self.castling_log.append((white_queen_side, white_king_side, black_queen_side, black_king_side))
        elif isinstance(move.moved_piece, p.Rook):
            # disable queen side castling if left rook has moved
            if move.start_column == 0:
                if player.color == 'white':
                    white_queen_side = False
                elif player.color == 'black':
                    black_queen_side = False

            # disable king side castling if right rook has moved
            elif move.start_column == 7:
                if player.color == 'white':
                    white_king_side = False
                elif player.color == 'black':
                    black_king_side = False

            self.castling_log.append((white_queen_side, white_king_side, black_queen_side, black_king_side))

    def reset_castling(self, move: object):
        """
        If the last move was from a 'Rook' or a 'King', the last 'castling_log' is removed.
        """

        if isinstance(move.moved_piece, p.King) or isinstance(move.moved_piece, p.Rook):
            self.castling_log.pop()

    def castling_move(self, move: object):
        """
        Checks if it is castling and executes or resets the 'Rook' move.
        """

        if move.castle_move:
            # queen side castling move
            if (move.start_column - move.end_column) == 2:
                # swapping the rook with the blank piece
                self.board[move.end_row][0], self.board[move.end_row][move.end_column + 1] = \
                    self.board[move.end_row][move.end_column + 1], self.board[move.end_row][0]

            # king side castling move
            elif (move.start_column - move.end_column) == -2:
                # swapping the rook with the blank piece
                self.board[move.end_row][7], self.board[move.end_row][move.end_column - 1] = \
                    self.board[move.end_row][move.end_column - 1], self.board[move.end_row][7]

    def print_console(self):
        """
        Outputs the current board on the console.
        """

        for r in range(8):
            for c in range(8):
                print(self.board[r][c], end=' ')
            print()
