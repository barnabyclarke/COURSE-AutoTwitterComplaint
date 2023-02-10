# import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import time

PROMISED_UP = 75
PROMISED_DOWN = 500
EMAIL = "x"
PASSWORD = "x"
PHONE = "x"


class InternetSpeedTwitterBot:

    def __init__(self):
        self.down = 0
        self.up = 0
        self.chrome_driver_path = Service("C:/Users/BC/Development/chromedriver.exe")
        self.driver = webdriver.Chrome(service=self.chrome_driver_path)

    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")
        self.driver.maximize_window()

        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(
            (By.ID, 'onetrust-accept-btn-handler')
        )).click()  # Accept cookies
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(
            (By.CLASS_NAME, 'notification-dismiss')
        )).click()  # Close notification
        WebDriverWait(self.driver, 1).until(EC.element_to_be_clickable(
            (By.CLASS_NAME, 'start-text')
        )).click()  # Run speed test
        WebDriverWait(self.driver, 50).until(EC.visibility_of_element_located(
            (By.CLASS_NAME, 'result-label')
        ))  # Pauses until run is done
        time.sleep(2)
        self.driver.find_element(
            By.XPATH, '/html/body/div[3]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[8]/div/a'
        ).click()  # Close pop-up
        self.down = float(self.driver.find_element(
            By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/'
                      'div[1]/div[1]/div/div[2]/span'
        ).text)  # Get download speed
        self.up = float(self.driver.find_element(
            By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/'
                      'div[1]/div[2]/div/div[2]/span'
        ).text)  # Get upload speed
        if self.up > PROMISED_UP and self.down > PROMISED_DOWN:
            self.driver.quit()  # If up and down are both good, Chrome closes

    def tweet_at_provider(self):
        self.driver.get("https://twitter.com/i/flow/login")

        # # LOGIN
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/'
                       'div[5]/label/div/div[2]/div/input')
        )).send_keys(EMAIL)  # Input email
        action = ActionChains(self.driver)
        action.send_keys(Keys.ENTER).perform()  # Hit enter
        try:
            WebDriverWait(self.driver, 1).until(EC.visibility_of_element_located(
                (By.XPATH,
                 '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/'
                 'div/label/div/div[2]/div[1]/input')
            )).send_keys(PASSWORD)  # Input password
            action = ActionChains(self.driver)
            action.send_keys(Keys.ENTER).perform()  # Hit enter
        except TimeoutException:
            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/'
                           'div[2]/label/div/div[2]/div/input')
            )).send_keys(PHONE)  # Input phone
            action = ActionChains(self.driver)
            action.send_keys(Keys.ENTER).perform()  # Hit enter
            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/'
                           'div/div[3]/div/label/div/div[2]/div[1]/input')
            )).send_keys(PASSWORD)  # Input password
            action = ActionChains(self.driver)
            action.send_keys(Keys.ENTER).perform()  # Hit enter

        # # Tweet
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(
            (By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/'
                       'div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/'
                       'div/div[2]/div/div/div/div')
        )).send_keys(f"@ Why do I have an internet speed of {self.down}Mbps download and {self.up}Mbps upload "
                     f"speed when I pay for {PROMISED_DOWN}Mbps download and {PROMISED_UP}Mbps upload.")
        # ^^ Input text to Tweet ^^
        self.driver.find_element(
            By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/'
                      'div/div/div[2]/div[3]/div/div/div[2]/div[3]/div/span/span'
        ).click()  # Send Tweet

        self.driver.quit()
