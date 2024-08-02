import os
import time
import pandas as pd
from dotenv import load_dotenv
from pydantic import ValidationError
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from data_gmail import GmailAccount

load_dotenv()

try:
    info_account = GmailAccount(
        email=os.getenv('EMAIL'),
        password=os.getenv('PASSWORD'),
        new_password=os.getenv('NEW_PASS'),
        first_name=os.getenv('NAME'),
        last_name=os.getenv('LAST_NAME'),
        backup_email=os.getenv('BACKUP_EMAIL')
    )
except ValidationError as e:
    print(f'Something wrong: {e}')
    exit(1)


driver = webdriver.Chrome()


def login(account: GmailAccount):
    driver.get('https://accounts.google.com/')
    time.sleep(2)
    driver.find_element(By.ID, 'identifierId').send_keys(account.email)
    driver.find_element(By.ID, 'identifierId').send_keys(Keys.RETURN)
    time.sleep(1)
    driver.find_element(By.NAME, 'Passwd').send_keys(account.password)
    driver.find_element(By.NAME, 'Passwd').send_keys(Keys.RETURN)
    time.sleep(5)


def change_name(account: GmailAccount):
    driver.get('https://account.google.com/personal-info')
    time.sleep(3)
    driver.find_element(By.PARTIAL_LINK_TEXT, 'Name').send_keys(Keys.RETURN)
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, "[aria-label='Edit Name']").click()
    time.sleep(4)
    driver.find_element(By.ID, 'i7').clear()
    driver.find_element(By.ID, 'i7').send_keys(account.first_name)
    driver.find_element(By.ID, 'i12').clear()
    driver.find_element(By.ID, 'i12').send_keys(account.last_name)
    driver.find_element(By.CLASS_NAME, 'UywwFc-vQzf8d').click()
    time.sleep(5)


def change_password(account: GmailAccount):
    driver.get('https://myaccount.google.com/security')
    time.sleep(2)
    driver.find_element(By.ID, 'i16').click()
    time.sleep(12)
    driver.find_element(By.NAME, 'password').send_keys(account.new_password)
    driver.find_element(By.NAME, 'confirmation_password').send_keys(account.new_password)
    driver.find_element(By.NAME, 'password').send_keys(Keys.RETURN)
    time.sleep(5)


def save_data_to_table(account: GmailAccount):
    data = {
        'Email': [account.email],
        'Password': [account.new_password],
        'First Name': [account.first_name],
        'Last Name': [account.last_name],
        'Backup Email': [account.backup_email]
    }
    df = pd.DataFrame(data)
    if not os.path.exists('data'):
        os.makedirs('data', exist_ok=True)
    file_path = os.path.join('data', 'gmail_account_data.csv')
    df.to_csv(file_path, index=False)


try:
    login(info_account)
    change_name(info_account)
    #change_password(info_account)
    #save_data_to_table(info_account)
finally:
    driver.quit()
