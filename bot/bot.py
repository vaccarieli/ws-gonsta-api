from flask import Flask, request
from wsmsg import send_message, send_image
import logging
from pathlib import Path
from json import dumps, loads, load, dump
# from css import getIntegrant
from sys import platform
import traceback
from threading import Lock
from datetime import datetime
import pytz
import os
import re
import json
from time import sleep
from config import config
import logging

# set up logging



IP, PORT = config["WEBHOOK_APP_IP"], int(config["WEBHOOK_APP_PORT"])

panamaTimeZone = pytz.timezone('America/Bogota')
hhmmss = datetime.now(panamaTimeZone).strftime("%H:%M:%S")
[hours, minutes, seconds] = [int(x) for x in hhmmss.split(':')]
turno = "Mañana" if hours < 13 else "Tarde" if hours < 19 else "Noche"

ws_utils_path = Path("/home/vaccarieli/files/") if platform != "win32" else Path("P:/Synology/")
path_image_sent = ws_utils_path / "wsUtils/control/imageSent.txt"
pdf_file = ws_utils_path / "wsUtils/Catalogo Switch 2022 Abril.pdf"
ads = ws_utils_path / "wsUtils/anuncio juegos 2022.jpg"
text = ws_utils_path / "wsUtils/text.txt"
controlSent = ws_utils_path / "wsUtils/control/contactsSent.txt"
tequeñosMessages = ws_utils_path / "wsUtils/tequeños-templates.json"
whatsappWhiteList = ws_utils_path / "wsUtils/control/newContactsFound.txt"

yeniredTequeños = ws_utils_path / "yenired publicidad/YENIRED TEQUEÑOS.jpg"
yeniredLimpieza = ws_utils_path / "yenired publicidad/YENIRED LIMPIEZA.jpg"
urlImageTequeños = "https://www.linkpicture.com/q/YENIRED-TEQUENOS.jpg"
urlImageLimpieza = "https://www.linkpicture.com/q/YENIRED-LIMPIEZA.jpg"

miguel_numero = "50760269392"
mi_numero = "50763641778"
test_room_group = "120363047630248137"
yenired_numero = "50760283543"
pysllanobonitoI =  "50761578280-1599012020"
pysllanobonitoII = "50761578280-1610642594"
groups_interact = [pysllanobonitoI, pysllanobonitoII]
black_list = ["50767394785"]
stories_broadcast = "status@broadcast"
allowed_people = [mi_numero, miguel_numero]
elio_gonzalez = "Elio Gonzalez"
yenired_rico = "Yenired Rico"
miguel_david = "Diguel David"
allowed_instances = ["Yenired"]

logging.basicConfig(filename=ws_utils_path / 'ws-messages.log', level=logging.INFO,
                    format='%(asctime)s %(message)s')

def random_messages():
    with open(tequeñosMessages, "r", encoding="utf-8") as file: 
        listOfMessages = json.load(file)
        #Change order of message
        listOfMessages[turno].append(listOfMessages[turno].pop(0))
        
    with open(tequeñosMessages, "w", encoding="utf-8") as file: 
        json.dump(listOfMessages, file, indent=4, ensure_ascii=False)

    return f"*{listOfMessages[turno][0]}!*"


app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
log_message  = Lock()
in_process = False
initiated_by = False
flag = False
countMessageGroup = 0
firstStart = True

instace_init = {
    elio_gonzalez: "Elio",
    yenired_rico: "Yenired",
    miguel_david: "Miguel"
}

@app.route('/messages/upsert', methods=['POST'])
def webhook():
    global in_process, initiated_by, flag, countMessageGroup, firstStart
    isFile = False
    if request.method == 'POST':
        request_json = request.json
        try:
            userInstance = request_json.get("userInstance", False)
            message = request_json.get("message", False)
            fromMe = request_json.get("fromMe", False)
            isBroadcast = request_json.get("isBroadcast", False)
            remoteJid = request_json.get("remoteJid", False).split("@")[0] if request_json.get("remoteJid", False) else False
            participant = request_json.get("participant", False)
            pushName = request_json.get("pushName", False)
            chatType = request_json.get("chatType", False)
            messageTimestamp = request_json.get("messageTimestamp", False) if isinstance(request_json.get("messageTimestamp", False),int) else request_json.get("messageTimestamp", False)["low"]
            audio = request_json.get("audio", False)
            video = request_json.get("video", False)
            image = request_json.get("image", False)
            document = request_json.get("document", False)
            isFile = all([audio, video, image, document])
            message_time = str(datetime.fromtimestamp(int(messageTimestamp)))
            wasReactionMessage = request_json.get("wasReactionMessage", False)

            with log_message:
                if not isFile:
                    logging.info(f"{chatType} : {userInstance} - {pushName}: {message}")
            
            if message == "/respond":
                pass

            if message == "/menu" and remoteJid in allowed_people:
                
                send_message(mi_numero, "This is the menu", userInstance)

            # send message if pattern found
            try:
                teque_combo_pattern = re.compile(r'(?i)(teque|c[o0]mb)[ñosod]?', re.IGNORECASE)
                if re.search(teque_combo_pattern, message) and not isFile and not fromMe:
                    if chatType == "Group":
                        msg = str(f"{chatType} - {pushName} - {participant}: {message}")
                    else:
                        msg = str(f"{chatType} - {pushName} - {remoteJid}: {message}")
                    send_message(mi_numero, msg, userInstance)
            except TypeError:
                traceback.print_exc()
            
            # Ignore all incoming requests once the message is in process!
            if userInstance in allowed_instances:
                if flag: 
                        return "Received"
                flag = True
                try:
                    if not fromMe and (pysllanobonitoI == remoteJid):
                        countMessageGroup+=1

                    if countMessageGroup == int(config["SEND_AD_EVERY_N_TIMES"]) or firstStart:
                        firstStart = False
                        countMessageGroup = 0
                        logging.info("Ad in process!")
                        send_image(pysllanobonitoI, yeniredTequeños, random_messages(), userInstance)
                finally:
                    flag = False

        except Exception as e:
            traceback.print_exc()

        return "Received"
        # return request_json["messages"][0]

print("App listening on IP", IP, "and PORT", PORT)
app.run(host=IP, port=PORT, debug=False)
