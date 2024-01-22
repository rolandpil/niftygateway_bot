import requests
import logging
import urllib.parse
import csv
import json
import re
import time

# logging.basicConfig(level=logging.DEBUG)
# Get from smspva.com
API_KEY = ''
# Get from any niftygateway page
CLIENT_ID = ''

a = open("verified.csv", "x")
a.close()


def main():
    # IMPORT EMAIL AND PASSWORD
    user = []
    bank = []

    with open('accounts.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        user = next(csvreader)
        for row in csvreader:
            bank.append(row)

    for user in bank:
        email = user[0].lower()
        print(email)
        password = user[1]
        with requests.Session() as c:

            # LOGIN
            c.headers.update({
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"})
            proxies = {
                # http://user:pass@ip:port
                'http': ''}
            c.proxies.update(proxies)
            c.get("https://niftygateway.com/")

            # ENCODE EMAIL AND PASSWORD FOR URL
            password = urllib.parse.quote(password)
            email = urllib.parse.quote(email)

            payload = 'grant_type=password&client_id=' + \
                CLIENT_ID+'&password='+password+'&username='+email
            headers = {
                'authority': 'api.niftygateway.com',
                'accept': 'application/json, text/plain, */*',
                'dnt': '1',
                'sec-ch-ua-mobile': '?0',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://niftygateway.com',
                'sec-fetch-site': 'same-site',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'accept-language': 'en-US,en;q=0.9',
            }

            response = c.request(
                "POST", "https://api.niftygateway.com/o/token/", headers=headers, data=payload)
            access_token = json.loads(response.text)['access_token']
            bearer_token = "Bearer "+access_token

            # GET PHONE NUMBER
            i = True
            while i:
                getnumber = requests.get(
                    f'http://smspva.com/priemnik.php?metod=get_number&country=FR&service=opt19&apikey={API_KEY}')
                number_info = json.loads(getnumber.text)
                if number_info['response'] != '1':
                    time.sleep(10)
                else:
                    i = False
                    print(
                        f"Phone number: {number_info['number']}, id {number_info['id']}")
                    phonenumber = number_info['number']
                    indices = [0, 1, 3, 5, 7]
                    t = [phonenumber[i:j]
                         for i, j in zip(indices, indices[1:]+[None])]
                    # THIS HAS TO BE EDITED BASED ON REGION
                    formatted_phonenumber = urllib.parse.quote(
                        "+33" + t[0] + " " + t[1] + " " + t[2] + " " + t[3] + " " + t[4])
            payload = "to=" + formatted_phonenumber
            # ENTER PHONE NUMBER
            url = "https://api.niftygateway.com//user/verification/"
            payload = payload
            headers = {
                'authority': 'api.niftygateway.com',
                'accept': 'application/json, text/plain, */*',
                'dnt': '1',
                'authorization': bearer_token,
                'sec-ch-ua-mobile': '?0',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://niftygateway.com',
                'sec-fetch-site': 'same-site',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'accept-language': 'en-US,en;q=0.9',
            }

            response = requests.request(
                "POST", url, headers=headers, data=payload)
            print(response.text)
            if response.status_code == 400:
                print("Removing old number and adding new one.")
                url = "https://api.niftygateway.com//user/verification/"

                payload = {}
                headers = {
                    'authority': 'api.niftygateway.com',
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

                response = requests.request(
                    "DELETE", url, headers=headers, data=payload)

                url = "https://api.niftygateway.com//user/verification/"
                payload = "to=" + formatted_phonenumber
                headers = {
                    'authority': 'api.niftygateway.com',
                    'accept': 'application/json, text/plain, */*',
                    'dnt': '1',
                    'authorization': bearer_token,
                    'sec-ch-ua-mobile': '?0',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
                    'content-type': 'application/x-www-form-urlencoded',
                    'origin': 'https://niftygateway.com',
                    'sec-fetch-site': 'same-site',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-dest': 'empty',
                    'accept-language': 'en-US,en;q=0.9',
                }

                response = requests.request(
                    "POST", url, headers=headers, data=payload)

            # CHECK FOR CODE
            a = True
            attempt = 0
            while a:
                time.sleep(10)

                # GET SMS CODE
                print("Searching for code")
                getcode = requests.get(
                    f'http://smspva.com/priemnik.php?metod=get_sms&country=FR&service=opt19&id={number_info["id"]}&apikey={API_KEY}')
                code_info = json.loads(getcode.text)
                if code_info['response'] == '1':
                    code = re.findall(r'[0-9]+', code_info['text'])[0]
                    print(f"Found code {code}")

                    # ENTER CODE

                    url = "https://api.niftygateway.com//user/verification/"

                    payload = 'code='+code
                    headers = {
                        'authority': 'api.niftygateway.com',
                        'accept': 'application/json, text/plain, */*',
                        'dnt': '1',
                        'authorization': bearer_token,
                        'sec-ch-ua-mobile': '?0',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
                        'content-type': 'application/x-www-form-urlencoded',
                        'origin': 'https://niftygateway.com',
                        'sec-fetch-site': 'same-site',
                        'sec-fetch-mode': 'cors',
                        'sec-fetch-dest': 'empty',
                        'accept-language': 'en-US,en;q=0.9',
                    }

                    response = requests.request(
                        "PUT", url, headers=headers, data=payload)
                    a = False
                    if response.status_code == 200:
                        with open("verified.csv", "a", newline='') as csvfile:
                            csvwriter = csv.writer(csvfile)
                            csvwriter.writerow([user[0], user[1]])
                    else:
                        print("ERROR BINDING PHONE NUMBER")
                        print(response.text)
                if attempt == 15:
                    print("Timeout")
                    a = False
                attempt += 1


main()
