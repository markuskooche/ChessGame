from abc import ABC, abstractmethod
from chess.move import Move


class Piece(ABC):
    """
    The 'Piece' class is an abstract class from which all 'Pieces' inherit.
    This class contains functions that are used by all classes, or contains functions that must be implemented.
    """

    def __init__(self, player: object, row: int, column: int, name: str, evaluation: int):
        self.evaluation: int = evaluation
        self.player: object = player
        self.name: str = name

        self.column: int = column
        self.row: int = row

    def position(self) -> tuple:
        return self.row, self.column

    def load_image(self) -> str:
        """
        This function returns the correct name of the required image.
        """
        return f'{self.player.color[0]}_{self.name}'
    
    def set_position(self, row: int, column: int):
        """
        This function updates the position [row, column] of a piece.
        """
        self.column = column
        self.row = row

    def prepare_directions(self, directions: list[tuple], pins: list[tuple]) -> list[tuple]:
        """
        This function is used for a 'ComputerizedPlayer' to update allowed movement directions.
        For a 'HumanPlayer', it returns the original list.
        """
        calculated_directions = directions

        # this is always false with 'HumanPlayer'
        if len(pins) != 0:
            for pin in pins:
                if (self.row == pin[0]) and (self.column == pin[1]):
                    calculated_directions.clear()

                    # append both directions to go to the enemy and the king
                    calculated_directions.append((pin[2], pin[3]))
                    calculated_directions.append(((-1) * pin[2], (-1) * pin[3]))
                    break

        return calculated_directions

    def iterative_moves(self, direction: tuple, board: object) -> list[object]:
        """
        This function serves as an auxiliary function for the characters Bishop, Rook and Queen.
        It iterates in a passed direction over all allowed moves and returns them.
        """
        moves: list[object] = []

        for i in range(1, 8):
            new_column: int = self.column + (i * direction[1])
            new_row: int = self.row + (i * direction[0])

            if (new_row in range(0, 8)) and (new_column in range(0, 8)):
                piece = board.get_piece(row=new_row, column=new_column)
                if piece.player is not self.player:
                    moves.append(Move(self.position(), (new_row, new_column), board))

                    # ends the loop if it is an enemy piece
                    # this prevents the jumping over of pieces
                    if piece.player is not None:
                        break
                else:
                    break

            # to improve speed
            else:
                break

        return moves

    @abstractmethod
    def legal_moves(self, board: object) -> list[tuple]:
        """
        An abstract method to ensure that this function is implemented by all pieces.
        """
        pass
