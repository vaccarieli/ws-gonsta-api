import express from "express";
import {delay, AnyMessageContent, MiscMessageGenerationOptions} from "@adiwajshing/baileys";
import bodyParser from "body-parser";
import {userSocks} from "./makeWaSocket";
import config from "./config";

export const app = express();

// Use body-parser to parse request bodies as JSON
app.use(bodyParser.json({limit: "1000mb"}));

// Use body-parser to parse URL-encoded bodies
app.use(bodyParser.urlencoded({limit: "1000mb", extended: true}));

const sendMessageTimeTaken = (text: any) => {
    let words = text.split(" ").length;
    let typing_speed = 40;
    return text ? ((words / typing_speed) * 60000) / 2 : 0;
};

const sendMediaFile = async (
    sock: any,
    to: string,
    file: Buffer,
    mimetype: string,
    filename: string,
    text: string = "",
    authorized_contacts: string[] = []
) => {
    const messageOptions: MiscMessageGenerationOptions = {
        statusJidList: authorized_contacts,
    };

    const data = await sock?.sendMessage(
        to,
        {
            image: file,
            mimetype: mimetype,
            caption: text,
            fileName: filename,
        },
        messageOptions
    );
    return data;
};

const sendMessageWTyping = async (
    sock: any,
    jid: string,
    text: AnyMessageContent,
    customSendMessage: ((...args: any[]) => Promise<void>) | null = null,
    precense_typying: boolean = true,
    authorized_contacts: string[] = []
) => {
    let sendMessageTime: number = sendMessageTimeTaken(text);

    if (sendMessageTime && config.PRECENSE_TYPING && precense_typying && jid != "status@broadcast") {
        await sock.presenceSubscribe(jid);
        await delay(1000);

        await sock.sendPresenceUpdate("composing", jid);
        await delay(sendMessageTime);

        await sock.sendPresenceUpdate("paused", jid);
    }

    if (!customSendMessage && jid != "status@broadcast") {
        return await sock?.sendMessage(jid, {text: text});
    } else if (jid == "status@broadcast" && !customSendMessage) {
        const messageOptions: MiscMessageGenerationOptions = {
            backgroundColor: "#315575",
            font: 3,
            statusJidList: authorized_contacts,
        };
        return await sock?.sendMessage(jid, {text: text}, messageOptions);
    } else if (customSendMessage) {
        const result = customSendMessage(text);

        if (result instanceof Promise) {
            return await result;
        }
    }
};

app.post("/message/text", async (req: any, res: any) => {
    const key = req.query.key;
    const precense_typying = JSON.parse(String(req.query.precense_typying).toLowerCase());
    const jid = req.body.id;

    // Parse the 'authorized_ids' field from the request body as an array of strings
    const authorized_contacts: string[] = Array.isArray(req.body.authorized_ids)
        ? req.body.authorized_ids
        : [req.body.authorized_ids];

    const response = await sendMessageWTyping(
        userSocks[key],
        jid,
        req.body.text,
        null,
        precense_typying,
        authorized_contacts
    );
    res.json({error: false, data: response});
});

app.post("/message/image", async (req, res) => {
    const key = String(req.query.key);
    const precense_typying = JSON.parse(String(req.query.precense_typying).toLowerCase());
    const id = String(req.body.id);
    const text = req.body.text;
    let [image_name, image_data, mimetype] = req.body.media_file;
    image_data = Buffer.from(image_data, "base64");

    // Parse the 'authorized_ids' field from the request body as an array of strings
    const authorized_contacts: string[] = Array.isArray(JSON.parse(req.body.authorized_ids))
        ? JSON.parse(req.body.authorized_ids)
        : [JSON.parse(req.body.authorized_ids)];

    const data = await sendMessageWTyping(
        userSocks[key],
        id,
        text,
        () => sendMediaFile(userSocks[key], id, image_data, mimetype, image_name, text, authorized_contacts),
        precense_typying
    );

    res.json({error: false, data: "data"});
});

app.get("/group/getallgroups", async (req, res) => {
    let key = String(req.query.key);
    let data: any;

    try {
        data = await userSocks[key]?.groupFetchAllParticipating();
    } catch (error) {
        data = {};
    }
    res.json({error: false, data: data});
});
