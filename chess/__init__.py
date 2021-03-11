__author__ = "Markus Koch"
__status__ = "Production"
__version__ = "0.4.3"

from time import sleep

import chess.pieces as p
import pygame

from chess.players import HumanPlayer, RandomPlayer, MiniMaxPlayer, MiniMaxIterativePlayer
from chess.player import ComputerizedPlayer
from chess.board import Board
from chess.move import Move

SIZE: int = 60
IMAGES: dict = {}
COLORS: dict[str, tuple] = {'white': (240, 240, 240), 'gray': (180, 180, 180),
                            'green': (0, 255, 0), 'yellow': (255, 255, 0), 'red': (255, 0, 0)}


class Game:
    players: dict = {
        '1': HumanPlayer(color='white', name='Human'),
        # '1': RandomPlayer(color='white'),
        '2': MiniMaxPlayer(color='black', max_depth=3)
    }

    def __init__(self):
        Game.load_pieces()

        self.running: bool = True

        pygame.init()
        pygame.display.set_caption('Chess')
        self.board = Board(self.players)
        self.players.get('1').set_enemy(self.board)
        self.players.get('2').set_enemy(self.board)
        self.display = pygame.display.set_mode((8 * SIZE, 8 * SIZE))
        self.player: int = 1

        self.human_moves: list[tuple] = []

        self.__draw()

        while self.running:
            current_player = self.players.get(str(self.player))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running: bool = False

                elif event.type == pygame.KEYDOWN:
                    # start a new game
                    if event.key == pygame.K_n:
                        self.board = Board(self.players)
                        self.players.get('1').set_enemy(self.board)
                        self.players.get('2').set_enemy(self.board)
                        self.player: int = 1

                    # undoes the last move
                    elif event.key == pygame.K_r:
                        # sets the player to 1 if move_log is empty
                        if self.board.undo_move():
                            self.player = (self.player % 2) + 1
                        else:
                            self.player = 1

                    # removes the selection
                    elif event.key == pygame.K_d:
                        self.human_moves = []

                    self.__draw()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if isinstance(current_player, HumanPlayer):
                        location: tuple = pygame.mouse.get_pos()
                        column: int = location[0] // SIZE
                        row: int = location[1] // SIZE

                        chosen_piece: object = self.board.get_piece(row, column)

                        if len(self.human_moves) == 0 and (chosen_piece.player == current_player):
                            moves = chosen_piece.legal_moves(self.board)

                            if len(moves) != 0:
                                start_column = moves[0].start_column
                                start_row = moves[0].start_row

                                self.human_moves = moves
                                self.highlight(self.human_moves, (start_row, start_column))
                            else:
                                self.highlight([], (row, column), color='red')

                        if len(self.human_moves) != 0:
                            for human_move in self.human_moves:
                                if (human_move.end_row == row) and (human_move.end_column == column):
                                    current_player.set_move(human_move)
                                    self.human_moves = []

            next_move = current_player.best_move(self.board)

            if next_move is not None:
                if isinstance(current_player, ComputerizedPlayer):
                    moving_piece = next_move.moved_piece
                    start = (next_move.start_row, next_move.start_column)
                    self.highlight(moving_piece.legal_moves(self.board), start)
                    sleep(1)
                elif isinstance(current_player, HumanPlayer):
                    current_player.set_move(None)

                if self.running:
                    self.animate_move(next_move)
                    self.board.move_piece(next_move)

                self.player = (self.player % 2) + 1
                self.__draw()
                sleep(0.5)

    def highlight(self, valid_moves, selected, color='green'):
        self.__draw_board()

        if selected != ():
            r, c = selected

            # initial setup for surfaces
            square = pygame.Surface((SIZE, SIZE))
            square.set_alpha(100)

            # highlight selected square
            square.fill(pygame.Color(COLORS.get(color)))
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

    def animate_move(self, selected_move: object):
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
            column = (start_column + (direction_c * frame / frame_count))
            row = (start_row + (direction_r * frame / frame_count))

            self.__draw_board()
            self.__draw_pieces()

            end_square = pygame.Rect(end_column * SIZE, end_row * SIZE, SIZE, SIZE)

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
