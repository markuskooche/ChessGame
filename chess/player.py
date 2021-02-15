from abc import ABC, abstractmethod


COLORS: list[str] = ['white', 'black']


class Player(ABC):
    def __init__(self, color: str, name: str):
        # TODO: not sure if this plan will work
        # self.opponent = opponent
        self.player_moves = {}

        if color not in COLORS:
            raise Exception(f"Player color must be in {COLORS} but color is '{color}'")
        else:
            self.color = color
        self.name = name


class ComputerizedPlayer(Player, ABC):
    def __init__(self, color: str, name: str):
        super().__init__(color=color, name=name)

    @abstractmethod
    def best_move(self, board: object) -> object:
        pass
