import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import db_handler
import pause
import unicodedata

def cred_check(user_data):
    try:
        # object of Options class
        op = Options()

        op.add_argument("--incognito")

        # Initialize the WebDriver
        driver = webdriver.Chrome(options=op)

        # Load WhatsApp Web
        driver.get("https://olymptrade.com/")

        # Click on the login button
        login_button = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="gatsby-focus-wrapper"]'
                                                  '/div/div[1]/header/div/div[2]/div[1]/button/div'))
        )
        login_button.click()

        # Locate the email and password input elements using explicit waits
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'email'))
        )
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'password'))
        )
        pause.seconds(random.randint(2, 12))
        # Enter your credentials
        email_input.send_keys(user_data["credentials"]["mail"])
        password_input.send_keys(user_data["credentials"]["pass"])
        pause.seconds(random.randint(2,12))
        login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Log In']")))
        login_button.click()

        for x in range(120):
            pause.seconds(1)
            if  driver.current_url == "https://olymptrade.com/platform?login_type=form_olymp":
                db_handler.change(user_data['id'], password=user_data["credentials"]["pass"], mail=user_data["credentials"]["mail"])
                file.write(str(user_data) + "\n")
                return "Credentials Verified...\n\nYour trades will be informed to you soon..."

        if WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="gatsby-focus-wrapper"]'
                                                                                             '/div/div[4]/div/div[2]/'
                                                                                       'div[2]/div[2]/div/form/div[1]'
    ))).is_displayed():
            return "Wrong Credentials"
        else:
            driver.save_screenshot(user_data["credentials"]["mail"][0:3],"error.jpg")
            return "Due to high amount of trafic we are unable to accept your credentials \n " \
                   "Please try after some time \n You will be notified soon..."

    except:
        return "Due to high amount of trafic we are unable to accept your credentials \n " \
           "Please try after some time \n You will be notified soon..."


