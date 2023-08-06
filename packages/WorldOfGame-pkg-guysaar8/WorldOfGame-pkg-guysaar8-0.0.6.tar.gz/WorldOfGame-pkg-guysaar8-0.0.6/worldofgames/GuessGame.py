#####################
# import modules
#####################
import random
import time
from ManegeGame import GameManager
import os


def print_hello():
    os.system('clear')
    print("Hello! to Guess Game")
    print("you will compete with the all mighty GAME MASTER")


def guess_game(difficulty):
    # Define variables that will be used
    game_id = "Guess Game"
    odds = 0
    out_of_loop = 1
    user_chosen_nums = []

    # Odds by difficulty
    if difficulty == 1:
        odds = 7
    elif difficulty == 2:
        odds = 14
    elif difficulty == 3:
        odds = 21
    elif difficulty == 4:
        odds = 28
    elif difficulty == 5:
        odds = 35

    # Choosing the odds block
    print_hello()

    # Start Guessing game
    # secret = random.randint(1, int(odds))  # random number
    secret = random.randint(1, odds)  # random number

    # get number from user
    os.system('clear')
    print("Let the game begin!")
    print("Guess the number the GAME MASTER has Chosen")
    print("Choose a number between 1 to ", odds)
    checking_list = GameManager.check_if_number()  # get number from user
    choose_num = checking_list[0]
    if_digit = checking_list[1]

    while True:
        if type(choose_num) == int and choose_num == secret:  # if digit and eq to secret num
            print("YOU WON THE GAME!!!")
            print("Kudos for winning on 1 to ", choose_num, " odds")
            print("Trail Number ", out_of_loop, " of ", difficulty)
            print("The number that was chosen was: ", secret)
            time.sleep(5)
            os.system('clear')
            GameManager.again(game_id, difficulty)

        elif out_of_loop >= difficulty:  # check last append
            # check all "if's"
            if (if_digit is True and choose_num > odds) or (not if_digit) or (choose_num in user_chosen_nums):
                generate_random = random.randint(1, odds)
                user_chosen_nums.append(generate_random)
                if generate_random == secret:
                    print("YOU WON THE GAME!!!")
                    print("Kudos for winning on 1 to ", choose_num, " odds")
                    print("Trail Number ", out_of_loop, " of ", difficulty)
                    print("The number that was chosen was: ", secret)
                    time.sleep(5)
                    os.system('clear')
                    GameManager.again(game_id, difficulty)
                else:  # last append is not digit - random number was add
                    print("You Lost To The Game Master")
                    print("Your choices ", user_chosen_nums)
                    print("The number that was chosen was: ", secret)
                    time.sleep(5)
                    GameManager.again(game_id, difficulty)

        elif if_digit is True and choose_num > odds:  # out of range
            os.system('clear')
            generate_random = random.randint(1, odds)
            user_chosen_nums.append(generate_random)
            GameManager.out_of_range()
            print("your choices so far", user_chosen_nums)
            print("Trail Number ", out_of_loop, " of ", difficulty)
            print("Choose a number between 1 to ", odds)

            checking_list = GameManager.check_if_number()
            choose_num = checking_list[0]
            if_digit = checking_list[1]
            out_of_loop += 1
            os.system('clear')

        elif not if_digit:  # not digit
            os.system('clear')
            generate_random = random.randint(1, odds)
            user_chosen_nums.append(generate_random)
            GameManager.invalid_character()
            print("your choices so far", user_chosen_nums)
            print("Trail Number ", out_of_loop, " of ", difficulty)
            print("Choose a number between 1 to ", odds)
            checking_list = GameManager.check_if_number()
            choose_num = checking_list[0]
            if_digit = checking_list[1]
            out_of_loop += 1

            os.system('clear')

        elif type(choose_num) == int and choose_num <= odds and choose_num != secret:
            if choose_num in user_chosen_nums:  # number already in list
                os.system('clear')
                generate_random = random.randint(1, 101)
                user_chosen_nums.append(generate_random)
                GameManager.in_list()
                print("your choices so far", user_chosen_nums)
                print("Trail Number ", out_of_loop, " of ", difficulty)
                print("Choose a number between 1 to ", odds)
                checking_list = GameManager.check_if_number()
                choose_num = checking_list[0]
                if_digit = checking_list[1]
                out_of_loop += 1
                os.system('clear')
            else:  # a good trail, but not eq to secret
                os.system('clear')
                user_chosen_nums.append(choose_num)
                print("nice try")
                print("your choices so far", user_chosen_nums)
                print("Trail Number ", out_of_loop, " of ", difficulty)
                print("Choose a number between 1 to ", odds)
                checking_list = GameManager.check_if_number()
                choose_num = checking_list[0]
                if_digit = checking_list[1]
                out_of_loop += 1
                os.system('clear')
