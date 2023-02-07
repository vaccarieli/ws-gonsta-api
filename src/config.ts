import * as fs from "fs";

interface Configuration {
  // WEBHOOK CONFIGURATION
  LOG_LEVEL: string;
  REQUEST_IP: string;
  WEBHOOK_ENABLED: boolean;
  WEBHOOK_URL: string;
  WEBHOOK_APP_IP: string;
  WEBHOOK_APP_PORT: string;
  WEBHOOK_ALLOWED_EVENTS: string[];
  APP_IP: string;
  APP_PORT: string;
  PRECENSE_TYPING: boolean;
  SAVE_N_MESSAGES_PER_CHAT: number;
  WS_USERS: string[];
  WS_NUMBERS: string[];
  ONLINE_ON_CONNECT: boolean;
  [key: string]: any;
}

const configFile = fs.readFileSync(".env", "utf8");
const lines = configFile.split("\n");
const config: Configuration = {} as Configuration;

for (let line of lines) {
  if (line.startsWith("#")) {
    continue;
  }

  let [key, value] = line.split("=");

  let property = key.trim() as keyof Configuration;

  if (!(property in config) && value) {
    value = value.trim().replace(/'([^']+)'/, "$1");

    if (property === "WS_USERS") {
      config.WS_USERS = value
        .split(",")
        .map((val) => {
          return val.trim();
        })
        .filter(Boolean);
    } else if (property === "WS_NUMBERS") {
      config.WS_NUMBERS = value
        .split(",")
        .map((val) => {
          return val.trim();
        })
        .filter(Boolean);
    } else {
      config[property] =
        value == "true" ? true : value == "false" ? false : value;
    }
  }
}

const WS_USERS_MAP: { [key: string]: string } = {};

for (let i = 0; i < config.WS_USERS.length; i++) {
  WS_USERS_MAP[config.WS_USERS[i]] = config.WS_NUMBERS[i];
}

config.WS_USERS_MAP = WS_USERS_MAP;

export default config;
