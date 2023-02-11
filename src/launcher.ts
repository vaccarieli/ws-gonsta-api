import {fetchLatestBaileysVersion, useMultiFileAuthState} from "@adiwajshing/baileys";

import {handler_events} from "./handler";
import config from "./config";
import makeWASockectT from "./makeWaSocket";
import {storage} from "./data";
import {Paths} from "./utils";

export const instanceCheck: {[key: string]: any} = {};

// start a connection
export const startSock = async () => {
    const {version} = await fetchLatestBaileysVersion();
    for (const user of config.WS_USERS) {
        const {state, saveCreds} = await useMultiFileAuthState(Paths.user_keys_folder(user));
        // It starts the socket
        instanceCheck[user] = await makeWASockectT(version, state, storage, user, handler_events, saveCreds, startSock);
        if (instanceCheck[user]) console.log(`Welcome Back! ${user}!`);
    }
};
