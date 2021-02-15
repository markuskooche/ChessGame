from abc import ABC, abstractmethod

class Player(ABC):
    def __init__(self, color: str, name: str):
        #self.opponent = opponent
        self.player_moves = {}
        self.color = color
        self.name = name
