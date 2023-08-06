#####################
# import modules
#####################
import os
import sys
import time


#####################
# Define class
#####################
class GameManager:
    # set game
    def __init__(self, game_id, difficulty):
        self.game_id = game_id
        self.difficulty = difficulty

    # run game
    @staticmethod
    def run(game_id, difficulty):
        if game_id == "Memory Game":
            from MemoryGame import memory_game
            memory_game(difficulty)

        elif game_id == "Guess Game":
            from GuessGame import guess_game
            guess_game(difficulty)

        elif game_id == "Currency Roulette":
            from CurrencyRoulette import currency_roulette
            currency_roulette(difficulty)

    # play again
    @staticmethod
    def again(game_id, difficulty):
        os.system('clear')
        print("What would you like to do?")
        print("Choose '1'  - to play again (will start with the current difficulty lv)")
        print("Choose '2' - to go back to menu")
        print("Otherwise you will be logged out")
        play_again = input("What is your choice? ")
        if play_again == "1":
            print("game is loading")
            time.sleep(7)
            os.system('clear')
            GameManager.run(game_id, difficulty)
        elif play_again == "2":
            print("game is loading")
            time.sleep(7)
            GameManager.change_game()
        else:
            GameManager.byebye()

    # change game
    @staticmethod
    def change_game():
        from Live import load_game
        os.system('clear')
        game_to_play = load_game()
        game_id = game_to_play[0]
        difficulty = game_to_play[1]
        GameManager.run(game_id, difficulty)

    # check if var is integer
    @staticmethod
    def check_if_number():
        choose_num = input("Insert a number: ")
        if_digit = choose_num.isdigit()
        if if_digit:  # is digit
            choose_num = int(choose_num)
            return [choose_num, if_digit]
        else:
            try:
                choose_num = float(choose_num)
                return [choose_num, if_digit]
            except ValueError:
                choose_num = str(choose_num)
                return [choose_num, if_digit]

    # exit game
    @staticmethod
    def byebye():
        os.system('clear')
        print('DO NOT MESS WITH THE GAME MASTER')
        print('BYE BYE')
        time.sleep(10)
        sys.exit()

    # print error - number was not in the list
    @staticmethod
    def in_list():
        print('DO NOT MESS WITH THE GAME MASTER')
        print("You typed a number that was already in the list")
        print("There for a random number was added")

    # print error - not a valid char
    @staticmethod
    def invalid_character():
        print('DO NOT MESS WITH THE GAME MASTER')
        print("You typed invalid character!!!")
        print("There for a random number was added")

    # print error - out of valid range
    @staticmethod
    def out_of_range():
        print("You were out of range")
        print("There for a random number was added")
        print("There for a random number was added")
