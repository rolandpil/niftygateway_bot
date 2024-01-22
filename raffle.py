import urllib
import requests
import csv
import json
from dhooks import Webhook, Embed

# Used for entering timed raffles

# Get from drawing page
CONTRACT_ADDRESS = ''
NIFFTY_TYPE = '3'

# Discord webhooks
webhook = ""
errorhook = ""
hook = Webhook(webhook)
ehook = Webhook(errorhook)

# https://user:pass@ip:port
proxy = ''
# Get from any niftygateway page
CLIENT_ID = ''


def main():
    user = []
    bank = []

    with open('accounts.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        user = next(csvreader)
        for row in csvreader:
            bank.append(row)

    for user in bank:
        with requests.Session() as c:
            # LOGIN
            c.headers.update({
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"})
            proxies = {
                'https': proxy}
            c.proxies.update(proxies)
            c.get("https://niftygateway.com/", proxies=proxies)

            # ENCODE EMAIL AND PASSWORD FOR URL
            password = urllib.parse.quote(user[1])
            email = urllib.parse.quote(user[0]).lower()
            print(email)

            payload = 'grant_type=password&client_id=' + \
                CLIENT_ID+'&password='+password+'&username='+email
            headers = {
                'authority': 'api.niftygateway.com',
                'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
                'accept': 'application/json, text/plain, */*',
                'dnt': '1',
                'sec-ch-ua-mobile': '?0',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'httpss://niftygateway.com',
                'sec-fetch-site': 'same-site',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'accept-language': 'en-US,en;q=0.9',

            }

            response = requests.request(
                "POST", "https://api.niftygateway.com/o/token/", headers=headers, data=payload, proxies=proxies)
            print(response)
            print(response.text)
            access_token = json.loads(response.text)['access_token']
            bearer_token = "Bearer "+access_token

            # GET CARD ID
            url = "https://api.niftygateway.com/stripe/list-cards/"

            payload = {}
            headers = {

                'authority': 'api.niftygateway.com',
                'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
                'accept': 'application/json, text/plain, */*',
                'dnt': '1',
                'authorization': bearer_token,
                'sec-ch-ua-mobile': '?0',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
                'origin': 'https://niftygateway.com',
                'sec-fetch-site': 'same-site',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'accept-language': 'en-US,en;q=0.9',
            }
            try:
                response = c.request(
                    "GET", url, headers=headers, data=payload, proxies=proxies)
                print(response.text)
                CARD_ID = json.loads(response.text)['data'][0]['id']
                FINGERPRINT = json.loads(response.text)[
                    'data'][0]['fingerprint']

                url = "https://api.niftygateway.com/drawing/enter/"

                payload = '{\"contractAddress\":\"'+CONTRACT_ADDRESS + \
                    '\",\"niftyType\":'+NIFFTY_TYPE + \
                    ',\"paymentType\":\"card\",\"cc_token\":\"' + \
                    CARD_ID+'\",\"fingerprint\":\"'+FINGERPRINT+'\"}'

                headers = {
                    'authority': 'api.niftygateway.com',
                    'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
                    'accept': 'application/json, text/plain, */*',
                    'dnt': '1',
                    'authorization': bearer_token,
                    'sec-ch-ua-mobile': '?0',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
                    'content-type': 'application/json;charset=UTF-8',
                    'origin': 'https://niftygateway.com',
                    'sec-fetch-site': 'same-site',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-dest': 'empty',
                    'accept-language': 'en-US,en;q=0.9',
                }

                response = c.request(
                    "POST", url, headers=headers, data=payload, proxies=proxies)
                try:
                    success = json.loads(response.text)
                except:
                    pass
                try:
                    if success['didSucceed'] == True:
                        embed = Embed(
                            description=f'Entered {user[0]} on {CONTRACT_ADDRESS}',
                            color=0x5CDBF0,
                            timestamp='now'  # sets the timestamp to current time
                        )
                        hook.send(embed=embed)

                    if success['didSucceed'] == False:
                        embed = Embed(
                            description=f'Error entering {user[0]} on {CONTRACT_ADDRESS}\n \n Error: {success["errorType"]}',
                            color=0x5CDBF0,
                            timestamp='now'  # sets the timestamp to current time
                        )
                        ehook.send(embed=embed)
                except:
                    pass

                print(response.text)
            except:
                print(f"Error {user[0]}")


main()
