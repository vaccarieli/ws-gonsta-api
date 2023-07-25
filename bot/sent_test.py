from wsmsg import send_image, send_message, requests_get
from handle_data import (
    extract_main_data,
    add_yt_url_to_data,
    generate_message,
    get_status_contacts,
)
import time

# from upscalingImage import super_resolution

digital_contents = [
    "Switch_Games",
    "Movies",
    "PlayStation_5_Games",
    "Xbox_Series_X_Games",
    "TV_Series_Seasons",
]

url_website = f"https://www.releases.com/l/Switch_Games"

blacklist = []
new_contacts = [
    "50760283543@s.whatsapp.net",
    "584127924055@s.whatsapp.net",
    "50763641778@s.whatsapp.net",
]
status_contacts = get_status_contacts(blacklist, new_contacts)

# Get data from the main page and organize it into a dictionary.
data = extract_main_data(requests_get(url_website))
print("Step 1 Done...")

data = add_yt_url_to_data(requests_get, data)
print("Step 2 Done...")

for key, value in data.items():
    game = key
    yt_url = data[game].get("yt_link", None)
    if not yt_url:
        continue
    image_url = data[game]["Image"]
    message = generate_message(yt_url)

    re = send_image(
        phoneNumber="broadcast",
        image=image_url,
        text=message,
        userKey="Elio",
        precense_typying=False,
        authorized_ids=status_contacts,
        url_image=True,
    )

    print(f"Status {game} was sent!")
    time.sleep(2)
