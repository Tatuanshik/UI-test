import os
import time
import fake_user_agent
from dotenv import load_dotenv
from pydantic import ValidationError
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from data_twitter import TwitterAccount


load_dotenv()

try:
    info_account = TwitterAccount(
        login=os.getenv('LOGIN'),
        email=os.getenv('EMAIL'),
        password=os.getenv('PASS'),
        new_password=os.getenv('NEW_PASS'),

    )
except ValidationError as e:
    print(f'Something wrong: {e}')
    exit(1)


user = fake_user_agent.user_agent()
options = webdriver.ChromeOptions()
options.add_argument(f'user-agent={user}')

driver = webdriver.Chrome(options=options)


def login(account: TwitterAccount):
    driver.get('https://x.com/i/flow/login')
    time.sleep(5)
    driver.find_element(By.NAME, 'text').send_keys(account.login)
    driver.find_element(By.NAME, 'text').send_keys(Keys.RETURN)
    time.sleep(5)
    driver.find_element(By.NAME, 'password').send_keys(account.password)
    driver.find_element(By.NAME, 'password').send_keys(Keys.RETURN)
    time.sleep(5)


def change_password(account: TwitterAccount):
    driver.get('https://x.com/settings/password')
    time.sleep(5)
    driver.find_element(By.NAME, 'current_password').send_keys(account.password)
    time.sleep(2)
    driver.find_element(By.NAME, 'new_password').send_keys(account.new_password)
    time.sleep(2)
    driver.find_element(By.NAME, 'password_confirmation').send_keys(account.new_password)
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, '[data-testid="settingsDetailSave').click()
    time.sleep(5)


def post_tweet(msg: str):
    driver.get('https://x.com/home')
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, 'div[data-testid="tweetTextarea_0"]').send_keys(msg)
    time.sleep(5)
    driver.find_element(By.CSS_SELECTOR, '[data-testid="tweetButtonInline"]').click()
    time.sleep(5)


try:
    login(info_account)
    change_password(info_account)
    post_tweet('Something')
finally:
    driver.quit()