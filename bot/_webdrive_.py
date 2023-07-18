import os
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from time import time, sleep
from json import load
from bs4 import BeautifulSoup
from pathlib import Path
import pickle
from json import dump
from sys import platform, exit

PATH = "P:\\Synology\\" if platform == "win32" else "/home/vaccarieli/files/"
PATH_WEBDRIVER = f"{PATH}webdrivers\\" if platform == "win32" else f"{PATH}webdrivers/"


def browser_service(brows):
    if brows == "firefox":
        return f"{PATH_WEBDRIVER}geckodriver"


BROWSER = "firefox"

options = FirefoxOptions()
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36 Edg/103.0.1264.37"
)
options.add_argument("--mute-audio")
options.add_argument("--headless")  # Enable headless mode for Firefox

Browser = Firefox
service = browser_service(BROWSER)


def web_driver_wait(driver, waiting_time_out, element):
    return WebDriverWait(driver, waiting_time_out).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, element))
    )


def click_on_el(driver, el: WebElement):
    ActionChains(driver).move_to_element(el).click().perform()


COOKIES_PATH = f"{PATH}cookies/cookies-{BROWSER}.pkl"
COOKIES_EXIST = Path(COOKIES_PATH).exists()


def handle_cookies(driver, save_cookies=False, load_cookies=False):
    if COOKIES_EXIST:
        cookies = pickle.load(open(COOKIES_PATH, "rb"))

    if save_cookies:
        pickle.dump(driver.get_cookies(), open(COOKIES_PATH, "wb"))
        print("Cookies were successfully saved!")

    if load_cookies and COOKIES_EXIST:
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.refresh()
        print("Cookies were successfully loaded!")


def _webdriver_get_(headless=False):
    while True:
        if headless:
            options.add_argument("--headless")
        try:
            driver = Browser(
                options=options, executable_path=service
            )  # Specify the geckodriver path
            return driver
        except Exception as e:
            print(e)
            continue
