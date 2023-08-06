from wog.GuessGame import GuessGame
from wog.MemoryGame import MemoryGame
from wog.CurrencyRouletteGame import CurrencyRouletteGame


def welcome(name):
    print("==============================")
    print(" _       __           ___")
    print("| |     / /  ___    //")
    print("| | /| / / //  \\\  //  __")
    print("| |/ |/ / //   // //    //")
    print("|_/  |_/  \\\__//  \\\___//")
    print("==============================")
    output = (f"Hello {name} and welcome to the World of Games (WoG).\n"
              f"Here you can find many cool games to play.\n")
    return output


def load_game():
    valid_option = False
    # I'm using a range like an Enum in favor of more readable code.
    memory_game, guess_game, currency_roulette_game = range(1, 4)
    winner_str = "Awesome, You're right! :)"
    looser_str = "It was close, but wrong. :(\nDon\'t give up, maybe next time!"
    while not valid_option:
        selected_game = input(f"\nPlease choose a game to play:\n"
              f"1. Memory Game - a sequence of numbers will appear for 1 second and you have to guess it back.\n"
              f"2. Guess Game - guess a number and see if you chose like the computer.\n"
              f"3. Currency Roulette - try and guess the value of a random amount of USD in ILS.\n")
        if selected_game.isdigit():
            selected_game = int(selected_game)
        if selected_game == memory_game or selected_game == guess_game or selected_game == currency_roulette_game:
            valid_option = True
        else:
            print("Please enter a valid input.")
    valid_option = False
    while not valid_option:
        difficult_level = int(input("Please choose game difficulty from 1 to 5:\n"))
        if (difficult_level >= 1) and (difficult_level <= 5):
            valid_option = True
            if selected_game == memory_game:
                game = MemoryGame(difficult_level)
            elif selected_game == guess_game:
                game = GuessGame(difficult_level)
            elif selected_game == currency_roulette_game:
                game = CurrencyRouletteGame(difficult_level)
            print(winner_str) if game.play() else print(looser_str)
        else:
            print("Please enter a valid input.")
