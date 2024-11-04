from bs4 import BeautifulSoup
from pathlib import Path
import random

main_project_path = Path("C:/Users/elios/Desktop/ws-gonsta-api")

vcf_file_path = main_project_path / "bot/contacts.vcf"

vcf_file_path_final = main_project_path / "bot/contacts_final.vcf"



import random

class MessageGenerator:
    def __init__(self):
        
        # Templates for messages with a YouTube URL
        self.templates_with_url = [
            "🎮 NINTENDO SWITCH: ¡Disponible Hoy! ¡Escríbeme Ya! 🕹\n👉 Mira el video aquí: {url} 👈\n📲 #Nintendo #Switch #Videojuegos",
            "🚀 NINTENDO SWITCH: ¡No te pierdas este contenido! 🎮\n🎬 Dale un vistazo al video aquí: {url}\n🎮 #NintendoSwitch #Gaming",
            "👾 NINTENDO SWITCH: ¡Atención jugadores! 🎮\n👉 Descubre más en este video: {url} 👈\n#Switch #Videojuegos #Nintendo",
            "🔥 NINTENDO SWITCH: ¡Nuevo lanzamiento para todos los fans! 🕹\n📺 Mira todo en: {url}\n#Nintendo #SwitchGaming",
            "🎉 NINTENDO SWITCH: ¡Aquí tienes el video más esperado! 📲\n🎮 Link directo: {url}\n#NintendoSwitch #GamerLife",
            "🎮 NINTENDO SWITCH: ¡Nuevo contenido disponible! 👾\nMira el video completo aquí: {url}\n#Switch #GamingLife",
            "🎉 NINTENDO SWITCH: ¡Descubre el juego en acción! 🎮\n👉 Enlace al video: {url}\n#Nintendo #Switch #Videojuegos",
            "🔥 NINTENDO SWITCH: ¡No te pierdas el gameplay! 🎮\n🎬 Video aquí: {url}\n#NintendoSwitch #GameLovers",
            "🚀 NINTENDO SWITCH: ¡Dale play para ver lo mejor de este lanzamiento! 🕹\n👉 Video aquí: {url}\n#SwitchGaming #NintendoFans",
            "🎬 NINTENDO SWITCH: ¡Todo lo que quieres ver está aquí! 🎮\n📺 Link al video: {url}\n#Nintendo #SwitchCommunity"
        ]

        # Templates for messages without a YouTube URL (only a game cover announcement)
        self.templates_without_url = [
            "🎮 NINTENDO SWITCH: ¡Nuevo lanzamiento disponible hoy! 🎉\n🖼️ ¡Mira la portada del juego! 📲 #Nintendo #Switch #Videojuegos",
            "🔥 NINTENDO SWITCH: ¡Ya llegó el juego que esperabas! 🎮\n📷 ¡Echa un vistazo a la portada! 🕹️ #Switch #Gaming",
            "🚀 NINTENDO SWITCH: ¡Listo para jugar! 🎮\n🖼️ ¡Mira la portada y descubre esta experiencia! #Nintendo #Switch #Videojuegos",
            "🎉 NINTENDO SWITCH: ¡Nuevo contenido para los fanáticos de siempre! 🎮\n📷 ¡Aquí está la portada! #NintendoSwitch #Gaming",
            "⚡ NINTENDO SWITCH: ¡Sumérgete en la experiencia desde hoy! 🎮\n🖼️ Observa la portada y prepárate para jugar. #Switch #Nintendo #Videojuegos",
            "🎮 NINTENDO SWITCH: ¡Ya disponible para todos! 🕹️\n📷 ¡Disfruta de la portada y prepárate! #NintendoSwitch #Videojuegos",
            "🚀 NINTENDO SWITCH: ¡Aventúrate con el nuevo lanzamiento! 🎮\n🖼️ Observa la portada y anímate a jugar. #Nintendo #Switch",
            "🔥 NINTENDO SWITCH: ¡Es el día de lanzamiento! 🎉\n📷 ¡Aquí tienes la portada del juego! #Switch #Gaming",
            "👾 NINTENDO SWITCH: ¡La espera ha terminado! 🎮\n🖼️ Descubre la portada del juego hoy. #NintendoSwitch #GamingTime",
            "⚡ NINTENDO SWITCH: ¡Un juego nuevo ya está aquí! 🕹️\n📷 Mira la portada y sumérgete en la diversión. #Switch #Nintendo"
        ]


    def generate_message(self, yt_url=None):
        if yt_url:
            # Choose a template that includes the YouTube URL
            message_template = random.choice(self.templates_with_url)
            return message_template.format(url=yt_url)
        else:
            # Choose a template without a YouTube URL
            return random.choice(self.templates_without_url)



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

    # Process each VCard entry
    for vcard in vcards:
        lines = vcard.strip().split("\n")

        # Initialize variables to store the contact information
        name = ""
        full_name = ""
        cell_phone = ""

        for line in lines:
            with open(
                vcf_file_path_final,
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
