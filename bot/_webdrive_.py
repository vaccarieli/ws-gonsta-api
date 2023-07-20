from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import pickle
from sys import platform

PATH = "P:\\Synology\\" if platform == "win32" else "/home/vaccarieli/files/"

options = FirefoxOptions()
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36 Edg/103.0.1264.37"
)
options.add_argument("--mute-audio")
options.add_argument("--headless")  # Enable headless mode for Firefox


def web_driver_wait(driver, waiting_time_out, element):
    return WebDriverWait(driver, waiting_time_out).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, element))
    )


def click_on_el(driver, el: WebElement):
    ActionChains(driver).move_to_element(el).click().perform()


COOKIES_PATH = f"{PATH}cookies/cookies.pkl"
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


def webdriver():
    while True:
        try:
            driver = Firefox(options=options)
            return driver
        except Exception as e:
            print(e)
            continue


def download_image(driver, url) -> str:
    driver.get(url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "img"))
    )

    download_js = """
        fetch(arguments[0])
            .then(response => response.arrayBuffer())
            .then(buffer => {
                const uintArray = new Uint8Array(buffer);
                const base64String = btoa(String.fromCharCode(...uintArray));
                window.py_image_bytes = base64String;
            })
            .catch(error => console.error('Failed to fetch the image:', error));
        """
    driver.execute_script(download_js, url)

    # Wait for a moment to ensure JavaScript execution is complete
    WebDriverWait(driver, 10).until(
        lambda driver: driver.execute_script(
            "return window.py_image_bytes !== undefined"
        )
    )

    # Get the image bytes from the JavaScript variable
    return driver.execute_script("return window.py_image_bytes;")
