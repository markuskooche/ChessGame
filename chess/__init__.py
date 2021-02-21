__author__ = "Markus Koch"
__status__ = "Production"
__version__ = "0.4"

from time import process_time

import chess.pieces as p
import pygame

from chess.players import HumanPlayer, RandomPlayer
from chess.player import ComputerizedPlayer
from chess.board import Board
from chess.move import Move


SIZE: int = 60
IMAGES: dict = {}
COLORS: dict[str, tuple] = {'white': (240, 240, 240), 'gray': (180, 180, 180),
                            'green': (0, 255, 0), 'yellow': (255, 255, 0), 'red': (250, 110, 70)}


ENGINEERING_MODE: bool = False


class Game:
    players: dict = {
        '1': HumanPlayer(color='white', name='Markus'),
        # '2': HumanPlayer(color='black', name='Random')
        # '1': RandomPlayer(color='white'),
        '2': RandomPlayer(color='black')
    }

    def __init__(self):
        Game.load_pieces()

        selected_move: object = None
        saved_selection: tuple = ()
        running: bool = True

        pygame.init()
        pygame.display.set_caption('Chess')
        self.board = Board(self.players)
        self.players.get('1').set_enemy(self.board)
        self.players.get('2').set_enemy(self.board)
        self.display = pygame.display.set_mode((8 * SIZE, 8 * SIZE))
        self.player: int = 1

        self.__draw()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running: bool = False

                elif event.type == pygame.KEYDOWN:
                    # undoes the last move
                    if event.key == pygame.K_r:
                        # sets the player to 1 if move_log is empty
                        if self.board.undo_move():
                            self.player = (self.player % 2) + 1
                        else:
                            self.player = 1

                        saved_selection: tuple = ()
                        self.__draw()

                    # removes the selection
                    elif event.key == pygame.K_d:
                        saved_selection: tuple = ()
                        self.__draw()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    location: tuple = pygame.mouse.get_pos()
                    column: int = location[0] // SIZE
                    row: int = location[1] // SIZE

                    selected: tuple = (row, column)
                    selected_figure: object = self.board.get_piece(row=selected[0], column=selected[1])
                    actual_player: object = self.players.get(str(self.player))

                    # no valid piece is selected yet
                    if (len(saved_selection) == 0) and (selected_figure.player == actual_player):
                        start = process_time()
                        self.valid_moves = actual_player.legal_moves(self.board)
                        end = process_time()
                        print(f"'{actual_player.name}' TIME: {round(((end - start) * 1000), 2)}ms")

                        for valid_move in self.valid_moves:
                            if (valid_move.start_row == selected[0]) and (valid_move.start_column == selected[1]):
                                self.highlight(selected_figure.legal_moves(self.board), selected)
                                saved_selection = selected
                                break

                    # a piece is already selected but no final position yet
                    elif len(saved_selection) == 2:
                        check_move: object = Move(saved_selection, selected, self.board)
                        for i in range(len(self.valid_moves)):
                            valid_move = self.valid_moves[i]

                            if check_move.code() == valid_move.code():
                                self.animate_move(valid_move)
                                self.board.move_piece(self.valid_moves[i])
                                self.player = (self.player % 2) + 1
                                selected_move = None
                                saved_selection = ()

                                if not ENGINEERING_MODE:
                                    # if it is a 'ComputerizedPlayer' a computerized move is executed
                                    if isinstance(self.players.get(str(self.player)), ComputerizedPlayer):
                                        start = process_time()
                                        best_move = self.players.get(str(self.player)).best_move(self.board)
                                        end = process_time()
                                        print(f"'{actual_player.enemy.name}' TIME: {round(((end - start) * 1000), 2)}ms")
                                        print()
                                        self.player = (self.player % 2) + 1
                                        self.board.move_piece(best_move)

                                self.__draw()
                                break

                    # the selected piece is not your own piece
                    # else:
                        # self.__highlight_spot(position=selected, color=COLORS.get('red'))

                    # moves the selected piece with a valid move
                    if selected_move is not None:
                        self.board.move_piece(selected_move)
                        self.player = (self.player % 2) + 1
                        selected_move = None

                        if not ENGINEERING_MODE:
                            # if it is a 'ComputerizedPlayer' a computerized move is executed
                            if isinstance(self.players.get(str(self.player)), ComputerizedPlayer):
                                start = process_time()
                                best_move = self.players.get(str(self.player)).best_move(self.board)
                                end = process_time()
                                # print(f"'{actual_player.enemy.name}' TIME: {round(((end - start) * 1000), 2)}ms")
                                # print()
                                self.player = (self.player % 2) + 1
                                self.board.move_piece(best_move)

                        self.__draw()

    def highlight(self, valid_moves, selected):
        self.__draw_board()

        if selected != ():
            r, c = selected

            # initial setup for surfaces
            square = pygame.Surface((SIZE, SIZE))
            square.set_alpha(100)

            # highlight selected square
            square.fill(pygame.Color(COLORS.get('green')))
            self.display.blit(square, (c * SIZE, r * SIZE))

            # highlight squares which valid moves
            square.fill(COLORS.get('yellow'))

            if len(valid_moves) != 0:
                for valid_move in valid_moves:
                    if (valid_move.start_row == r) and (valid_move.start_column == c):
                        column = (valid_move.end_column * SIZE)
                        row = (valid_move.end_row * SIZE)
                        self.display.blit(square, (column, row))

        self.__draw_pieces()

    def animate_move(self, selected_move):
        clock = pygame.time.Clock()

        start_column = selected_move.start_column
        start_row = selected_move.start_row
        end_column = selected_move.end_column
        end_row = selected_move.end_row

        # to disable the moved piece, otherwise it's visible twice
        blank = p.Blank(start_row, start_column)
        self.board.set_piece(start_row, start_column, blank)

        direction_c = end_column - start_column
        direction_r = end_row - start_row

        frames_per_square = 6
        frame_count = (abs(direction_r) + abs(direction_c)) * frames_per_square

        for frame in range(frame_count + 1):
            column = (start_column + (direction_c * frame/frame_count))
            row = (start_row + (direction_r * frame / frame_count))

            self.__draw_board()
            self.__draw_pieces()

            end_square = pygame.Rect(end_column * SIZE, end_row * SIZE, SIZE, SIZE)
            # pygame.draw.rect(self.display, COLORS.get('yellow'), end_square)

            captured_piece = selected_move.captured_piece
            if not isinstance(captured_piece, p.Blank):
                self.display.blit(IMAGES[captured_piece.load_image()], end_square)

            moved_piece = selected_move.moved_piece
            self.display.blit(IMAGES[moved_piece.load_image()], pygame.Rect(column * SIZE, row * SIZE, SIZE, SIZE))

            pygame.display.flip()
            clock.tick(60)

    def __draw(self):
        self.__draw_board()
        self.__draw_pieces()

    def __draw_board(self):
        for r in range(8):
            for c in range(8):
                color: str = 'white' if ((r + c) % 2 == 0) else 'gray'
                pygame.draw.rect(self.display, COLORS.get(color), pygame.Rect((c * SIZE), (r * SIZE), SIZE, SIZE))

    def __draw_pieces(self):
        for r in range(8):
            for c in range(8):
                piece = self.board.get_piece(row=r, column=c)
                if type(piece) != p.Blank:
                    self.display.blit(IMAGES[piece.load_image()], pygame.Rect((c * SIZE), (r * SIZE), SIZE, SIZE))
        pygame.display.flip()

    @staticmethod
    def load_pieces():
        image_names = ['b_rook', 'b_knight', 'b_bishop', 'b_queen', 'b_king', 'b_pawn',
                       'w_rook', 'w_knight', 'w_bishop', 'w_queen', 'w_king', 'w_pawn']
        for image_name in image_names:
            loader = pygame.image.load(f'./chess/pieces/{image_name}.png')
            IMAGES[image_name] = pygame.transform.scale(loader, (SIZE, SIZE))
