import requests
import names
import random
import csv
import string
from random import randint
import time

bank = []

# Number of accounts to create
num = 50

# @example.com
catchall = ""


def create():
    # USER INFO GENERATION
    first_name = names.get_first_name()
    last_name = names.get_last_name()
    email = first_name+last_name+str(randint(100, 999))+catchall
    password = "nftgen$$$"+str(randint(100, 999))
    username = first_name+last_name+str(randint(1, 9))

    bank = [email, password]
    with requests.Session() as c:
        # SIGNUP
        accountdata = '{"email": "'+email+'","password": "'+password+'","username": "' + \
            username+'","name": "'+first_name+'","subscribe": "false","referral": null}'
        headers = {
            'authority': 'api.niftygateway.com',
            'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
            'accept': 'application/json, text/plain, */*',
            'dnt': '1',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://niftygateway.com',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'accept-language': 'en-US,en;q=0.9',
        }
        signup = c.request(
            "POST", "https://api.niftygateway.com/users/signup/", headers=headers, data=accountdata)
        if signup.status_code == 200:
            print(f"Account {email} created successfully.")
            with open("accounts.csv", "a", newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(bank)
        else:
            print(signup.status_code)
            print(signup.text)


for x in range(0, num-1):
    create()
