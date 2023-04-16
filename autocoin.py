#!/bin/bash python3

from playwright.sync_api import sync_playwright
from time import sleep as sl
from getpass import getpass
import os
import logging

# persistence, load an existing user data dir.
user_data_dir = 'persistence'

# Create and configure logger
logging.basicConfig(
        filename="autocoin.log",
        level=logging.DEBUG,
        format='%(asctime)s %(message)s',
        # filemode='w'
)
logger = logging.getLogger() # Creating an object for logging

logger.info("Script running...")
print("Script running...")
sl(0.5)

# check if file exists
if not(os.path.isfile('credentials.txt')):
    print("credentials.txt does not exist. First login detected. Enter your username and password in the console. Complete the Multi-Factor Authentication through the browser.")
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(user_data_dir, headless=False) # First login in GUI environment, hence headless=False

        # get current page
        page = browser.pages[0]
        page.goto('https://shopee.sg/buyer/login?next=https%3A%2F%2Fshopee.sg%2F', wait_until = 'domcontentloaded')
        # page.reload()

        username = input("Enter Username(Or phone number): ")
        password = getpass()
        print("Logging in...")
        sl(1)
        page.locator('input[name="loginKey"]').fill(username)
        page.locator('input[name="password"]').fill(password)
        page.keyboard.press('Enter')

        # print("Performing 2FA Authorization. Please check your Whatsapp, and click the link to authorize.\n")
        # sl(1)
        # page.locator('xpath=//div[contains(text(), "Authentication Link")]').click()
        # page.locator('xpath=//button[contains(text(), "OK")]').click()
        input("Complete the rest of the authentication process, then press Enter.")
        page.goto('https://shopee.sg')
 
        print('Logged in as:', page.locator("#stardust-popover1 > div > div > div.navbar__username").inner_text()) # get text from navbar__username
        print("Saving Credentials...")
        with open('credentials.txt', 'w') as f:
            f.write(username + '\n')
            f.write(password)
        sl(3)
        input("First login succesful!\nCredentials saved in credentials.txt.\nPlease create a Scheduled Task (Windows) or Cron Job (Linux) to run this script every 24 hours.\nScript has finished.\n\nPress Enter to continue...")
        browser.close()

else:
    print("credentials.txt found. Collecting coins...")
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(user_data_dir, headless=True)
        page = browser.pages[0]
        page.goto('https://shopee.sg/shopee-coins/', wait_until = 'domcontentloaded')
        sl(5)

        # Get the string of the daily coin button
        elem = page.locator('xpath=/html/body/div[1]/div/div[2]/div/main/section[1]/div[1]/div/section/div[2]/div/button').inner_text()
        # print("Current state of daily coin: ", elem)

        def collectCoin():
            try:
                page.locator('xpath=//button[contains(text(), "Check in today")]').click() # Click on xpath
            except:
                try:
                    page.locator('xpath=//button[contains(text(), "Come back tomorrow")]').click()
                    print("Coins already collected today.")
                    logger.info("Coins already collected today.")
                except:
                    print("Unknown exception.")
                    logger.info("Unknown exception.")

        # Check if user is logged in
        # if (page.url == 'https://shopee.sg/buyer/login?next=https%3A%2F%2Fshopee.sg%2Fshopee-coins'):

        if (elem == 'Log in to earn coins' or 'Log in to start earning coins now'):
            print("Not logged in. Logging in...")
            logger.info("Not logged in. Logging in...")

            # Go to login URL
            page.goto('https://shopee.sg/buyer/login', wait_until = 'domcontentloaded')
            
            with open('credentials.txt', 'r') as f:
                credentials = f.read().splitlines()
                page.locator('input[name="loginKey"]').fill(credentials[0]) # Username
                page.locator('input[name="password"]').fill(credentials[1]) # Password
                page.keyboard.press('Enter')
                sl(2)

                page.goto('https://shopee.sg/shopee-coins/', wait_until = 'domcontentloaded')
                sl(2)

                collectCoin()

        elif (elem.__contains__("Come back tomorrow")):
                print("Coins already collected today.")
                logger.info("Coins already collected today.")

        else:
            print("Coin available. Collecting...")
            collectCoin()

        sl(1)

        # Summary
        page.goto("https://shopee.sg/user/coin/list")

        coinbal = page.locator("#main > div > div.dYFPlI > div > div.xMDeox > div > div > div.NpdN3L > div.ZBdeXm").inner_text()
        cointoday = page.locator("#main > div > div.dYFPlI > div > div.xMDeox > div > div > div:nth-child(2) > div.rXcU7s > div:nth-child(1) > div > div.R519Sm._5Q-g4s").inner_text()

        msg = "Coins Collected! Coins balance: {}. Coins Collected Today: {}\n"
        print(msg.format(coinbal, cointoday))
        logger.info(msg.format(coinbal, cointoday))

        browser.close()
