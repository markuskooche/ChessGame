__author__ = "Markus Koch"
__status__ = "Production"
__version__ = "0.2.1"


import chess.figures as figure
from chess.players import HumanPlayer
from chess.board import Board
from chess.move import Move
import pygame


SIZE: int = 60
IMAGES: dict = {}
COLORS: dict[str, tuple] = {'white': (240, 240, 240), 'gray': (180, 180, 180),
                            'yellow': (250, 250, 140), 'red': (250, 110, 70)}


class Game:
    players: dict = {
        '1': HumanPlayer(color='white', name='Markus'),
        '2': HumanPlayer(color='black', name='Computer')
    }

    def __init__(self):
        Game.load_pieces()
        player_selection: list[tuple] = []
        self.pieces_changed: bool = True
        self.board_changed: bool = True
        self.valid_moves: list = []
        self.player: int = 1

        running: bool = True

        pygame.init()
        pygame.display.set_caption('Chess')
        self.display = pygame.display.set_mode((8 * SIZE, 8 * SIZE))
        self.board = Board(self.players)
        self.draw()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running: bool = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.player = (self.player % 2) + 1
                        self.board.undo_move()
                        self.draw()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    location: tuple = pygame.mouse.get_pos()
                    column: int = location[0] // SIZE
                    row: int = location[1] // SIZE

                    selected: tuple = (row, column)
                    selected_figure: object = self.board.get_piece(row=selected[0], column=selected[1])

                    if (len(player_selection) == 0) and (selected_figure.player == self.players.get(str(self.player))):
                        self.valid_moves = selected_figure.legal_moves(self.board)
                        if len(self.valid_moves) != 0:
                            self.highlight_board(row=selected[0], column=selected[1], color=COLORS.get('yellow'))
                            player_selection.append(selected)
                        else:
                            self.highlight_board(row=selected[0], column=selected[1], color=COLORS.get('red'))
                        print(self.valid_moves)
                    elif (len(player_selection) == 1) and (selected in self.valid_moves):
                        player_selection.append(selected)
                    else:
                        self.highlight_board(row=selected[0], column=selected[1], color=COLORS.get('red'))

                    if len(player_selection) == 2:
                        player_move: object = Move(player_selection[0], player_selection[1], self.board)
                        self.board.move_piece(player_move)
                        self.player = (self.player % 2) + 1
                        player_selection: list[tuple] = []
                        self.draw()

    def draw(self):
        self.draw_board()
        self.draw_pieces()

    def draw_board(self):
        for r in range(8):
            for c in range(8):
                color: str = 'white' if ((r + c) % 2 == 0) else 'gray'
                pygame.draw.rect(self.display, COLORS.get(color), pygame.Rect((c * SIZE), (r * SIZE), SIZE, SIZE))

    def draw_pieces(self):
        for r in range(8):
            for c in range(8):
                piece = self.board.get_piece(row=r, column=c)
                if type(piece) != figure.Blank:
                    self.display.blit(IMAGES[piece.load_image()], pygame.Rect((c * SIZE), (r * SIZE), SIZE, SIZE))
        pygame.display.flip()

    def highlight_board(self, row: int, column: int, color: tuple):
        self.draw_board()
        pygame.draw.rect(self.display, color, pygame.Rect((column * SIZE), (row * SIZE), SIZE, SIZE))
        self.draw_pieces()

    @staticmethod
    def load_pieces():
        pieces = ['b_rook', 'b_knight', 'b_bishop', 'b_queen', 'b_king', 'b_pawn',
                  'w_rook', 'w_knight', 'w_bishop', 'w_queen', 'w_king', 'w_pawn']
        for piece in pieces:
            IMAGES[piece] = pygame.transform.scale(pygame.image.load(f'./chess/pieces/{piece}.png'), (SIZE, SIZE))
