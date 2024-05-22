from wsmsg import send_image, requests_get, send_message, send_message_vid
from handle_data import (
    extract_main_data,
    add_yt_url_to_data,
    generate_message,
    get_status_contacts,
)
import time


digital_contents = [
    "Switch_Games",
    "Movies",
    "PlayStation_5_Games",
    "Xbox_Series_X_Games",
    "TV_Series_Seasons",
]

url_website = f"https://www.releases.com/l/Switch_Games"

blacklist = []
new_contacts = []

status_contacts = get_status_contacts(blacklist, new_contacts, ["switch", "wii", "3ds"])

import time

text = "Hola como estas? Soy Elio quien te instalo los juegos en tu Nintendo Switch. Cambie de teléfono y no pude mantener mi otro contacto por no estar en el País, así que me pueden contactar a este número. Saludos."
# send_message_vid(
#   "584246447397", "/home/vaccarieli/Downloads/test.mp4", text, "elio", True
# )

contacts_sent_path = (
    "/home/vaccarieli/Projects/ws-gonsta-api/bot/track_sent_contacts.txt"
)

with open(
    contacts_sent_path,
    "r",
    encoding="utf-8",
) as file:
    contacts_sent = [i.strip() for i in file.readlines()]

for contact in status_contacts:
    if contact not in contacts_sent:
        print("Message sent to: " + contact)
        send_message(contact, text, "elio", False)
        with open(
            contacts_sent_path,
            "a",
            encoding="utf-8",
        ) as file:
            file.write(contact + "\n")
        time.sleep(5)


# # Get data from the main page and organize it into a dictionary.
# data = extract_main_data(requests_get(url_website))
# print("Step 1 Done...")

# data = add_yt_url_to_data(requests_get, data)
# print("Step 2 Done...")

# for key, value in data.items():
#     game = key
#     yt_url = data[game].get("yt_link", None)
#     if not yt_url:
#         continue
#     image_url = data[game]["Image"]
#     message = generate_message(yt_url)

#     re = send_image(
#         phoneNumber="broadcast",
#         image=image_url,
#         text=message,
#         userKey="Elio",
#         precense_typying=False,
#         authorized_ids=status_contacts,
#         url_image=True,
#     )

#     print(f"Status {game} was sent!")
#     time.sleep(2)
