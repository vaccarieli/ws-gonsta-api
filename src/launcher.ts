import {fetchLatestBaileysVersion, useMultiFileAuthState} from "@adiwajshing/baileys";

import {handler_events} from "./handler";
import makeWASockectT from "./makeWaSocket";
import {storage} from "./data";
import {Paths} from "./utils";

export const startSock = async (user: string) => {
    const {version} = await fetchLatestBaileysVersion();
    const {state, saveCreds} = await useMultiFileAuthState(Paths.user_keys_folder(user));
    return await makeWASockectT(version, state, storage, user, handler_events, saveCreds, startSock);
};
