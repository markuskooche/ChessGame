__author__ = "Markus Koch"
__status__ = "Production"
__version__ = "0.3"


import chess.figures as figure
from chess.player import ComputerizedPlayer
from chess.players import HumanPlayer, RandomPlayer
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
        '2': RandomPlayer(color='black')

        # '2': HumanPlayer(color='black', name='Random')
    }

    def __init__(self):
        Game.load_pieces()

        selected_move: object = None
        saved_selection: tuple = ()
        running: bool = True

        pygame.init()
        pygame.display.set_caption('Chess')
        self.board = Board(self.players)
        self.players.get('1').set_opponent(self.board)
        self.players.get('2').set_opponent(self.board)
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
                        self.player = (self.player % 2) + 1
                        saved_selection: tuple = ()
                        self.board.undo_move()
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

                    # No valid piece is selected yet
                    if (len(saved_selection) == 0) and (selected_figure.player == actual_player):
                        self.valid_moves = actual_player.legal_moves(self.board)

                        for valid_move in self.valid_moves:
                            if (valid_move.start_row == selected[0]) and (valid_move.start_column == selected[1]):
                                self.__highlight_spot(position=selected, color=COLORS.get('yellow'))
                                saved_selection = selected
                                break
                        else:
                            self.__highlight_spot(position=selected, color=COLORS.get('red'))

                    # A piece is already selected but no final position yet
                    elif len(saved_selection) == 2:
                        for valid_move in self.valid_moves:
                            check_move: object = Move(saved_selection, selected, self.board)
                            if check_move.code() == valid_move.code():
                                selected_move = check_move
                                saved_selection = ()
                                break

                    # The selected piece is not your own piece
                    else:
                        self.__highlight_spot(position=selected, color=COLORS.get('red'))

                    # Moves the selected piece with a valid move
                    if selected_move is not None:
                        self.board.move_piece(selected_move)
                        self.player = (self.player % 2) + 1
                        selected_move = None

                        # If it is a ComputerizedPlayer a computerized move is executed
                        if isinstance(self.players.get(str(self.player)), ComputerizedPlayer):
                            best_move = self.players.get(str(self.player)).best_move(self.board)
                            self.player = (self.player % 2) + 1
                            self.board.move_piece(best_move)

                        self.__draw()

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
                if type(piece) != figure.Blank:
                    self.display.blit(IMAGES[piece.load_image()], pygame.Rect((c * SIZE), (r * SIZE), SIZE, SIZE))
        pygame.display.flip()

    def __highlight_spot(self, position: tuple, color: tuple):
        # TODO: how to remove this?
        # TODO: if i can remove -> more colors possible but problem with overlaying pieces
        self.__draw_board()

        column: int = (position[1] * SIZE)
        row: int = (position[0] * SIZE)
        pygame.draw.rect(self.display, color, pygame.Rect(column, row, SIZE, SIZE))
        self.__draw_pieces()

    @staticmethod
    def load_pieces():
        pieces = ['b_rook', 'b_knight', 'b_bishop', 'b_queen', 'b_king', 'b_pawn',
                  'w_rook', 'w_knight', 'w_bishop', 'w_queen', 'w_king', 'w_pawn']
        for piece in pieces:
            IMAGES[piece] = pygame.transform.scale(pygame.image.load(f'./chess/pieces/{piece}.png'), (SIZE, SIZE))
