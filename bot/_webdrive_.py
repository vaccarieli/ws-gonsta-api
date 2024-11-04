from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from pathlib import Path
import pickle
from sys import platform
import base64
import re
from bs4 import BeautifulSoup

PATH = "C:/Users/elios/Desktop/ws-gonsta-api/" if platform == "win32" else "/home/vaccarieli/files/"

options = uc.ChromeOptions()
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36 Edg/103.0.1264.37"
)
options.add_argument("--mute-audio")


def web_driver_wait(driver, waiting_time_out, element):
    return WebDriverWait(driver, waiting_time_out).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, element))
    )


def click_on_el(driver, el: WebElement):
    ActionChains(driver).move_to_element(el).click().perform()


COOKIES_PATH = f"{PATH}/cookies.pkl"
COOKIES_EXIST = Path(COOKIES_PATH).exists()


def handle_cookies(main_url, driver, save_cookies=False, load_cookies=False):
    if COOKIES_EXIST:
        cookies = pickle.load(open(COOKIES_PATH, "rb"))

    if save_cookies:
        input("Enter any key to continue, when ready!")
        pickle.dump(driver.get_cookies(), open(COOKIES_PATH, "wb"))
        print("Cookies were successfully saved!")

    if load_cookies and COOKIES_EXIST:
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.refresh()
        print("Cookies were successfully loaded!")


def webdriver():
    while True:
        try:
            # driver = Firefox(options=options)
            return uc.Chrome(options=options)
        except Exception as e:
            print(e)
            continue


def download_image(driver, url) -> str:
    driver.get(url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "img"))
    )

    download_js = """
            const img = document.querySelector('img');
            let byteArray; // Declare byteArray outside to make it accessible globally

            if (img && img.src) {
            fetch(img.src)
                .then(response => response.arrayBuffer())
                .then(buffer => {
                byteArray = new Uint8Array(buffer); // Assign to the globally declared byteArray
                window.py_image_bytes = btoa(String.fromCharCode(...byteArray));
                })
                .catch(error => console.error('Error fetching image:', error));
            } else {
            console.error('Image not found or no src attribute.');
            }
        """
    driver.execute_script(download_js)

    # Wait for a moment to ensure JavaScript execution is complete
    WebDriverWait(driver, 10).until(
        lambda driver: driver.execute_script(
            "return window.py_image_bytes !== undefined"
        )
    )

    return driver.execute_script("return window.py_image_bytes;")
