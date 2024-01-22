import requests
import json
from dhooks import Webhook, Embed
import time

# Checks total entries for a raffle and logs it to a discord webhook


def main():
    # Discord webhook for logging
    webhook = ""
    hook = Webhook(webhook)

    url = "https://api.niftygateway.com//nifty/metadata-unminted/"

    # Enter contract address
    # Visit page to get valid bearer token and cookie
    payload = '{"contractAddress":"","niftyType":"1","cancelToken":{"promise":{}},"timeout":30000}'
    headers = {
        'authority': 'api.niftygateway.com',
        'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
        'accept': 'application/json, text/plain, /',
        'authorization': '',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        'content-type': 'application/json',
        'origin': 'https://niftygateway.com/',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'accept-language': 'en-US,en;q=0.9',
        'Cookie': ''
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    jsonresponse = json.loads(response.text)

    embed = Embed(
        description=f'Entrycount: {jsonresponse["niftyMetadata"]["drawingInfo"]["totalEntryCount"]}',
        color=0x5CDBF0,
        timestamp='now'  # sets the timestamp to current time
    )
    print(
        f'Entrycount: {jsonresponse["niftyMetadata"]["drawingInfo"]["totalEntryCount"]}')
    hook.send(embed=embed)

    time.sleep(60)
    main()


main()
