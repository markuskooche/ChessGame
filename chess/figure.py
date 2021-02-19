from abc import ABC, abstractmethod
from chess.move import Move


class Figure(ABC):
    def __init__(self, player: object, row: int, column: int, figure: str, evaluation: int):
        self.evaluation: int = evaluation
        self.player: object = player
        self.figure: str = figure
        self.column: int = column
        self.row: int = row

    def load_image(self) -> str:
        return f'{self.player.color[0]}_{self.figure}'

    def set_position(self, row: int, column: int):
        self.column = column
        self.row = row

    def prepare_directions(self, directions: list[tuple], pins: list[tuple]) -> list[tuple]:
        calculated_directions = directions

        if len(pins) != 0:
            for pin in pins:
                if (self.row == pin[0]) and (self.column == pin[1]):
                    calculated_directions.clear()

                    # append pinned direction to go to the opponent
                    # append opposite direction to go to the king
                    calculated_directions.append((pin[2], pin[3]))
                    calculated_directions.append(((-1) * pin[2], (-1) * pin[3]))
                    break

        return calculated_directions

    def iterative_moves(self, direction: tuple, board: object) -> list[object]:
        positions: list[object] = []
        start: tuple = (self.row, self.column)

        for i in range(1, 8):
            new_column: int = self.column + (i * direction[1])
            new_row: int = self.row + (i * direction[0])

            if (new_row in range(0, 8)) and (new_column in range(0, 8)):
                figure = board.get_piece(row=new_row, column=new_column)
                if figure.player is not self.player:
                    positions.append(Move(start, (new_row, new_column), board))

                    # ends the loop if it is an enemy figure
                    # this prevents the jumping over of figures
                    if figure.player is not None:
                        break
                else:
                    break

            # to improve speed
            else:
                break

        return positions

    @abstractmethod
    def legal_moves(self, board: object) -> list[tuple]:
        pass
