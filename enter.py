import time
from random import randint
import os
import zipfile
from selenium import webdriver
import csv
from selenium.webdriver.common.keys import Keys

# url for niftygateway drawing
url = 'https://niftygateway.com/enterdrawing/?contractAddress=0x374e4a05e665f25b6c996ec2eeae05c792359821&niftyType=12'

PROXY_HOST = '000.00.000.00'  # rotating proxy or host
PROXY_PORT = 11111  # port
PROXY_USER = ''  # username
PROXY_PASS = ''  # password

# request params
manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""

background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
        }
    };

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
""" % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)


def get_chromedriver(use_proxy=False, user_agent=None):
    path = os.path.dirname(os.path.abspath(__file__))
    chrome_options = webdriver.ChromeOptions()
    if use_proxy:
        pluginfile = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options.add_extension(pluginfile)
    if user_agent:
        chrome_options.add_argument('--user-agent=%s' % user_agent)
    driver = webdriver.Chrome(
        os.path.join(path, 'chromedriver'),
        chrome_options=chrome_options)
    return driver


def main():
    user = []
    bank = []

    # Import accounts to enter
    with open('accounts.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        user = next(csvreader)
        for row in csvreader:
            bank.append(row)

    # Navigate site and enter queue for purchase
    for user in bank:
        driver = get_chromedriver(use_proxy=True)
        driver.get('https://niftygateway.com/validate-profile')
        time.sleep(1)
        try:
         element = driver.find_element_by_xpath(
             '/html/body/div/div/div[2]/div[2]/div[1]/form/div[1]/div/input')
         element.send_keys(user[0])
         element = driver.find_element_by_xpath(
             '/html/body/div/div/div[2]/div[2]/div[1]/form/div[2]/div/input')
         element.send_keys(user[1])
         time.sleep(1)
         element = driver.find_element_by_xpath(
             '/html/body/div/div/div[2]/div[2]/div[1]/form/button/span[1]')
         element.click()
         time.sleep(1)
         driver.get(url)
 
         element = driver.find_element_by_xpath(
             '/html/body/div/div/div[2]/div/div[4]/div/div')
         time.sleep(1)
         element.click()
         time.sleep(1)
         driver.close()
        except:
         driver.close()


main()
