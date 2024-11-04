import os
import re
import json
import time
import traceback
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
import base64
import time
from _webdrive_ import download_image, webdriver, handle_cookies
import random


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a string to make it a valid filename by removing forbidden characters.

    Parameters:
        filename (str): The original string to sanitize.

    Returns:
        str: A sanitized version of the filename.
    """
    # Define a regex pattern for forbidden characters
    forbidden_characters_pattern = r'[<>:"/\\|?*]'
    
    # Replace forbidden characters with an empty string
    sanitized = re.sub(forbidden_characters_pattern, '', filename)
    
    # Optionally, you can also limit the length of the filename
    # sanitized = sanitized[:255]  # Limit to 255 characters (common max length for filenames)
    
    return sanitized.strip()  # Remove leading/trailing whitespace


def save_response_as_html(response_text, filename="parsed_response.html") -> BeautifulSoup:
    # Parse the response text with BeautifulSoup
    soup = BeautifulSoup(response_text, "html.parser")
    
    # Get the path to the user's desktop
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    file_path = os.path.join(desktop_path, filename)
    
    # Save the parsed HTML content to a file on the desktop
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(soup.prettify())
    
    print(f"Parsed HTML saved to {file_path}")

    return soup



def load_html_from_desktop(filename="parsed_response.html") -> BeautifulSoup:
    # Get the path to the user's desktop
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    file_path = os.path.join(desktop_path, filename)
    
    # Read the HTML content from the file and parse it with BeautifulSoup
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    
    # Parse the HTML content and return it as a BeautifulSoup object
    return BeautifulSoup(html_content, "html.parser")


def get_data_weekly(soup, data) -> dict:
    data = {}

    for week in ["Last week", "This week •", "Next week"]:
        if week not in data:
            data[week] = {}
        soup_element = soup.find("div", class_="RWP-Calendar-GroupView", attrs={"data-pointprimarytext": week})

        # Extract lists of each attribute
        game_names = [i.text.strip() for i in soup_element.find_all("a", class_="RWPCC-CalendarItems-ItemControl-Name RWPCC-Overlay-OverlayControl-navitem")]
        game_consoles = [i.text.strip() for i in soup_element.find_all("span", class_="RWPCC-CalendarItems-TypeAndVersionsControl-Version")]
        image_urls = [i.find("img").get("src") for i in soup_element.find_all("a", class_="RWPCC-CalendarItems-ItemControl-Image RWPCC-Overlay-OverlayControl-navitem")]
        href_urls = [f"{main_url}{i.get('href')}" for i in soup_element.find_all("a", class_="RWPCC-CalendarItems-ItemControl-Image RWPCC-Overlay-OverlayControl-navitem")]

        # Combine data into a dictionary of dictionaries
        for i, game_name in enumerate(game_names):
            data[week][game_name] = {
                "Game Console": game_consoles[i],
                "Image Url": image_urls[i],
                "Href Url": href_urls[i]
            }


def get_today_data(driver, soup, data) -> dict:

    today_data_soup = soup.find("div", attrs={"class":"RWP-Calendar-GroupView", "data-pointsecondarytext":"Today"})

    release_date = today_data_soup.find("span", class_="RWP-Calendar-GroupHeader-PrimaryText").text.strip().replace("•", "")
    when = today_data_soup.find("span", class_="RWP-Calendar-GroupHeader-PointSecondary").text.strip()

    if today_data_soup:
        game_names = [i.text.strip() for i in today_data_soup.find_all("a", class_="RWPCC-CalendarItems-ItemControl-Name RWPCC-Overlay-OverlayControl-navitem")]
        game_consoles = [i.text.strip() for i in today_data_soup.find_all("span", class_="RWPCC-CalendarItems-TypeAndVersionsControl-Version")]
        image_urls = [i.find("img").get("src").replace("/200", "/") for i in today_data_soup.find_all("a", class_="RWPCC-CalendarItems-ItemControl-Image RWPCC-Overlay-OverlayControl-navitem")]
        href_urls = [f"{main_url}{i.get('href')}" for i in today_data_soup.find_all("a", class_="RWPCC-CalendarItems-ItemControl-Image RWPCC-Overlay-OverlayControl-navitem")]

        # Combine data into a dictionary of dictionaries
        for i, game_name in enumerate(game_names):
            base64Image = download_image(driver, image_urls[i])
            data[game_name] = {
                "Href Url": href_urls[i],
                "Base64 Image": base64Image,
                "Game Console": game_consoles[i],
                "Release Date" : release_date,
                "When": when
            }


def get_game_data(soup, data, game):

    video_div = soup.find("div", class_="RWP-Product-MainInfoView-GalleryMedia RWP-Product-MainInfoView-GalleryVideo mad_active RWPCC-YoutubeVideo-YoutubeVideoControl RWPCC-YoutubeVideo-YoutubeVideoControl-preview")

    if video_div:
        data[game]["Youtube URL"] = video_div.get("data-src")

    return data

main_url = "https://www.releases.com"
url = f"{main_url}/hot/games_switch/daily"

def extract_data():
    data = {}

    driver = webdriver()  # Initialize undetected Chrome with options
    driver.get(url)

    try:
        time.sleep(6)
        soup = save_response_as_html(driver.page_source)

        # soup = load_html_from_desktop()

        get_today_data(driver, soup, data)

        for game in data:
            game_name_file = f"{sanitize_filename(game)}.html"
            game_href_url = data[game]["Href Url"]

            driver.get(game_href_url)
            time.sleep(8)
            soup = save_response_as_html(driver.page_source, game_name_file)

            # soup = load_html_from_desktop(game_name_file)
            get_game_data(soup, data, game)

        # Print formatted JSON output
        # Close the browser after a delay

    except Exception:
        traceback.print_exc()

    finally:
        driver.quit()
    
    return data
