#####################
# import modules
#####################
import json
import os


#####################
# Define functions
#####################
def singin():  # say hello to new user
    print("Hello Rookie and welcome to the World Of Games (WoG)")
    print("Before we begin, the best experience of your life")
    print("You need to create a new account")
    pass


def welcome(logon_name):  # say hello to user
    print("Hello " + logon_name + " and welcome to the World Of Games (WoG)")
    print("Here you can find many cool games to play")


def loging():
    # Loads Accounts DB
    with open('account_db.json') as account_db:
        accounts = json.load(account_db)

    # get username
    os.system('clear')
    logon_name = input("What is your log on name: ")  # Get Logon name
    logon_name = logon_name.upper()

    # check if username exist
    while True:
        try:
            if accounts[logon_name]:
                os.system('clear')
                break
        except KeyError:  # if user does not exist user will be created and added to json
            os.system('clear')
            singin()
            account_name = input("Insert your new account name: ")
            account_name = account_name.upper()
            accounts[account_name] = 'account_info'
            with open('account_db.json', "w") as account_db:
                json.dump(accounts, account_db)
            logon_name = account_name

    return logon_name
