import express from "express";
import { delay, AnyMessageContent } from "@adiwajshing/baileys";
import bodyParser from "body-parser";
import { userSocks } from "./makeWaSocket";
import config from "./config";
import { idType, wasSentRecently } from "./utils";

export const app = express();

// Use body-parser to parse request bodies as JSON
app.use(bodyParser.json({ limit: "10mb" }));

// Use body-parser to parse URL-encoded bodies
app.use(bodyParser.urlencoded({ limit: "10mb", extended: true }));

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
  text: string = ""
) => {
  const data = await sock?.sendMessage(to, {
    image: file,
    mimetype: mimetype,
    caption: text,
    fileName: filename,
  });
  return data;
};

const sendMessageWTyping = async (
  sock: any,
  jid: string,
  text: AnyMessageContent,
  customSendMessage: ((...args: any[]) => Promise<void>) | null = null,
  precense_typying: boolean = true
) => {
  let sendMessageTime: number = sendMessageTimeTaken(text);

  if (sendMessageTime && config.PRECENSE_TYPING && precense_typying) {
    await sock.presenceSubscribe(jid);
    await delay(1000);

    await sock.sendPresenceUpdate("composing", jid);
    await delay(sendMessageTime);

    await sock.sendPresenceUpdate("paused", jid);
  }

  if (!customSendMessage) {
    return await sock?.sendMessage(jid, { text: text });
  } else {
    const result = customSendMessage(text);
    if (result instanceof Promise) {
      return await result;
    }
  }
};

app.post("/message/text", async (req: any, res: any) => {
  const key = req.query.key;
  const precense_typying = JSON.parse(
    String(req.query.precense_typying).toLowerCase()
  );
  const jid = req.body.id;

  const response = await sendMessageWTyping(
    userSocks[key],
    jid,
    req.body.text,
    null,
    precense_typying
  );
  res.json({ error: false, data: response });
});

app.post("/message/image", async (req, res) => {
  const key = String(req.query.key);
  const precense_typying = JSON.parse(
    String(req.query.precense_typying).toLowerCase()
  );
  const id = String(req.body.id);
  const text = req.body.text;
  let [image_name, image_data, mimetype] = req.body.media_file;
  image_data = Buffer.from(image_data, "base64");
  let data: any;

  try {
    const data = await sendMessageWTyping(
      userSocks[key],
      id,
      text,
      () =>
        sendMediaFile(
          userSocks[key],
          id,
          image_data,
          mimetype,
          image_name,
          text
        ),
      precense_typying
    );
  } catch (error) {
    data = {};
  }

  res.json({ error: false, data: data });
});

app.get("/group/getallgroups", async (req, res) => {
  let key = String(req.query.key);
  let data: any;

  try {
    data = await userSocks[key]?.groupFetchAllParticipating();
  } catch (error) {
    data = {};
  }
  res.json({ error: false, data: data });
});
