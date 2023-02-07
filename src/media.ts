import { downloadContentFromMessage } from "@adiwajshing/baileys/lib/Utils/messages-media";

export const downloadMedia = async (
  m: any,
  webhookData: any,
  mediaTypes: any
) => {
  const messages = m?.messages?.[0];

  if (messages?.message) {
    const mediaType =
      Object.keys(messages?.message).find((type) => type in mediaTypes) ?? "";

    if (Object.keys(mediaTypes).includes(mediaType)) {
      let buffer = Buffer.from([]);
      try {
        const stream = await downloadContentFromMessage(
          messages?.message?.[mediaType],
          mediaTypes[mediaType]
        );
        webhookData["message"] = messages?.message?.[mediaType].caption;
        for await (const chunk of stream) {
          buffer = Buffer.concat([buffer, chunk]);
        }
      } catch (error) {
        console.error(error);
      }
      webhookData[mediaTypes[mediaType]] = buffer.toString("base64");
    }
  }
};
