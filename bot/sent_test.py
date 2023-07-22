from _webdrive_ import webdriver, download_image
from wsmsg import send_image, send_message
from handle_data import (
    extract_main_data,
    add_yt_url_to_data,
    generate_message,
    get_status_contacts,
)
from upscalingImage import super_resolution

# Replace the URL and download_path with your desired values

digital_contents = [
    "Switch_Games",
    "Movies",
    "PlayStation_5_Games",
    "Xbox_Series_X_Games",
    "TV_Series_Seasons",
]

url_website = "https://www.releases.com/l/Switch_Games"

# send_message(
#     phoneNumber="broadcast",
#     text="Hi",
#     userKey="Miguel",
#     authorized_ids=["50763641778@s.whatsapp.net", "50760269392@s.whatsapp.net", 50766725108@s.whatsapp.net],
# )
# import sys

# sys.exit()

# driver = webdriver()

# driver.get(url_website)
blacklist = []
new_contacts = []

status_contacts = get_status_contacts(blacklist, new_contacts)

import base64

# Read the binary data from the file
with open("/home/vaccarieli/ws-gonsta-api/bot/300.jpeg", "rb") as file:
    binary_data = file.read()

# Convert the binary data to base64 encoding
base64_data = base64.b64encode(binary_data).decode("utf-8")


re = send_image(
    phoneNumber="broadcast",
    image=base64_data,
    text="message",
    userKey="Elio",
    precense_typying=False,
    authorized_ids=status_contacts,
    base64=True,
)

print(re)

import sys

sys.exit()

# Get data from the main page and organize it into a dictionary.
data = extract_main_data(driver.page_source)
print("Step 1 Done...")

data = add_yt_url_to_data(driver, data)
print("Step 2 Done...")

for key, value in data.items():
    game = key
    yt_url = data[game].get("yt_link", None)
    if not yt_url:
        continue
    image_url = data[game]["Image"]
    message = generate_message(yt_url)

    image_base64 = super_resolution(download_image(driver, image_url))

    re = send_image(
        phoneNumber="broadcast",
        image=image_base64,
        text=message,
        userKey="Miguel",
        precense_typying=False,
        authorized_ids=status_contacts,
        base64=True,
    )
    print(f"Status {game} was sent!")

driver.close()
