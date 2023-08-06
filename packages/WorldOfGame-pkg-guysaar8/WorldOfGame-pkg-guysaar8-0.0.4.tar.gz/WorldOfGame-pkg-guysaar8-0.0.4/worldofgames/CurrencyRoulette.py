#####################
# import modules
#####################
import random
import os
import time
from ManegeGame import GameManager
import requests
import json


###################
# Define functions
#####################

# print hello
def print_hello():
    os.system('clear')
    print("Hello! to Currency Roulette")
    print("you will compete with the all mighty GAME MASTER")


def currency_roulette(difficulty):

    # reset variables
    out_of_loop = 1
    user_chosen_nums = []
    range_app = 0
    odds = 0
    game_id = "Currency Roulette"

    # Odds by difficulty and range
    if difficulty == 1:
        odds = 1
        range_app = 5
    elif difficulty == 2:
        odds = 2
        range_app = 4
    elif difficulty == 3:
        odds = 4
        range_app = 3
    elif difficulty == 4:
        odds = 4
        range_app = 2
    elif difficulty == 5:
        odds = 5
        range_app = 1
    # Choosing the odds block
    print_hello()
    print("Difficulty lv is ", odds, " you win, long as your pick is in range of */- ", range_app,
          " from the correct amount")

    # generate random dollar number
    dollar = random.randint(1, 101)

    os.system('clear')

    # get rest API of current USD to ILS
    print("Let the game begin!")
    print("Getting current Dollar rate")
    response = requests.get("https://openexchangerates.org/api/latest.json?app_id=55bb2564d5e3467e9806631f5d7144b3")
    response_j = json.loads(response.content)
    dollar_rate = float(response_j['rates'].get('ILS'))  # change to float
    ils = round(dollar * dollar_rate, 2)  # round to hundredth

    print("How much is ", dollar, "$ in ILS")
    checking_list = GameManager.check_if_number()  # get number from user
    choose_num = checking_list[0]

    while True:
        if (type(choose_num) == int or type(choose_num) == float) and \
                (ils - range_app) <= choose_num <= (ils + range_app):  # if user has won
            os.system('clear')
            user_chosen_nums.append(choose_num)
            print("your choices so far", user_chosen_nums)
            print("you won")
            time.sleep(5)
            print("*" * 70)
            GameManager.again(game_id, difficulty)
        else:
            # check last append
            if out_of_loop == 3:
                generate_random = random.randint(1, 350)
                user_chosen_nums.append(generate_random)
                # last append was invalid
                if (choose_num in user_chosen_nums) or (type(choose_num) == str):
                    os.system('clear')
                    # generate random number
                    generate_random = random.randint(1, 350)
                    user_chosen_nums.append(generate_random)
                    # if random number is eq to secret
                    if (type(generate_random) == int or type(generate_random) == float) and \
                            (ils - range_app) <= choose_num <= (ils + range_app):  # if user has won
                        os.system('clear')
                        user_chosen_nums.append(choose_num)
                        print("your choices so far", user_chosen_nums)
                        print("you won")
                        time.sleep(5)
                        print("*" * 70)
                        GameManager.again(game_id, difficulty)
                    else:
                        print("You lost")
                        print("Your choices", user_chosen_nums)
                        print("The correct answer is:", ils)
                        print("The USD rete is: ", dollar_rate)
                        time.sleep(5)
                        print("*" * 70)
                        GameManager.again(game_id, difficulty)

                else:  # good trail but didn't win
                    os.system('clear')
                    user_chosen_nums.append(choose_num)
                    print("You lost")
                    print("Your choices", user_chosen_nums)
                    print("The correct answer is:", ils)
                    print("The USD rete is: ", dollar_rate)
                    time.sleep(5)
                    print("*" * 70)
                    GameManager.again(game_id, difficulty)

            elif type(choose_num) == str:  # if is a string
                os.system('clear')
                out_of_loop += 1
                generate_random = random.randint(1, 350)
                user_chosen_nums.append(generate_random)
                GameManager.invalid_character()
                print('Try again')
                print("your choices so far", user_chosen_nums)
                print("How much is ", dollar, "$ in ILS")
                checking_list = GameManager.check_if_number()
                choose_num = checking_list[0]
                os.system('clear')
            else:
                if choose_num in user_chosen_nums:  # check if already in the list
                    out_of_loop += 1
                    os.system('clear')
                    generate_random = random.randint(1, 350)
                    user_chosen_nums.append(generate_random)
                    GameManager.in_list()
                    print("your choices so far", user_chosen_nums)
                    print("How much is ", dollar, "$ in ILS")
                    print("try again")
                    checking_list = GameManager.check_if_number()
                    choose_num = checking_list[0]
                else:  # good trail but didn't win
                    out_of_loop += 1
                    os.system('clear')
                    user_chosen_nums.append(choose_num)
                    print("your choices so far", user_chosen_nums)
                    print("How much is ", dollar, "$ in ILS")
                    print("try again")
                    checking_list = GameManager.check_if_number()
                    choose_num = checking_list[0]
