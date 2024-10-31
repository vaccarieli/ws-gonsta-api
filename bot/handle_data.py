from bs4 import BeautifulSoup
from pathlib import Path

main_project_path = Path("C:/Users/elios/Desktop/ws-gonsta-api")

vcf_file_path = main_project_path / "bot/contacts.vcf"


def generate_message(yt_url):
    return f"""🎮 ¡Disponible Hoy! ¡Escribeme Ya!🕹
👉 Mira El Video Aquí: {yt_url} 👈
📲 #Nintendo #Switch #Videojuegos """


def extract_url(url) -> str:
    import re

    # Define the regular expression pattern to match the URL inside the parentheses
    pattern = r"url\((.*?)\)"

    # Use the findall() method to find all occurrences of the pattern in the string
    try:
        return re.findall(pattern, url)[0]
    except Exception:
        pass


def extract_main_data(html, filter="Today") -> dict:
    new_calendar = {}
    base_url = "https://www.releases.com"

    soup = BeautifulSoup(html, "html.parser")

    images = [
        extract_url(i.find("div", class_="calendar-item-head").get("style"))
        for i in soup.find_all("a", class_="calendar-item-href subpage-trigg")
    ]

    calendar = [
        {
            i.a.text.strip(): {
                "link": base_url + i.a.get("href").strip(),
                "Image": images[index],
            }
        }
        for index, i in enumerate(soup.find_all("div", class_="calendar-item-detail"))
    ]
    calendar_2 = [
        i.find("span", class_="test-time").text.strip()
        for i in soup.find_all(
            "div", class_="calendar-item-footer platform-selector-wrap"
        )
    ]

    for index, date in enumerate(calendar_2):
        for key, value in calendar[index].items():
            if date == filter:
                new_calendar[key] = value

    return new_calendar


def convert_embed_to_watch_link(embed_link):
    watch_link = embed_link.replace(
        "youtube.com/embed/", "www.youtube.com/watch?v="
    ).replace("?autoplay=1", "")
    return watch_link


import pathlib


def add_yt_url_to_data(requests_get, data):
    import time

    for game in data:
        html = requests_get(data[game]["link"])

        soup = BeautifulSoup(html, "html.parser")

        def youtube_url_attribute_value(value):
            return value and value.startswith("https://youtube.com")

        yt_url = soup.find("section", attrs={"video-url": youtube_url_attribute_value})

        if yt_url:
            data[game].update(
                {
                    "yt_link": convert_embed_to_watch_link(
                        yt_url.get("video-url").strip()
                    )
                }
            )
        time.sleep(2)
    return data


import os


def get_status_contacts(blacklist: list, new_contacts, filter_list: list) -> list:
    contacts = []
    count = 0
    with open(vcf_file_path, "r", encoding="utf-8") as vcf_file:
        # Read the entire content of the VCF file
        vcf_data = vcf_file.read()

    # Split the VCF data into individual VCard entries
    vcards = vcf_data.strip().split("END:VCARD\n")
    os.remove(vcf_file_path)

    # Process each VCard entry
    for vcard in vcards:
        lines = vcard.strip().split("\n")

        # Initialize variables to store the contact information
        name = ""
        full_name = ""
        cell_phone = ""

        for line in lines:
            with open(
                vcf_file_path,
                "a",
                encoding="utf-8",
            ) as file:
                if line.startswith("TEL;TYPE="):
                    phone_number = (
                        line.split(":", 1)[1].replace("-", "").replace(" ", "")
                    )
                    if len(phone_number) == 8:
                        phone_number = "+507" + phone_number
                        file.write("TEL;TYPE=CELL:" + phone_number + "\n")
                    else:
                        file.write("TEL;TYPE=CELL:" + phone_number + "\n")
                else:
                    file.write(line + "\n")
                    if "CATEGORIES" in line:
                        file.write("END:VCARD\n")

            if line.startswith("N:"):
                # Extract name from the N field
                name = line.split(":", 1)[1]

            if line.startswith("FN:"):
                # Extract full name from the FN field
                full_name = line.split(":", 1)[1]

        for line in lines:
            if line.startswith("TEL;TYPE="):
                # Check if the phone number starts with '+507' or starts with '6' and is 8 digits long
                if any(
                    keyword for keyword in filter_list if keyword in name.lower()
                ) or any(
                    keyword for keyword in filter_list if keyword in full_name.lower()
                ):
                    if phone_number.startswith("+507"):
                        count += 1
                        cell_phone = phone_number[1:]
                        break  # No need to continue processing the VCard if a valid phone number is found
                    elif phone_number.startswith("6") and len(phone_number) == 8:
                        count += 1
                        cell_phone = "507" + phone_number
                        break

                # Check if both name and cell_phone are not empty to print the contact information
        if name and cell_phone:
            if cell_phone not in blacklist:
                contacts.append(cell_phone)
    contacts.extend(new_contacts)
    return contacts
