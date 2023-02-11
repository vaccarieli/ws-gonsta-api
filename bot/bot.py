from flask import Flask, request
from wsmsg import send_message, send_image
import logging
from pathlib import Path
from sys import platform
import traceback
from threading import Lock
from datetime import datetime
import pytz
import re
import json
from config import config
from utils import handle_messages_tools

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


logging.basicConfig(filename=ws_utils_path / 'ws-messages.log', level=logging.INFO,
                    format='%(asctime)s %(message)s')

logger = logging.getLogger(__name__)

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

class Instance:
    _instances = {}

    def __init__(self, name: str, number: str) -> None:
        self._name = name
        self._number = number
        if name not in Instance._instances.items():
            Instance._instances[name] = number

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def number(self) -> str:
        return self._number

    @number.setter
    def number(self, number: str):
        self._number = number

    @classmethod
    def access_map(cls, name: str) -> str:
        return cls._instances[name]


# grupos
test_room_group = Instance("test_room_group", "120363047630248137")
pysllanobonitoI =  Instance("pysllanobonitoI", "50761578280-1599012020")
pysllanobonitoII = Instance("pysllanobonitoII", "50761578280-1610642594")

# personas
elio_gonzalez = Instance("Elio", "50763641778")
yenired_rico = Instance("Yenired", "50760283543")
miguel_david = Instance("Miguel", "50760269392")
gonsta_bot = Instance("GonstaBot", "50768600215")

allowed_interact_bot = [elio_gonzalez.number, miguel_david.number]

log_message  = Lock()
in_process = False
initiated_by = False
flag = False
countMessageGroup = 0
firstStart = True

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
            isFile = any([audio, video, image, document])
            message_time = str(datetime.fromtimestamp(int(messageTimestamp)))
            wasReactionMessage = request_json.get("wasReactionMessage", False)

            with log_message:
                if not isFile:
                    logger.info(f"{chatType} : {userInstance} - {pushName}: {message}")
        
            try:
                if not isFile:
                    teque_combo_pattern = re.compile(r'(?i)(teque|c[o0]mb)[ñosod]?', re.IGNORECASE)
                    if re.search(teque_combo_pattern, message) and not fromMe:
                        if chatType == "Group":
                            msg = str(f"{chatType} - {pushName} - {participant}: {message}")
                        else:
                            msg = str(f"{chatType} - {pushName} - {remoteJid}: {message}")

                        send_message(elio_gonzalez.number, msg, userInstance)

            except TypeError:
                logger.error(str(f"ERROR: wasReactionMessage:{wasReactionMessage}, isBroadcast:{isBroadcast}, chatType:{chatType}, pushName:{pushName}, participant:{participant}, message:{message}"))
                logger.error(str(f"ERROR: wasReactionMessage:{wasReactionMessage}, isBroadcast:{isBroadcast}, chatType:{chatType}, pushName:{pushName}, remoteJid:{remoteJid}, message:{message}"))
                logger.error(f"ERROR: {traceback.format_exc()}")
            
            # Ignore all incoming requests once the message is in process!
            if userInstance == yenired_rico.name:
                if flag: 
                        return "Received"
                flag = True
                try:
                    if not fromMe and (pysllanobonitoI.number == remoteJid):
                        countMessageGroup+=1

                    if countMessageGroup == int(config["SEND_AD_EVERY_N_TIMES"]) or firstStart:
                        firstStart = False
                        countMessageGroup = 0
                        logger.info("Ad in process!")
                        send_image(pysllanobonitoI.number, yeniredTequeños, random_messages(), userInstance)
                finally:
                    flag = False

            # GonstaBot Responses Implementation 
            if chatType == "Group" and participant in allowed_interact_bot and (userInstance == gonsta_bot.name):
                if message == "/menu":         # group interactions
                    send_message(remoteJid, "This is the menu", gonsta_bot.name, False)

            # Auto responses to get info
            if chatType == "Normal" and fromMe: 
                if message == "/menu":         # individual interactions
                    send_message(remoteJid, "This is the menu", userInstance, False)
            
            if userInstance == elio_gonzalez.name:
                handle_messages_tools(message, remoteJid, elio_gonzalez.name)

        except Exception:
            logger.error(f"ERROR: {traceback.format_exc()}")

        return "Received"

print("App listening on IP", IP, "and PORT", PORT)
app.run(host=IP, port=PORT, debug=False)
