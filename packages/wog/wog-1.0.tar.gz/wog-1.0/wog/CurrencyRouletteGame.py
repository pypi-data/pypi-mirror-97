from wog.Game import Game
from currency_converter import CurrencyConverter
from random import randint


class CurrencyRouletteGame(Game):
    def __init__(self, difficulty):
        super().__init__(difficulty)

    @staticmethod
    def __calculate_currency(amount_of_dollars):
        currency_converter = CurrencyConverter()
        exchange_rate = currency_converter.convert(amount_of_dollars, 'USD', 'ILS')
        return exchange_rate

    def __get_money_interval(self, usd_ils_value):
        d = self.difficulty
        t = usd_ils_value
        interval = (t - (5 - d), t + (5 - d))
        return interval

    @staticmethod
    def __get_guess_from_user(amount_of_dollars):
        user_guess = input(f"\nCan you guess what is the exchange rate"
                           f" between {amount_of_dollars} Dollar to Shekel(USD -> ILS)?\n")
        return user_guess

    def play(self):
        rand_num = randint(1, 100)
        user_guess = int(self.__get_guess_from_user(rand_num))
        really_exchange_rate = self.__calculate_currency(rand_num)
        limits_tuple = self.__get_money_interval(really_exchange_rate)
        print(f"\nThe current exchange rate: {self.__calculate_currency(1)}.\n"
              f"{rand_num} x {self.__calculate_currency(1)} = {self.__calculate_currency(rand_num)}")
        if (user_guess >= int(limits_tuple[0])) and (user_guess <= int(limits_tuple[1])):
            return True
        else:
            return False
