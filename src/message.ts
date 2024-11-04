import express from "express";
import {delay, AnyMessageContent, MiscMessageGenerationOptions} from "@adiwajshing/baileys";
import bodyParser from "body-parser";
import {userSocks} from "./makeWaSocket";
import config from "./config";
import fs from "fs";

export const app = express();

const apiUrl = "http://172.17.0.2:9000/upscale_image";

// Use body-parser to parse request bodies as JSON
app.use(bodyParser.json({limit: "50mb"}));

// Use body-parser to parse URL-encoded bodies
app.use(bodyParser.urlencoded({limit: "50mb", extended: true}));

async function postBase64Image(url: string, base64Image: string): Promise<any> {
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json", // Replace with the appropriate content type
            },
            body: JSON.stringify({image: base64Image}),
        });

        if (!response.ok) {
            throw new Error("Network response was not ok.");
        }

        return await response.json();
    } catch (error) {
        console.error("Error while making POST request:", error);
        return null;
    }
}

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
        const byteArray = Array.from(uintArray);
        const base64String = btoa(String.fromCharCode.apply(null, byteArray));
        const extension = get_url_ext(image_url);
        const image_data = Buffer.from(uintArray); // Original Image Data

        const new_image_data = await postBase64Image(apiUrl, base64String)
            .then((response) => {
                const uintArray = new Uint8Array(
                    Array.from(atob(response["upscaled_image"]), (char) => char.charCodeAt(0))
                );
                return Buffer.from(uintArray);
            })
            .catch((error) => {
                throw error;
            });

        // Return an array with the three values to be destructured
        return [`image.${extension}`, new_image_data, mimeTypes[extension]];
    } catch (error) {
        console.error("Failed to fetch the image:", error);
        throw error; // Rethrow the error so the calling code can handle it if needed
    }
};

const sendMediaFile = async (
    sock: any,
    jid: string,
    file: Buffer,
    mimetype: string,
    filename: string,
    text: string = "",
    statusJidList: string[] = []
) => {

    const data = await sock.sendMessage(jid, {
        image: file,
        caption: text
    }, {
        backgroundColor: "#FFFFFF",
        font: "Arial",
        statusJidList: statusJidList,
        broadcast: true // Enables broadcast mode
    });

    return data;
};

const sendMessageWTyping = async (
    sock: any,
    jid: string,
    text: AnyMessageContent,
    video_path: string | null,
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

    if (video_path) {
        return await sock?.sendMessage(
            jid, 
            { 
                video: fs.readFileSync(video_path), 
                caption: text,
            }
        )
    }
    
    else if (!customSendMessage && jid != "status@broadcast") {
         await sock?.sendMessage(jid, {text: text});


    } 
    
    else if (jid == "status@broadcast" && !customSendMessage) {
        const messageOptions: MiscMessageGenerationOptions = {
            backgroundColor: "#315575",
            font: 3,
            statusJidList: authorized_contacts,
        };
        return await sock?.sendMessage(jid, {text: text}, messageOptions);
    } 
    
    else if (customSendMessage) {
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

        // Convert the base64 string to a Buffer if it's not already a Buffer
        if (typeof image_data === 'string') {
            image_data = Buffer.from(image_data, 'base64');
        }
    } 

    // Parse the 'authorized_ids' field from the request body as an array of strings
    const authorized_contacts: string[] = Array.isArray(JSON.parse(req.body.authorized_ids))
        ? JSON.parse(req.body.authorized_ids)
        : [JSON.parse(req.body.authorized_ids)];

    const data = await sendMessageWTyping(
        userSocks[key],
        id,
        text,
        null,
        () => sendMediaFile(userSocks[key], id, image_data, mimetype, image_name, text, authorized_contacts),
        precense_typying
    );

    res.json({error: false, data: data});
});

app.post("/message/video", async (req: any, res: any) => {
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
        req.body.video_path,
        null,
        precense_typying,
        authorized_contacts
    );
    res.json({error: false, data: response});
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
