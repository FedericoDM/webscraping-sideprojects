# Class - DriverManager
# Author - FedericoDM
# Description - This class is used to manage the driver and browser instances

import time
import selenium
from selenium.webdriver import Chrome
from selenium.webdriver.chrome import webdriver as chrome_webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Local imports
from utils.constants import TIMEOUT, SCROLL_PAUSE_TIME


class DriverManager:
    TIMEOUT = TIMEOUT
    SCROLL_PAUSE_TIME = SCROLL_PAUSE_TIME

    def __init__(self, localtest, headless, download_location):
        self.localtest = localtest
        self.download_location = download_location
        self.headless = headless
        self.driver = self._get_chrome_driver()
        self.action = ActionChains(self.driver)

    def _get_chrome_driver(self):
        chrome_options = chrome_webdriver.Options()
        chrome_options.add_argument("--no-sandbox")

        if self.headless:
            chrome_options.add_argument("--headless")

        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-gpu")

        # service = Service(self.download_location)
        driver_path = self.download_location

        print(driver_path)
        driver = Chrome(executable_path=driver_path, options=chrome_options)
        print("Got driver successfully")

        return driver

    def get_page(self, page):
        """
        Navigates to a particular webpage
        """
        self.driver.get(page)

    def click_by_xpath(self, xpath):
        """
        Clicks desired XPath
        """
        button = WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        try:
            button = WebDriverWait(self.driver, self.TIMEOUT).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            print("Hovering to button")
            self.action.move_to_element(button)
            self.action.perform()
            button.click()
        except Exception as error:
            print(str(error))
            self.driver.execute_script("arguments[0].click();", button)
        return button

    def hover_by_xpath(self, xpath):
        """
        Function receives an xpath and hovers over such element
        """
        button = WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        self.action.move_to_element(button)
        self.action.perform()

    def click_by_iden(self, iden):
        """
        Clicks element found by id
        """
        WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.presence_of_element_located((By.ID, iden))
        )
        try:
            button = WebDriverWait(self.driver, TIMEOUT).until(
                EC.element_to_be_clickable((By.ID, iden))
            )
            print("Hovering to button")
            self.action.move_to_element(button)
            self.action.perform()
            button.click()
        except Exception as error:
            print(str(error))
            self.driver.execute_script("arguments[0].click();", button)

        return button

    def scroll_down(self):
        """
        Scrolls down until the bottom of the page is reached
        """
        # Get the initial page height
        last_height = self.driver.execute_script(
            "return document.body.scrollHeight"
        )

        while True:
            # Scroll down to the bottom
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )

            # Wait for new content to load
            time.sleep(self.SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last height
            new_height = self.driver.execute_script(
                "return document.body.scrollHeight"
            )
            if new_height == last_height:
                break
            last_height = new_height

    def send_text(self, xpath, text):
        """
        Sends text through a textbox
        """
        text_box = self.click_by_xpath(xpath)
        text_box.send_keys(text)

    def get_text(self, xpath):
        WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return self.driver.find_element(by=By.XPATH, value=xpath).text

    def get_text_or_value(self, xpath):
        WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        element = self.driver.find_element(by=By.XPATH, value=xpath)

        if element.get_attribute("value"):
            return element.get_attribute("value")
        else:
            return element.text

    def get_texts(self, xpath):
        WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        texts = self.driver.find_elements(by=By.XPATH, value=xpath)
        texts = [i.text for i in texts]
        return texts

    def is_clickable(self, id):
        try:
            WebDriverWait(self.driver, self.TIMEOUT).until(
                EC.element_to_be_clickable((By.XPATH, id))
            )
            return True
        except selenium.common.exceptions.TimeoutException:
            return False