"""World Of Games

Play some little games, have fun :)
You can execute the game by call package name.

To run the game, write:
start!
after you imported the package.
"""
from wog import MainGame
valid_input = False
start = input("To start the game, please write:\n\"start!\"")
while not valid_input:
    if start == "start!":
        MainGame.start_game()
        valid_input = True
    else:
        print("Invalid input.")
        valid_input = False
