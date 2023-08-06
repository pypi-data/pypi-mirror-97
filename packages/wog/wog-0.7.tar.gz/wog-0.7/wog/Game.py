from abc import ABC, abstractmethod


class Game(ABC):
    @abstractmethod
    def __init__(self, difficulty):
        self.difficulty = difficulty

    @abstractmethod
    def play(self):
        pass
