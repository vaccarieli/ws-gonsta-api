import {Boom} from "@hapi/boom";
import {DisconnectReason, fetchLatestBaileysVersion, useMultiFileAuthState} from "@adiwajshing/baileys";

import config from "./config";
import makeWASockectT from "./makeWaSocket";
import {storage} from "./data";
import {Paths} from "./utils";

const sockUpdateSaveCreds = async (userSocks: any, user: any, saveCreds: any, startSock: any) => {
    userSocks[user].ev.process(
        // events is a map for event name => event data

        async (events: any) => {
            // something about the connection changed
            // maybe it closed, or we received all offline message or connection opened
            if (events["connection.update"]) {
                const update = events["connection.update"];
                const {connection, lastDisconnect} = update;
                if (connection === "close") {
                    // reconnect if not logged out
                    if ((lastDisconnect?.error as Boom)?.output?.statusCode !== DisconnectReason.loggedOut) {
                        await startSock();
                    } else {
                        console.log("Connection closed. You are logged out.");
                    }
                }
                console.log("connection update", update);
            }
            // credentials updated -- save them
            if (events["creds.update"] && saveCreds) {
                await saveCreds();
            }
        }
    );
};

// start a connection
export const startSock = async () => {
    const {version, isLatest} = await fetchLatestBaileysVersion();
    for (const user of config.WS_USERS) {
        const {state, saveCreds} = await useMultiFileAuthState(Paths.user_keys_folder(user));
        // It starts the socket
        await makeWASockectT(version, state, storage, user, sockUpdateSaveCreds, saveCreds, startSock);
        if (state.creds.me) console.log(`Welcome Back! ${user}!`);
    }
};
