from wog.Live import load_game, welcome


def start_game():
    play_again = True
    valid_input = False
    player_name = input("Hi!\nWhat is your name?\n")
    print(welcome(player_name))
    while play_again:
        play_again = False
        valid_input = False
        load_game()
        while not valid_input:
            user_choice = input("\nDo you want to try again?\nPlease enter \'Yes\' or \'No\'.\n")
            if user_choice == 'Yes':
                valid_input = True
                play_again = True
            elif user_choice == 'No':
                valid_input = True
                play_again = False
            else:
                print("Invalid input.\n")
