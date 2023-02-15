import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time

PROMISED_DOWN = 150
PROMISED_UP = 10
TWITTER_USERNAME = os.environ.get("TWITTER_USERNAME")
TWITTER_PASSWORD = os.environ.get("TWITTER_PASSWORD")


class InternetSpeedTwitterBot:

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)

        self.driver = webdriver.Chrome(service=Service("D:\Development\chromedriver.exe"), options=chrome_options)
        self.down = 0
        self.up = 0

    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")
        time.sleep(3)

        # Deal with cookies -> click on show options and then click on save preferences
        try:
            self.driver.find_element(By.ID, "onetrust-pc-btn-handler").click()
        except NoSuchElementException:
            pass
        else:
            time.sleep(2)
            self.driver.find_element(By.CLASS_NAME, "save-preference-btn-handler").click()

        self.driver.find_element(By.CLASS_NAME, "start-text").click()
        time.sleep(60)

        self.down = float(self.driver.find_element(By.CSS_SELECTOR, ".result-item-download .result-data-value").text)
        self.up = float(self.driver.find_element(By.CSS_SELECTOR, ".result-item-upload .result-data-value").text)

        # print(f"Download {self.down}\nUpload {self.up}")

    def tweet_at_provider(self, message):
        self.driver.get("https://www.twitter.com/")
        time.sleep(3)
        self.driver.find_element(By.LINK_TEXT, "Zaloguj się").click()
        time.sleep(4)

        login = self.driver.find_element(By.NAME, "text")
        login.send_keys(TWITTER_USERNAME)
        login.send_keys(Keys.ENTER)
        time.sleep(3)
        password = self.driver.find_element(By.NAME, "password")
        password.send_keys(TWITTER_PASSWORD)
        password.send_keys(Keys.ENTER)

        time.sleep(5)
        self.driver.find_element(By.CSS_SELECTOR, "a[data-testid='SideNav_NewTweet_Button'").click()

        time.sleep(2)
        tweet = self.driver.find_element(By.CLASS_NAME, "public-DraftStyleDefault-block")
        tweet.send_keys(message)

        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, "div[data-testid='tweetButton']").click()


bot = InternetSpeedTwitterBot()
bot.get_internet_speed()

if bot.down < PROMISED_DOWN or bot.up < PROMISED_UP:
    bot.tweet_at_provider(
        f"Hey Internet Provider, "
        f"why is my internet speed {bot.down}down/{bot.up}up when I pay for {PROMISED_DOWN}down/{PROMISED_UP}up?"
    )
