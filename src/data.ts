import config from "./config";
import { Paths } from "./utils";
import { makeInMemoryStore } from "@adiwajshing/baileys";
import MAIN_LOGGER from "@adiwajshing/baileys/lib/Utils/logger";

// users to interact on ws

// pass arguments to enable/disable feature --no-store, --no-reply
const useStore = !process.argv.includes("--no-store");

export const logger = MAIN_LOGGER.child({});
logger.level = config.LOG_LEVEL;

export const storage: { [key: string]: any } = {};

export const store_data = () => {
  config.WS_USERS.map((user) => {
    // paths for data
    // the store maintains the data of the WA connection in memory
    // can be written out to a file & read from it
    const store = useStore ? makeInMemoryStore({ logger }) : undefined;
    let user_data_file = Paths.user_data_file(user);
    store?.readFromFile(user_data_file);

    // save every 10s the data to a json file using setIntervale which schedules something to run at certain times provided the JS runtime is idle at that time.
    setInterval(() => {
      store?.writeToFile(user_data_file);
    }, 10_000);
    storage[user] = store;
  });
};