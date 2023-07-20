from _webdrive_ import webdriver, download_image
from wsmsg import send_image
from bs4 import BeautifulSoup
from handle_data import extract_main_data, add_yt_url_to_data, generate_message

# Replace the URL and download_path with your desired values

digital_contents = [
    "Switch_Games",
    "Movies",
    "PlayStation_5_Games",
    "Xbox_Series_X_Games",
    "TV_Series_Seasons",
]

url_website = "https://www.releases.com/l/Switch_Games"


driver = webdriver()

driver.get(url_website)

# Get data from the main page and organize it into a dictionary.
data = extract_main_data(driver.page_source)
print("Step 1 Done...")

data = add_yt_url_to_data(driver, data)
print("Step 2 Done...")

for key, value in data.items():
    game = key
    yt_url = data[game]["yt_link"]
    image_url = data[game]["Image"]
    message = generate_message(yt_url)

    image_base64 = download_image(driver, image_url)

    re = send_image(
        phoneNumber="broadcast",
        image=image_base64,
        text=message,
        userKey="Miguel",
        precense_typying=False,
        authorized_ids=["50763641778@s.whatsapp.net", "50760269392@s.whatsapp.net"],
        base64=True,
    )
    print(f"Status {game} was sent!")

driver.close()
