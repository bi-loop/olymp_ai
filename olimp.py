import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pause
from selenium.webdriver.chrome.service import Service
from pyvirtualdisplay import Display
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def cred_check(user_id, mail, password):
    try:
        # display = Display(visible=1, size=(800, 600))
        # display.start()
        option = webdriver.ChromeOptions()
        # Initialize the WebDriver
        option.add_experimental_option("excludeSwitches", ["enable-automation"])
        option.add_experimental_option('useAutomationExtension', False)

        # For ChromeDriver version 79.0.3945.16 or over
        option.add_argument('--disable-blink-features=AutomationControlled')
        option.add_argument("window-size=1280,800")
        option.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")
        service = Service(ChromeDriverManager().install())

        # Initialize WebDriver with the Service object and options
        driver = webdriver.Chrome(service=service, options=option)

        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

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
        email_input.send_keys(mail)
        password_input.send_keys(password)
        pause.seconds(2)
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Log In']")))
        login_button.click()

        for x in range(60):
            pause.seconds(1)
            if driver.current_url == "https://olymptrade.com/platform?login_type=form_olymp":
                return True

        if WebDriverWait(driver, 4).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="gatsby-focus-wrapper"]'
                                                            '/div/div[4]/div/div[2]/'
                                                            'div[2]/div[2]/div/form/div[1]'
                                                  ))).is_displayed():
            print("Invalid Error Displayed")
            driver.save_screenshot(str(user_id) + "error.png")
            driver.close()
            return False

        else:
            driver.save_screenshot(str(user_id) + "error.png")
            print('Check Error Image')
            driver.close()
            return False

    except Exception as e:
        print(e)
        return False

