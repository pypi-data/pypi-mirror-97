#####################
# import modules
#####################
import os
from ManegeGame import GameManager


#####################
# Define functions
#####################

def game_list():  # print to screen game list
    print("*" * 70)
    print("Which game would you like to play?")
    print("1. Memory Game - a sequence of numbers will appear for 1 second and you have to guess it back")
    print("2. Guess Game - guess a number and see if you chose like the computer")
    print("3. Currency Roulette - try and guess the value of a random amount of USD in ILS")
    print("*" * 70)
    print("Please choose a game from: (choose number 1-3)")


def invalid_character():  # print to screen invalid char message
    print('DO NOT MESS WITH THE GAME MASTER')
    print("You typed invalid character!!!")


def memory_rules():  # print to screen memory_rules
    print("Memory Game Rules:")
    print("*" * 70)
    print("Choosing difficulty will affect your chance of winning")
    print("For example:")
    print("difficulty 5 will generate 5 numbers between 1 to 101 the you will have to guess which is it"
          "all currently")
    print("difficulty 4 will generate 4 numbers between 1 to 101 the you will have to guess which is it"
          "all currently")
    print("And so on...")
    print("*" * 70)


def guess_rules():  # print to screen guess_rules
    print("Guess Game Rules:")
    print("*" * 70)
    print("Choosing difficulty will affect your chance of winning")
    print("For example:")
    print("difficulty 5 will have to guess a number between 1 to  35")
    print("difficulty 4 will have to guess a number between 1 to  28")
    print("And so on...")
    print("*" * 70)


def currency_rules():  # print to screen currency_rules
    print("Currency Rules:")
    print("*" * 70)
    print("You will need to answer how much ILS is equal to US Dollars")
    print("How much is 10$ in ILS?")
    print("Choosing difficulty will  affect your chance of winning")
    print("For example:")
    print("Difficulty 1 will give you a range of accuracy - 1 = (-/+)5")
    print("Difficulty 2 will give you a range of accuracy - 2 = (-/+)4")
    print("And so on...")
    print("*" * 70)


def reset_var():  # Define variables that will be used in the script function
    if_digit = 'false'
    out_of_loop = 1
    difficulty_list = 'Null'
    game_name = 'Null'
    check_list = 'Null'
    return [if_digit, out_of_loop, difficulty_list, game_name, check_list]


def load_game():  # loading will get the game_id and difficulty
    # Define variables
    game_id = 0
    reset_var()
    get_list = reset_var()
    out_of_loop = get_list[1]

    # Choose a game
    game_list()
    check_list = GameManager.check_if_number()
    choose_num = check_list[0]
    if_digit = check_list[1]

    os.system('clear')  # clear screen

    # check if input is valid
    while True:
        if if_digit is True and 3 >= choose_num >= 1:  # is digit and in range
            print("have fun")
            import time
            time.sleep(3)
            os.system('clear')  # clear screen
            break
        else:
            if out_of_loop <= 3:  # up to 3 times typed invalid char
                invalid_character()
                print("And make sure you insert a number between 1 - 3,")
                out_of_loop = out_of_loop + 1
                game_list()
                check_list = GameManager.check_if_number()
                choose_num = check_list[0]
                if_digit = check_list[1]

                os.system('clear')  # clear screen

            if out_of_loop > 3:  # more than 3 times typed invalid char
                out_of_loop += 1
                invalid_character()
                game_list()
                check_list = GameManager.check_if_number()
                choose_num = check_list[0]
                if_digit = check_list[1]

                os.system('clear')  # clear screen

            if out_of_loop > 6:  # 6 trails and the users is logged of from app
                GameManager.byebye()

    # Define variables
    reset_var()
    get_list = reset_var()
    out_of_loop = get_list[1]

    # Define game id
    if choose_num == 1:
        game_id = 'Memory Game'
    elif choose_num == 2:
        game_id = 'Guess Game'
    elif choose_num == 3:
        game_id = 'Currency Roulette'

    os.system('clear')  # clear screen

    # Choose difficulty
    print("You will play " + game_id)
    if game_id == "Memory Game":
        memory_rules()
    elif game_id == 'Guess Game':
        guess_rules()
    elif game_id == 'Currency Roulette':
        currency_rules()

    print("Choose game difficulty from 1 to 5")
    difficulty_list = GameManager.check_if_number()
    choose_num = difficulty_list[0]
    if_digit = difficulty_list[1]

    os.system('clear')  # clear screen

    while True:
        if if_digit is True and 1 <= choose_num <= 5:  # is int and in range
            print("you choose game " + game_id + " and difficulty level ", choose_num)
            break
        else:  # up to 6 times invalid char
            if out_of_loop < 6:
                out_of_loop += 1
                invalid_character()
                print("try again")
                print("You will play " + game_id)
                if game_id == "Memory Game":
                    memory_rules()
                elif game_id == 'Guess Game':
                    guess_rules()
                elif game_id == 'Currency Roulette':
                    currency_rules()
                print("Please choose game difficulty from 1 to 5: ")
                difficulty_list = GameManager.check_if_number()
                choose_num = difficulty_list[0]
                if_digit = difficulty_list[1]
                os.system('clear')
            else:  # 6 trails and the users is logged of from app
                GameManager.byebye()

    # return values
    difficulty = choose_num
    return [game_id, difficulty]
