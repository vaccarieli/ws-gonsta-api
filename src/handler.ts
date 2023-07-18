import {Boom} from "@hapi/boom";

import {downloadMedia} from "./media";
import {sendWebhook} from "./webhook";

// custom modules
import config from "./config";
import {idType} from "./utils";

import {DisconnectReason} from "@adiwajshing/baileys";

const mediaTypes: {[index: string]: any} = {
    audioMessage: "audio",
    imageMessage: "image",
    videoMessage: "video",
    documentMessage: "document",
};

const messages_upsert = (m: any, user: any) => {
    if (config.WEBHOOK_ENABLED) {
        if (config.WEBHOOK_ALLOWED_EVENTS.includes("messages.upsert")) {
            const messages = m.messages[0];
            const text = messages.message?.extendedTextMessage?.text;
            const conversation = messages.message?.conversation;

            const webhookData: {[key: string]: any} = {
                userInstance: user,
                message: text !== undefined ? text : conversation,
                fromMe: messages?.key.fromMe,
                isBroadcast: messages?.broadcast,
                remoteJid: messages?.key.remoteJid,
                participant: messages?.key.participant ? messages?.key.participant.replace(idType.normalChat, "") : "",
                pushName: messages?.pushName,
                chatType: messages?.key.remoteJid?.includes(idType.normalChat) ? "Normal" : "Group",
                messageTimestamp: messages?.messageTimestamp,
                wasReactionMessage: messages.message?.reactionMessage ? true : false,
            };

            downloadMedia(m, webhookData, mediaTypes);
            sendWebhook(webhookData, config.WEBHOOK_URL);
        }
    }
};

export const handler_events = (userSocks: any, user: any, saveCreds: any, startSock: any) => {
    userSocks[user].ev.process(async (events: any) => {
        if (events["connection.update"]) {
            const update = events["connection.update"];
            const {connection, lastDisconnect} = update;
            if (connection === "close") {
                if ((lastDisconnect?.error as Boom)?.output?.statusCode !== DisconnectReason.loggedOut) {
                    await startSock(user);
                } else {
                    console.log("Connection closed. You are logged out.");
                }
            }
            console.log("connection update", update);
        }

        if (events["creds.update"]) {
            await saveCreds();
        }

        if (events["messages.upsert"]) {
            messages_upsert(events["messages.upsert"], user);
        }
    });
};
