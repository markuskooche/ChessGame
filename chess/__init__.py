__author__ = "Markus Koch"
__status__ = "Production"
__version__ = "1.0.1"


from chess.board import Board
from chess.move import Move
import pygame


IMAGES = {}
COLORS = [(240, 240, 240), (180, 180, 180)]

MAX_FPS = 30
SIZE = 60


class Game:
    def __init__(self):
        Game.load_pieces()
        pygame.init()
        pygame.display.set_caption('Chess')
        self.display = pygame.display.set_mode((8 * SIZE, 8 * SIZE))
        self.board = Board()
        clock = pygame.time.Clock()
        running = True

        selected = ()
        player_click = []

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.board.undo_move()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    location = pygame.mouse.get_pos()
                    column = location[0] // SIZE
                    row = location[1] // SIZE
                    if selected == (row, column):
                        selected = ()
                    else:
                        selected = (row, column)
                        player_click.append(selected)

                    if len(player_click) == 2:
                        moving = Move(player_click[0], player_click[1], self.board)
                        self.board.move_piece(moving)
                        selected = ()
                        player_click = []
            self.draw()
            clock.tick(MAX_FPS)
            pygame.display.flip()

    def draw(self):
        self.draw_board()
        self.draw_pieces()

    def draw_board(self):
        for r in range(8):
            for c in range(8):
                color = COLORS[((r + c) % 2)]
                pygame.draw.rect(self.display, color, pygame.Rect((c * SIZE), (r * SIZE), SIZE, SIZE))

    def draw_pieces(self):
        for r in range(8):
            for c in range(8):
                piece = self.board.get_piece(row=r, column=c)
                if piece != '--':
                    self.display.blit(IMAGES[piece], pygame.Rect((c * SIZE), (r * SIZE), SIZE, SIZE))

    @staticmethod
    def load_pieces():
        pieces = ['bR', 'bN', 'bB', 'bQ', 'bK', 'bP', 'wR', 'wN', 'wB', 'wQ', 'wK', 'wP']
        for piece in pieces:
            IMAGES[piece] = pygame.transform.scale(pygame.image.load(f'./chess/pieces/{piece}.png'), (SIZE, SIZE))
