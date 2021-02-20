from chess.player import ComputerizedPlayer
import chess.figures as figure
import numpy


class Board:
    def __init__(self, players: dict):
        self.move_log = []
        self.white_move = True
        self.board = numpy.empty((8, 8), dtype=object)

        # [i][0] = white_queen_side_castling, [i][1] = white_king_side_castling
        # [i][2] = black_queen_side_castling, [i][3] = clack_king_side_castling
        self.castling_log: list[tuple] = [(True, True, True, True)]

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

    def set_piece(self, row: int, column: int, set_piece: object):
        self.board[row][column] = set_piece

    def move_piece(self, move: object):
        """
        Executes the move and updates the board and the position of the figure.
        """
        self.board[move.start_row][move.start_column] = figure.Blank(move.start_row, move.start_column)
        self.board[move.end_row][move.end_column] = move.moved_piece
        move.moved_piece.set_position(move.end_row, move.end_column)
        player = move.moved_piece.player

        # updating the kings position
        if isinstance(move.moved_piece, figure.King):
            move.moved_piece.player.king_position = (move.end_row, move.end_column)

        # pawn promotion
        if move.is_pawn_promotion:
            # TODO: detect which promotion is the best [Knight or Queen]
            if isinstance(player, ComputerizedPlayer):
                self.board[move.end_row][move.end_column] = figure.Queen(player, move.end_row, move.end_column)
            else:
                entry = None

                # TODO: create a popup window where you can select a figure
                while entry not in ['N', 'B', 'R', 'Q']:
                    entry = input('Enter Pawn Promotion [N, B, R, Q]: ').upper()

                if entry == 'N':
                    self.board[move.end_row][move.end_column] = figure.Knight(player, move.end_row, move.end_column)
                elif entry == 'B':
                    self.board[move.end_row][move.end_column] = figure.Bishop(player, move.end_row, move.end_column)
                elif entry == 'R':
                    self.board[move.end_row][move.end_column] = figure.Rook(player, move.end_row, move.end_column)
                elif entry == 'Q':
                    self.board[move.end_row][move.end_column] = figure.Queen(player, move.end_row, move.end_column)

        # update player.en_passant on 2 square pawn moves
        if isinstance(move.moved_piece, figure.Pawn) and abs(move.start_row - move.end_row):
            player.en_passant = ((move.start_row + move.end_row) // 2, move.end_column)
        else:
            player.en_passant = ()

        # en passant move
        if move.is_en_passant:
            self.board[move.start_row][move.end_column] = figure.Blank(move.start_row, move.end_column)

        # castling move
        self.castling_move(move)

        # update castling rights
        self.update_castling(move, player)

        self.white_move = not self.white_move
        self.move_log.append(move)

    def undo_move(self) -> bool:
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
            self.white_move = not self.white_move

            # resets the captured pawn
            if move.is_en_passant:
                enemy = move.moved_piece.player.opponent
                pawn = figure.Pawn(enemy, move.start_row, move.end_column)
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
        castling_log_length = len(self.castling_log) - 1

        white_queen_side = self.castling_log[castling_log_length][0]
        white_king_side = self.castling_log[castling_log_length][1]
        black_queen_side = self.castling_log[castling_log_length][2]
        black_king_side = self.castling_log[castling_log_length][3]

        if isinstance(move.moved_piece, figure.King):
            if player.color == 'white':
                white_queen_side = False
                white_king_side = False
            elif player.color == 'black':
                black_queen_side = False
                black_king_side = False

            self.castling_log.append((white_queen_side, white_king_side, black_queen_side, black_king_side))
        elif isinstance(move.moved_piece, figure.Rook):
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
        if isinstance(move.moved_piece, figure.King) or isinstance(move.moved_piece, figure.Rook):
            self.castling_log.pop()

    def castling_move(self, move: object):
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
        for r in range(8):
            for c in range(8):
                print(self.board[r][c], end=' ')
            print()
