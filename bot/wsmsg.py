from time import sleep
from requests import get, post
from mimetypes import guess_type
from sys import platform
from json import load, dump, dumps
from pathlib import Path
from os import path
from config import config

PORT, IP = config["APP_PORT"], config["REQUEST_IP"]
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
baseUrl = f"http://{IP}:{PORT}/" if platform == "win32" else f"http://{IP}:{PORT}/"
jsonPath = "P:\\Synology\\ws\\instances.json" if platform == 'win32' else "/home/vaccarieli/files/ws/instances.json"
qrCodePath = "P:\\Synology\\ws\\qrCode.png" if platform == "win32" else "/home/vaccarieli/files/ws/qrCode.png"
group_list_path = "P:\\Synology\\ws\\group_list.json" if platform == "win32" else "/home/vaccarieli/files/ws/group_list.json"


idType = {
  "normalChat": "@s.whatsapp.net",
  "groupChat": "@g.us",
  "broadCast": "@broadcast",
  "story": "status@broadcast",
}

def send_message(phoneNumber, text, userKey, precense_typying=True):
    headers ={}

    params = {
        "key": userKey,
        "precense_typying": precense_typying
    }
    data = {
        "id": phoneNumber+idType["normalChat"] if len(phoneNumber) < 17 else phoneNumber+idType["groupChat"],
        "text": text
    }
    return post(f"{baseUrl}message/text", headers=headers, params=params, data=data).json()


def send_image(phoneNumber, image, text="", userKey=None, precense_typying=True):
    import requests
    import base64

    headers = {
    }

    params = {
        "key": userKey,
        "precense_typying": precense_typying
    }

    with open(image, "rb") as im:
        image_bytes = im.read()
        encoded_image = base64.b64encode(image_bytes).decode('utf-8')
    
    data = { 
    "id": phoneNumber+idType["normalChat"] if len(phoneNumber)==11 else phoneNumber+idType["groupChat"],
    'text': text,
    "media_file":(path.basename(image), encoded_image, guess_type(image)[0])
    }
    
    return requests.post(f"{baseUrl}message/image", headers=headers, data=data, params=params).json()

def groupListAll(userKey):
    payload = {
        "key": userKey
    }
    return get(f"{baseUrl}group/getallgroups", params=payload).json()


