from wsmsg import send_image, send_message, groupListAll
from sys import platform
import json
import datetime
import time
import pytz
from pathlib import Path
import urllib
from tqdm import tqdm

start_time = time.time()
panamaTimeZone = pytz.timezone('America/Bogota')
hhmmss = datetime.datetime.now(panamaTimeZone).strftime("%H:%M:%S")
[hours, minutes, seconds] = [int(x) for x in hhmmss.split(':')]
x = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
hours = int(x.seconds / 3600)

idType = {
  "normalChat": "@s.whatsapp.net",
  "groupChat": "@g.us",
  "broadCast": "@broadcast",
  "story": "status@broadcast",
}

greeting = "Buenos Dias" if hours < 13 else "Buenas Tardes" if hours < 19 else "Buenas Noches"
turno = "Mañana" if hours < 13 else "Tarde" if hours < 19 else "Noche"
    
ws_utils_path = Path("/home/vaccarieli/files/") if platform != "win32" else Path("P:/Synology/")
path_image_sent = ws_utils_path / "wsUtils/control/imageSent.txt"
pdf_file = ws_utils_path / "wsUtils/Catalogo Switch 2022 Abril.pdf"
ads = ws_utils_path / "wsUtils/anuncio juegos 2022.jpg"
text = ws_utils_path / "wsUtils/text.txt"
controlSent = ws_utils_path / "wsUtils/control/contactsSent.txt"
tequeñosMessages = ws_utils_path / "wsUtils/tequeños-templates.json"
tequeñosMessagesSender = ws_utils_path / "wsUtils/tequeños-templates - sender.json"
whatsappWhiteList = ws_utils_path / "wsUtils/control/newContactsFound.txt"

yeniredTequeños = ws_utils_path / "yenired publicidad/YENIRED TEQUEÑOS.jpg"
yeniredLimpieza = ws_utils_path / "yenired publicidad/YENIRED LIMPIEZA.jpg"
urlImageTequeños = "https://www.linkpicture.com/q/YENIRED-TEQUENOS.jpg"
urlImageLimpieza = "https://www.linkpicture.com/q/YENIRED-LIMPIEZA.jpg"

mi_numero = "50763641778"
test_room_group = "120363047630248137"
yenired_numero = "50760283543"
pysllanobonitoI =  "50761578280-1599012020"
pysllanobonitoII = "50761578280-1610642594"
groups_interact = [pysllanobonitoI, pysllanobonitoII]
black_list = ["50767394785", "50766387392"]
stories_broadcast = "status@broadcast"

userKeyElio = "Elio"
userKeyYenired = "Yenired"
userKeyMiguel = "Miguel"

def random_messages():
    with open(tequeñosMessagesSender, "r", encoding="utf-8") as file: 
        listOfMessages = json.load(file)
        #Change order of message
        listOfMessages[turno].append(listOfMessages[turno].pop(0))
        
    with open(tequeñosMessagesSender, "w", encoding="utf-8") as file: 
        json.dump(listOfMessages, file, indent=4, ensure_ascii=False)

    return f"*{listOfMessages[turno][0]}!*"

messageLimpieza = f"{greeting} ¡Vecin@, disculpa la cadena! 🙏 Solo quería informarte que estoy disponible para hacer la limpieza en tu hogar. Si estás interesado en mis servicios y quieres saber más, no dudes en ponerte en contacto conmigo. 📱 Te prometo dejar tu hogar reluciente y con una sensación de frescura. ¡Espero oír de ti pronto! 😊"
footerText = ""
queryMessage = f"Hola Yenired {greeting}, quiero ordenar!"
queryMessage = urllib.parse.quote(queryMessage)
footerOfMessage = "Muchas Gracias!"
message_chain = "Hola Veci Buen dia!¡Los tequeños recién hechos están aquí! 🔥 No te quedes sin probarlos, ofrecemos servicio de delivery durante todo el día, desde temprano hasta tarde para que puedas disfrutar de un desayuno, cena o merienda deliciosa en casa. ¡Aprovecha esta oportunidad y haz tu pedido ahora!"


message_te = random_messages()
def sendAd(group_list):
    with open(path_image_sent, 'r', encoding='utf-8') as f: contacts_sent = [i.strip() for i in f.readlines()]

    for group in [groupListAll(userKeyMiguel)]: 
        for group_id in group["data"]: # 50761578280-1599012020@g.us
            if group_id.strip("@g.us") in group_list:
                for participant in tqdm(group["data"][group_id]["participants"], desc="Progress: "):
                    if participant['admin'] is None and participant not in black_list:
                        participant = participant['id'].strip('@s.whatsapp.net')
                        if participant not in contacts_sent:
                            message_te = random_messages()
                            send_image(participant, yeniredTequeños, message_te, userKeyYenired, False)
                            with open(path_image_sent, 'a', encoding='utf-8') as f: f.write(participant+'\n')
                            time.sleep(20)

    send_message(mi_numero, "Los mensajes fueron enviados exitosamente!", userKeyYenired)

if __name__ == "__main__":
    response = send_image(mi_numero, yeniredTequeños, message_te, "Miguel")

    # response = send_message(mi_numero, message, "Miguel")

    # sendAd(groups_interact)
