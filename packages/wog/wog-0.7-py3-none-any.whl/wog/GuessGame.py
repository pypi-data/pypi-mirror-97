from wog.Game import Game
from random import randint


class GuessGame(Game):
    def __init__(self, difficulty):
        super().__init__(difficulty)
        self.__secret_number = 0

    def __generate_number(self):
        print("\nLet\'s try to guess a number.")
        self.__secret_number = randint(1, self.difficulty)

    def __get_guess_from_user(self):
        user_guess = int(input(f"\nPlease guess a number between 1 to {self.difficulty}.\n"))
        return user_guess

    @staticmethod
    def __compare_results(secret_number, user_guess):
        return True if secret_number == user_guess else False

    def play(self):
        self.__generate_number()
        user_number = self.__get_guess_from_user()
        print(f"\nWe chose the number: {self.__secret_number}, you guessed: {user_number}.")
        return self.__compare_results(self.__secret_number, user_number)
