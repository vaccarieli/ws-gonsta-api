from wsmsg import send_image, requests_get, send_message, send_message_vid
from handle_data import (
    extract_main_data,
    add_yt_url_to_data,
    generate_message,
    get_status_contacts,
)
import time
from pathlib import Path
import random
import time
from tqdm import tqdm
import os


main_project_path = Path("C:/Users/elios/Desktop/ws-gonsta-api")

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


mensajes_promocionales = {
    30: "🎮 Juegos ilimitados en tu *NINTENDO SWITCH* 🎮\nPor solo $69, instala *NUESTRA APLICACIÓN* y descarga juegos sin límite.\n¿No quieres pagar $69? Cada juego por $9.\n💥 ¡Transforma tu Switch hoy!",
    31: "🎮 Disfruta de juegos ilimitados en tu *NINTENDO SWITCH* 🎮\nCon *NUESTRA APLICACIÓN* a $69, descargas sin parar.\n¿Prefieres un juego? Solo $9 cada uno.\n💥 ¡Aprovecha y ahorra más!",
    32: "🎮 Juegos sin fin en tu *NINTENDO SWITCH* 🎮\nInstala *NUESTRA APLICACIÓN* por $69 y juega ilimitadamente.\n¿No te interesa el pack? Cada juego a $9.\n💥 ¡Dale nueva vida a tu Switch!",
    33: "🎮 Juegos ilimitados en tu *NINTENDO SWITCH* 🎮\nPor $69, descarga sin parar con *NUESTRA APLICACIÓN*.\n¿Solo un juego? Págalo a $9.\n💥 ¡Ahorra a lo grande y disfruta!",
    34: "🎮 Lleva tu *NINTENDO SWITCH* al máximo 🎮\nPor $69, instala *NUESTRA APLICACIÓN* y disfruta de juegos ilimitados.\n¿Solo uno? $9 cada juego.\n💥 ¡Convierte tu Switch en una superconsola!",
    35: "🎮 Juegos ilimitados en tu *NINTENDO SWITCH* 🎮\nCon $69, descarga todo lo que quieras con *NUESTRA APLICACIÓN*.\n¿Prefieres pagar por cada juego? $9 cada uno.\n💥 ¡Aprovecha y ahorra más!",
    36: "🎮 Disfruta sin límites en tu *NINTENDO SWITCH* 🎮\nInstala *NUESTRA APLICACIÓN* por $69 y descarga sin parar.\n¿Un juego suelto? Solo $9.\n💥 ¡Haz de tu Switch algo grande!",
    37: "🎮 Lleva tu *NINTENDO SWITCH* a otro nivel 🎮\nPor $69, instala *NUESTRA APLICACIÓN* y juega sin fin.\n¿Solo un juego? Está a $9.\n💥 ¡No dejes pasar esta oportunidad!",
    38: "🎮 Juegos ilimitados en tu *NINTENDO SWITCH* 🎮\nInstala *NUESTRA APLICACIÓN* por $69 y descarga sin parar.\n¿Solo quieres un juego? Está a $9.\n💥 ¡Haz de tu Switch la mejor consola!",
    39: "🎮 Juegos ilimitados para tu *NINTENDO SWITCH* 🎮\nPor $69, instala *NUESTRA APLICACIÓN* y disfruta sin límites.\n¿Un solo juego? También por $9.\n💥 ¡Convierte tu Switch en la consola definitiva!",
    40: "🎮 Juegos ilimitados en tu *NINTENDO SWITCH* 🎮\nDescarga todo lo que quieras por $69 con *NUESTRA APLICACIÓN*.\n¿Solo uno? $9 cada juego.\n💥 ¡No te pierdas esta oferta!",
    41: "🎮 Disfruta de juegos sin fin en tu *NINTENDO SWITCH* 🎮\nPor $69, con *NUESTRA APLICACIÓN*, descarga sin parar.\n¿Un solo juego? Págalo a $9.\n💥 ¡Convierte tu Switch en la mejor opción!",
    42: "🎮 Juegos ilimitados en tu *NINTENDO SWITCH* 🎮\nPor $69, *NUESTRA APLICACIÓN* te permite jugar sin límites.\n¿Solo uno? Cada juego a $9.\n💥 ¡Transforma tu Switch con esta oferta!",
    43: "🎮 Lleva tu *NINTENDO SWITCH* a otro nivel 🎮\nCon $69, descarga sin parar con *NUESTRA APLICACIÓN*.\n¿Prefieres solo un juego? Cada uno a $9.\n💥 ¡No te pierdas esta oferta!",
    44: "🎮 Juegos ilimitados en tu *NINTENDO SWITCH* 🎮\nPor solo $69, *NUESTRA APLICACIÓN* y descarga ilimitada.\n¿Solo uno? Cada juego a $9.\n💥 ¡Haz de tu Switch la mejor consola!",
    45: "🎮 Disfruta de juegos sin fin en tu *NINTENDO SWITCH* 🎮\nPor $69, instala *NUESTRA APLICACIÓN* y descarga sin parar.\n¿Solo quieres un juego? Está a $9.\n💥 ¡Aprovecha el mejor trato!",
    46: "🎮 Lleva tu *NINTENDO SWITCH* al máximo 🎮\nCon $69, descarga todo lo que quieras con *NUESTRA APLICACIÓN*.\n¿Prefieres pagar por cada juego? Solo $9.\n💥 ¡Transforma tu Switch ahora!",
    47: "🎮 Juegos ilimitados en tu *NINTENDO SWITCH* 🎮\nPor solo $69, descarga sin parar con *NUESTRA APLICACIÓN*.\n¿Prefieres uno a la vez? Cada uno a $9.\n💥 ¡Convierte tu Switch en la mejor consola!",
    48: "🎮 Lleva tu *NINTENDO SWITCH* a otro nivel 🎮\nCon $69, instala *NUESTRA APLICACIÓN* y juega sin parar.\n¿Solo un juego? Está a $9.\n💥 ¡No te pierdas esta oferta única!",
    49: "🎮 Juegos ilimitados en tu *NINTENDO SWITCH* 🎮\nPor solo $69, disfruta de descargas ilimitadas con *NUESTRA APLICACIÓN*.\n¿No quieres pagar $69? Cada juego a $9.\n💥 ¡Dale a tu Switch el mejor catálogo!"
}




messages = {
    30: "Hola, soy Elio, el que te instaló los juegos en tu Switch. Cambié de número porque ya no estoy en el país. Ahora pueden contactarme a este número. ¡Saludos!",
    31: "¡Hola! Aquí Elio, quien instaló los juegos en tu Nintendo Switch. Perdí el contacto anterior al salir del país, así que pueden hablarme a este número. ¡Saludos!",
    32: "Hola, soy Elio. Les instalé los juegos en su Switch. Cambié de teléfono y no pude conservar mi número por estar fuera del país. Contáctenme aquí. ¡Saludos!",
    33: "¡Saludos! Soy Elio, quien configuró los juegos en su Nintendo Switch. Cambié de celular al estar fuera, así que este es mi nuevo número.",
    34: "Hola, ¿qué tal? Soy Elio, el que les instaló los juegos en su Switch. Cambié de teléfono porque no estoy en el país. Me pueden escribir aquí. Saludos.",
    35: "Hola, soy Elio. Los juegos de su Nintendo Switch fueron instalados por mí. Cambié de contacto porque ya no estoy en el país. Este es mi número nuevo. ¡Saludos!",
    36: "Hola, soy Elio, quien les puso los juegos en su Switch. Cambié de número al salir del país. Pueden contactarme ahora a este número.",
    37: "¡Hola! Soy Elio, el que les instaló los juegos en la Switch. Perdí el contacto al salir del país, así que este es mi nuevo número.",
    38: "Hola, soy Elio. Les instalé los juegos en su Switch. Cambié de número por no estar en el país. Este es el nuevo contacto.",
    39: "Hola, soy Elio, quien instaló los juegos en tu Nintendo Switch. Perdí el contacto anterior al salir del país, por lo que pueden llamarme aquí.",
    40: "Saludos, soy Elio. Los juegos de su Nintendo Switch fueron instalados por mí. Perdí el número anterior al estar fuera. Aquí me pueden contactar.",
    41: "Hola, soy Elio, quien les puso los juegos en la Switch. Cambié de número ya que estoy fuera del país. Este es mi nuevo contacto.",
    42: "Hola, aquí Elio, el que instaló los juegos en la Switch. Perdí el contacto anterior porque ya no estoy en el país, así que este es mi nuevo número.",
    43: "¡Hola! Soy Elio, el que configuró los juegos en su Nintendo Switch. Cambié de teléfono por estar fuera del país, ahora pueden contactarme aquí.",
    44: "Hola, soy Elio. Instalé los juegos en su Switch. Perdí el contacto al salir del país, y este es mi nuevo número.",
    45: "Hola, aquí Elio. Les puse los juegos en la Switch. Cambié de número por estar fuera del país. Contáctenme a este número.",
    46: "¡Saludos! Soy Elio, quien les instaló los juegos en su Nintendo Switch. Cambié de contacto ya que estoy fuera. Este es el nuevo.",
    47: "Hola, soy Elio, quien les puso los juegos en la Switch. Perdí el número anterior al salir del país, así que pueden escribir aquí.",
    48: "Hola, soy Elio, quien instaló los juegos en tu Switch. Cambié de número por no estar en el país. Pueden contactarme aquí.",
    49: "¡Hola! Soy Elio, el que configuró los juegos en su Nintendo Switch. Cambié de teléfono y ya no tengo el contacto anterior. Este es el nuevo."
}




contacts_sent_path = (
    main_project_path / "bot/track_sent_contacts.txt"
)

with open(
    contacts_sent_path,
    "r",
    encoding="utf-8",
) as file:
    contacts_sent = [i.strip() for i in file.readlines()]


# contacts_remaining = 0
# for contact in status_contacts:
#     wait_time = random.randint(30, 49)
#     if contact not in contacts_sent:
#         print("Message sent to: " + contact, "Remaing contacts to send: ", abs(len(status_contacts) - contacts_remaining))
#         send_message(contact, messages[wait_time], "elio", False)
#         with open(
#             contacts_sent_path,
#             "a",
#             encoding="utf-8",
#         ) as file:
#             file.write(contact + "\n")
#         time.sleep(wait_time)
#     contacts_remaining +=1

contacts_remaining = 0
total_contacts = len(status_contacts)

# Initialize the progress bar
progress_bar = tqdm(status_contacts, desc="Processing contacts", unit="contact", initial=1)

for contact in progress_bar:
    wait_time = random.randint(30, 49)
    
    if contact not in contacts_sent:
        send_message_vid(
            contact, "C:/Users/elios/Desktop/Promo Instalacion.mp4", mensajes_promocionales[wait_time], "elio", True
        )
        
        # Append contact to the file
        with open(contacts_sent_path, "a", encoding="utf-8") as file:
            file.write(contact + "\n")
        
        # Update contacts remaining
        contacts_remaining += 1

        # Update the progress bar description with the latest contact and remaining count
        progress_bar.set_description(f"Message sent to: {contact}")

        time.sleep(wait_time + 40)


# Close the progress bar
progress_bar.close()









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
