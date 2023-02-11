import makeWASocket, {MessageRetryMap, makeCacheableSignalKeyStore, WASocket} from "@adiwajshing/baileys";
import {AuthenticationState} from "@adiwajshing/baileys/lib/Types/Auth";
import {WAVersion} from "@adiwajshing/baileys/lib/Types/Socket";

// custom modules
import {logger} from "./data";
import config from "./config";
import {instanceCheck} from "./launcher";

export const userSocks: {[key: string]: WASocket} = {};
const msgRetryCounterMap: MessageRetryMap = {};

export default async (
    version: WAVersion,
    state: AuthenticationState,
    storage: any,
    ws_user: string,
    sockUpdateSaveCreds: any,
    saveCreds: any,
    startSock: any
) => {
    return new Promise((resolve, reject) => {
        if (!instanceCheck[ws_user]) {
            userSocks[ws_user] = makeWASocket({
                version,
                logger,
                printQRInTerminal: true,
                auth: {
                    creds: state.creds,
                    // caching makes the store faster to send/recv messages
                    keys: makeCacheableSignalKeyStore(state.keys, logger),
                },
                msgRetryCounterMap,
                generateHighQualityLinkPreview: true,
                // implement to handle retries
                getMessage: async (key: any) => {
                    if (storage[ws_user]) {
                        const msg = await storage[ws_user].loadMessage(key.remoteJid!, key.id!);
                        return msg?.message || undefined;
                    }
                    // only if store is present
                    return {
                        conversation: "hello",
                    };
                },
                markOnlineOnConnect: config.ONLINE_ON_CONNECT,
                browser: ["GonstaService", "Safari", "3.0"],
                emitOwnEvents: true,
            });
        }
        if (!userSocks[ws_user].user) {
            console.log(ws_user, "Scan the QR Code!\n");
        }

        storage[ws_user]?.bind(userSocks[ws_user].ev);
        sockUpdateSaveCreds(userSocks, ws_user, saveCreds, startSock);

        const check = setInterval(() => {
            if (userSocks[ws_user].user) {
                clearInterval(check);
                resolve(true);
            }
        }, 200);
    });
};
