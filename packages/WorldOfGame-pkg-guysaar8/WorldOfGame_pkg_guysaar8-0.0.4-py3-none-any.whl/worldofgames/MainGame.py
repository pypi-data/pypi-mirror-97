#####################
# Import modules
#####################
from UserAccount import loging, welcome
from Live import load_game
from ManegeGame import GameManager


#####################
# Define Functions
#####################

def log():
    # initiate login
    user = loging()
    welcome(user)
    return user


def start():
    # pick a game
    load_game_list = load_game()
    game_id = load_game_list[0]
    difficulty = load_game_list[1]

    print("You will Play = ", game_id, "Difficulty = ", difficulty)

    # load the chosen game

    game_to_play = GameManager(game_id, difficulty)
    game_to_play.run(game_id, difficulty)


#####################
# START
#####################

log()

start()
