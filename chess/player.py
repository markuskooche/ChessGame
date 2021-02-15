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


# TODO: maybe add ComputerizedPlayer(Player) [= abstract]
