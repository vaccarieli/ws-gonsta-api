import {fetchLatestBaileysVersion, useMultiFileAuthState} from "@adiwajshing/baileys";

import {handler_events} from "./handler";
import config from "./config";
import makeWASockectT from "./makeWaSocket";
import {storage} from "./data";
import {Paths} from "./utils";

// start a connection
export const startSock = async () => {
    const {version, isLatest} = await fetchLatestBaileysVersion();
    for (const user of config.WS_USERS) {
        const {state, saveCreds} = await useMultiFileAuthState(Paths.user_keys_folder(user));
        // It starts the socket
        await makeWASockectT(version, state, storage, user, handler_events, saveCreds, startSock);
        if (state.creds.me) console.log(`Welcome Back! ${user}!`);
    }
};
