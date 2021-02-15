from abc import ABC, abstractmethod


class Figure(ABC):
    def __init__(self, player: object, row: int, column: int, figure: str, evaluation: int):
        self.evaluation: int = evaluation
        self.player: object = player
        self.figure: str = figure
        self.column: int = column
        self.row: int = row

    def load_image(self) -> str:
        return f'{self.player.color[0]}_{self.figure}'

    def get_position(self) -> str:
        return 'ABCDEFGH'[self.column] + '87654321'[self.row]

    def set_position(self, row: int, column: int):
        self.column = column
        self.row = row

    def offset_moves(self, offsets: list[tuple], board: object) -> list[tuple]:
        positions: list[tuple] = []

        for (column_off, row_off) in offsets:
            new_column: int = self.column + column_off
            new_row: int = self.row + row_off

            if (new_row in range(0, 8)) and (new_column in range(0, 8)):
                figure = board.get_piece(row=new_row, column=new_column)
                if figure.player is not self.player:
                    positions.append((new_row, new_column))

        return positions

    def iterative_moves(self, it_column: int, it_row: int, board: object) -> list[tuple]:
        positions: list[tuple] = []

        for i in range(1, 8):
            new_column: int = self.column + it_column * i
            new_row: int = self.row + it_row * i

            if (new_row in range(0, 8)) and (new_column in range(0, 8)):
                figure = board.get_piece(row=new_row, column=new_column)
                if figure.player is not self.player:
                    positions.append((new_row, new_column))

                    # End the loop if it is an enemy figure.
                    # This prevents the jumping over of figures.
                    if figure.player is not None:
                        break
                else:
                    break

        return positions

    @abstractmethod
    def legal_moves(self, board: object) -> list[tuple]:
        pass