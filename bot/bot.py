from flask import Flask, request
from wsmsg import send_message, send_image, groupListAll
import logging
from pathlib import Path
from sys import platform
import traceback
from threading import Lock, Thread
from datetime import datetime
import pytz
import re
import json
from config import config
from utils import handle_messages_tools, check_cron, list_new_files_gdrive
from time import sleep


idType = {
    "normalChat": "@s.whatsapp.net",
    "groupChat": "@g.us",
    "broadCast": "@broadcast",
    "story": "status@broadcast",
}


# set up logging
IP, PORT = config["WEBHOOK_APP_IP"], int(config["WEBHOOK_APP_PORT"])

panamaTimeZone = pytz.timezone("America/Bogota")

ws_utils_path = (
    Path("/home/vaccarieli/files/") if platform != "win32" else Path("P:/Synology/")
)
path_image_sent = ws_utils_path / "wsUtils/control/imageSent.txt"
pdf_file = ws_utils_path / "wsUtils/Catalogo Switch 2022 Abril.pdf"
ads = ws_utils_path / "wsUtils/anuncio juegos 2022.jpg"
text = ws_utils_path / "wsUtils/text.txt"
controlSent = ws_utils_path / "wsUtils/control/contactsSent.txt"
tequeñosMessages = ws_utils_path / "wsUtils/tequeños-templates.json"
whatsappWhiteList = ws_utils_path / "wsUtils/control/newContactsFound.txt"

yeniredTequeños = ws_utils_path / "yenired publicidad/YENIRED TEQUEÑOS.jpg"
yeniredLimpieza = ws_utils_path / "yenired publicidad/YENIRED LIMPIEZA.jpg"

tjs_logo_gdrive_path = ws_utils_path / "yenired publicidad/TJS LOGO - GDRIVE.jpg"


logging.basicConfig(
    filename=ws_utils_path / "ws-messages.log",
    level=logging.INFO,
    format="%(asctime)s %(message)s",
)

logger = logging.getLogger(__name__)


def random_messages():
    hhmmss = datetime.now(panamaTimeZone).strftime("%H:%M:%S")
    [hours, minutes, seconds] = [int(x) for x in hhmmss.split(":")]
    turno = "Mañana" if hours < 13 else "Tarde" if hours < 19 else "Noche"
    with open(tequeñosMessages, "r", encoding="utf-8") as file:
        listOfMessages = json.load(file)
        # Change order of message
        listOfMessages[turno].append(listOfMessages[turno].pop(0))

    with open(tequeñosMessages, "w", encoding="utf-8") as file:
        json.dump(listOfMessages, file, indent=4, ensure_ascii=False)

    return f"*{listOfMessages[turno][0]}!*"


app = Flask(__name__)
log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)


class Instance:
    _instances = {}
    _user_instances = []

    def __init__(self, name: str, number: str) -> None:
        self._name = name
        self._number = number
        if name not in Instance._instances.items():
            Instance._instances[name] = number
        if not (len(number) >= 13):
            Instance._user_instances.append(name)

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

    @classmethod
    def list_instances(cls, selected_instance: str = None):
        instances_list = ""
        if selected_instance:
            return [*cls._user_instances][int(selected_instance) - 1]

        for index, instance in enumerate([*cls._user_instances], start=1):
            instances_list += f"{index}. {instance}\n"
        return instances_list


# grupos
tjs_room_group = Instance("tjs_room_group", "120363047630248137")
pysllanobonitoI = Instance("pysllanobonitoI", "50761578280-1599012020")
pysllanobonitoII = Instance("pysllanobonitoII", "50761578280-1610642594")

# people
elio_gonzalez = Instance("Elio", "50763641778")
yenired_rico = Instance("Yenired", "50760283543")
miguel_david = Instance("Miguel", "50760269392")
gonsta_bot = Instance("GonstaBot", "50768600215")

allowed_interact_bot = [elio_gonzalez.number, miguel_david.number]
groups_read_contacts = [pysllanobonitoI.number, pysllanobonitoII.number]

log_message = Lock()
flag = False
countMessageGroup = 0
firstStart = True
check_new_files = True
in_process_map = {}

# 0. List all available Instances

# 1. List all available groups and have them listed to make selection.


def list_all_groups(groups: dict, selected_group: any = None) -> str:
    if not selected_group:
        instances_list = ""
        for index, instance_id in enumerate(groups["data"], start=1):
            subject = groups["data"][instance_id]["subject"]
            participants = groups["data"][instance_id]["participants"]
            totalParticipants = len(participants)
            admins_list = [p for p in participants if p["admin"]]
            instances_list += f"*{index}. {subject}:*\n    *- # de Participantes: {totalParticipants}.*\n    *- Administradores:*\n"
            for index, admin in enumerate(admins_list, start=1):
                admin_contact = f'+{admin["id"].strip(idType["normalChat"])}'
                instances_list += f"        *{index}) {admin_contact}*\n"
                if index == len(admins_list):
                    instances_list += "\n"

        return instances_list

    else:
        return [*groups["data"]][int(selected_group) - 1]


#    *Escoge el grupo. Una vez seleccionado, tendrás la opción de elegir un mensaje preestablecido o personalizar uno.*

# *1. Estrenos de Juegos:*
# 	 *- Participantes: 3.*
# 	 *- Administradores:*
# 		*1) 50763641778*
# 		*2) 50765647834*

# 2. After making the selection have all the numbers printed having the admin listed first.


def list_all_numbers_by_group(groups: dict, group_selection: str) -> any:
    numbers_list = ""
    try:
        participants = groups["data"][group_selection]["participants"]
        admins_list = [p for p in participants if p["admin"]]
        for admin in admins_list:
            participants.remove(admin)
            participants.insert(0, admin)

        for index, participant in enumerate(participants, start=1):
            numbers_list += (
                f'*{index}) +{participant["id"].strip(idType["normalChat"])}*\n'
            )
    except Exception as e:
        print(e)
        return False
    return numbers_list


def check_files():
    logger.info("Checking Files in Process!")
    list_new_files = list_new_files_gdrive()
    # if list_new_files:
    #     send_image(
    #         tjs_room_group.number,
    #         tjs_logo_gdrive_path,
    #         list_new_files,
    #         gonsta_bot.name,
    #         False,
    #     )


def backgroun_task():
    import schedule

    schedule.every(30).minutes.do(check_files)

    while True:
        schedule.run_pending()
        sleep(1)


task_thread = Thread(target=backgroun_task)
task_thread.start()

app = Flask(__name__)


@app.route("/messages/upsert", methods=["POST"])
def webhook():
    global flag, countMessageGroup, firstStart, in_process_map, check_new_files
    isFile = False
    if request.method == "POST":
        request_json = request.json
        try:
            userInstance = request_json.get("userInstance", False)
            message = request_json.get("message", False)
            fromMe = request_json.get("fromMe", False)
            isBroadcast = request_json.get("isBroadcast", False)
            remoteJid = (
                request_json.get("remoteJid", False).split("@")[0]
                if request_json.get("remoteJid", False)
                else False
            )
            participant = request_json.get("participant", False)
            pushName = request_json.get("pushName", False)
            chatType = request_json.get("chatType", False)
            messageTimestamp = (
                request_json.get("messageTimestamp", False)
                if isinstance(request_json.get("messageTimestamp", False), int)
                else request_json.get("messageTimestamp", False)["low"]
            )
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
                    teque_combo_pattern = re.compile(
                        r"(?i)(teque|c[o0]mb)[ñosod]?", re.IGNORECASE
                    )
                    if re.search(teque_combo_pattern, message) and not fromMe:
                        if chatType == "Group":
                            msg = str(
                                f"{chatType} - {pushName} - {participant}: {message}"
                            )
                        else:
                            msg = str(
                                f"{chatType} - {pushName} - {remoteJid}: {message}"
                            )

                        send_message(elio_gonzalez.number, msg, userInstance)

            except TypeError:
                logger.error(
                    str(
                        f"ERROR: wasReactionMessage:{wasReactionMessage}, isBroadcast:{isBroadcast}, chatType:{chatType}, pushName:{pushName}, participant:{participant}, message:{message}"
                    )
                )
                logger.error(
                    str(
                        f"ERROR: wasReactionMessage:{wasReactionMessage}, isBroadcast:{isBroadcast}, chatType:{chatType}, pushName:{pushName}, remoteJid:{remoteJid}, message:{message}"
                    )
                )
                logger.error(f"ERROR: {traceback.format_exc()}")

            # Ignore all incoming requests once the message is in process!
            if userInstance == yenired_rico.name:
                if flag:
                    return "Received"
                flag = True
                try:
                    if not fromMe and (pysllanobonitoI.number == remoteJid):
                        countMessageGroup += 1

                    if (
                        countMessageGroup == int(config["SEND_AD_EVERY_N_TIMES"])
                        or firstStart
                    ):
                        firstStart = False
                        countMessageGroup = 0
                        logger.info("Ad in process!")
                        # send_image(
                        #     pysllanobonitoI.number,
                        #     yeniredTequeños,
                        #     random_messages(),
                        #     userInstance,
                        # )

                finally:
                    flag = False

            # GonstaBot Responses Implementation
            if (
                chatType == "Group"
                and participant in allowed_interact_bot
                and (userInstance == gonsta_bot.name)
            ):
                if message == "/menu":  # group interactions
                    send_message(remoteJid, "This is the menu", gonsta_bot.name, False)

            # Auto responses to get info
            if chatType == "Normal" and fromMe:
                if message == "/menu":  # individual interactions
                    send_message(remoteJid, "This is the menu", userInstance, False)

            if fromMe and chatType == "Normal":
                handle_messages_tools(message, remoteJid, userInstance)

                if message == "/listGroups" or in_process_map:
                    if "first_processed" not in in_process_map:
                        instances = Instance.list_instances()
                        send_message(remoteJid, instances, userInstance, False)
                        in_process_map["first_processed"] = True

                    elif "second_processed" not in in_process_map and len(message) <= 2:
                        instance_index = int(message)
                        instance = Instance.list_instances(instance_index)
                        in_process_map["instance"] = instance
                        in_process_map["second_processed"] = True

                    if in_process_map.get("instance", False):
                        if "third_processed" not in in_process_map:
                            groups = groupListAll(in_process_map["instance"])
                            group_list_msg = list_all_groups(groups)
                            send_message(remoteJid, group_list_msg, userInstance, False)
                            in_process_map["third_processed"] = True

                        elif (
                            "fourth_processed" not in in_process_map
                            and len(message) <= 2
                        ):
                            groups = groupListAll(in_process_map["instance"])
                            selection = list_all_groups(groups, message)
                            group_list_msg = list_all_numbers_by_group(
                                groups, selection
                            )
                            send_message(remoteJid, group_list_msg, userInstance, False)
                            in_process_map.clear()

        except Exception:
            logger.error(f"ERROR: {traceback.format_exc()}")

        return "Received"


print("App listening on IP", IP, "and PORT", PORT)
app.run(host=IP, port=PORT, debug=False)
