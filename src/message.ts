import express from "express";
import {delay, AnyMessageContent, MiscMessageGenerationOptions} from "@adiwajshing/baileys";
import bodyParser from "body-parser";
import {userSocks} from "./makeWaSocket";
import config from "./config";

export const app = express();

// Use body-parser to parse request bodies as JSON
app.use(bodyParser.json({limit: "50mb"}));

// Use body-parser to parse URL-encoded bodies
app.use(bodyParser.urlencoded({limit: "50mb", extended: true}));

const sendMessageTimeTaken = (text: any) => {
    let words = text.split(" ").length;
    let typing_speed = 40;
    return text ? ((words / typing_speed) * 60000) / 2 : 0;
};

const mimeTypes: Record<string, string> = {
    jpg: "image/jpeg",
    png: "image/png",
    gif: "image/gif",
};

const get_url_ext = (url: string): string => {
    const [, , , , , filename] = url.split("/");
    return filename.split(".")[1];
};

const download_image_base64 = async (image_url: string): Promise<[string, Buffer, string]> => {
    try {
        const response = await fetch(image_url);
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        const buffer = await response.arrayBuffer();
        const uintArray = new Uint8Array(buffer);
        const image_data = Buffer.from(uintArray); // No need for type assertion
        const extension = get_url_ext(image_url);

        // Return an array with the three values to be destructured
        return [`image.${extension}`, image_data, mimeTypes[extension]];
    } catch (error) {
        console.error("Failed to fetch the image:", error);
        throw error; // Rethrow the error so the calling code can handle it if needed
    }
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
    const isurl_image = req.body.url_image;

    let [image_name, image_data, mimetype]: [string, Buffer, string] = ["", Buffer.from("", "base64"), ""];

    if (!isurl_image) {
        [image_name, image_data, mimetype] = req.body.media_file;
        image_data = Buffer.from(image_data as ArrayBuffer | SharedArrayBuffer); // Perform a type assertion here
    } else {
        [image_name, image_data, mimetype] = await download_image_base64(req.body.media_file);
    }

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

    res.json({error: false, data: data});
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

app.get("/get", async (req, res) => {
    let url = String(req.query.url);
    let data: any;

    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        const pagesource = await response.text();

        res.send(pagesource);
        return await response.text();
    } catch (error) {
        data = {};
    }
});
