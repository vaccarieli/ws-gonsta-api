import { downloadMedia } from "./media";
import { sendWebhook } from "./webhook";

// custom modules
import config from "./config";
import { idType } from "./utils";

const mediaTypes: { [index: string]: any } = {
  audioMessage: "audio",
  imageMessage: "image",
  videoMessage: "video",
  documentMessage: "document",
};

export const event_handler = async (sock: any, user: any) => {
  if (config.WEBHOOK_ENABLED) {
    if (config.WEBHOOK_ALLOWED_EVENTS.includes("messages.upsert")) {
      sock[user]?.ev.on("messages.upsert", async (m: any) => {
        const messages = m.messages[0];
        const text = messages.message?.extendedTextMessage?.text;
        const conversation = messages.message?.conversation;

        const webhookData: { [key: string]: any } = {
          userInstance: user,
          message: text !== undefined ? text : conversation,
          fromMe: messages?.key.fromMe,
          isBroadcast: messages?.broadcast,
          remoteJid: messages?.key.remoteJid,
          participant: messages?.key.participant
            ? messages?.key.participant.replace(idType.normalChat, "")
            : "",
          pushName: messages?.pushName,
          chatType: messages?.key.remoteJid?.includes(idType.normalChat)
            ? "Normal"
            : "Group",
          messageTimestamp: messages?.messageTimestamp,
          wasReactionMessage: messages.message?.reactionMessage ? true : false,
        };

        await downloadMedia(m, webhookData, mediaTypes);
        sendWebhook(webhookData, config.WEBHOOK_URL);
      });
    }
  }
};
