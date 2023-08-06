from wog.Game import Game
from random import randint
import sys
from time import sleep


class MemoryGame(Game):
    def __init__(self, difficulty):
        super().__init__(difficulty)

    def __generate_sequence(self):
        computer_sequence = []
        for i in range(self.difficulty):
            rand_num = randint(1, 101)
            computer_sequence.append(rand_num)
        return computer_sequence

    def __get_list_from_user(self):
        user_sequence = []
        print("\rNow try to remember which numbers appeared.")
        for i in range(self.difficulty):
            user_sequence.append(int(input(f"#{i + 1} number: ")))
        return user_sequence

    def __is_list_equal(self, computer_sequence, user_sequence):
        for i in range(self.difficulty):
            if computer_sequence[i] != user_sequence[i]:
                return False
        return True

    def play(self):
        computer_sequence = self.__generate_sequence()
        for number in computer_sequence:
            sys.stdout.write("\r")
            sys.stdout.write(f"{number} ")
            sleep(0.7)
            sys.stdout.flush()
        sys.stdout.flush()
        user_sequence = self.__get_list_from_user()
        print("\nThe numbers that appeared are:", str(computer_sequence))
        return self.__is_list_equal(computer_sequence, user_sequence)