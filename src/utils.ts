import config from "./config";
import fs from "fs";
import os from "os";

const getMacAddress = () => {
  const networkInterfaces = os.networkInterfaces();
  const keys = Object.keys(networkInterfaces);
  for (const key of keys) {
    const addresses = networkInterfaces[key];
    if (addresses) {
      for (const address of addresses) {
        if (address.mac && address.internal === false) {
          return `[${address.mac.replace(/:/g, "")}][${process.platform}]`;
        }
      }
    }
  }
};

export const appendToFile = (m: any, path: any) => {
  const fs = require("fs");
  fs.appendFile(path, `${JSON.stringify(m)}\n\n`, "utf-8", (err: any) => {
    if (err) throw err;
  });
};

export const idType = {
  normalChat: "@s.whatsapp.net",
  groupChat: "@g.us",
  broadCast: "@broadcast",
  story: "status@broadcast",
};

export const Paths = {
  cwd: process.cwd(),
  log_file: function () {
    return `${this.cwd}/debug-log.txt`;
  },
  user_data_path: function (user: string) {
    return `${this.cwd}/data/${user.toUpperCase()} ${getMacAddress()
      ?.toString()
      .toUpperCase()}/`;
  },
  log_messages_file: function (user: string) {
    let filePath = `${this.user_data_path(user)}log_messages.json`;
    if (!fs.existsSync(filePath)) fs.writeFileSync(filePath, "{}");
    return filePath;
  },
  user_data_file: function (user: string) {
    if (!fs.existsSync(this.user_data_path(user)))
      fs.mkdirSync(this.user_data_path(user), { recursive: true });
    return `${this.user_data_path(user)}user_data.json`;
  },
  user_keys_folder: function (user: string) {
    return `${this.user_data_path(user)}keys`;
  },
};

export const wasSentRecently = (webHookData: any, obj: any, user: any) => {
  if (obj) {
    for (let innerIndex = 0; innerIndex < obj.length; innerIndex++) {
      if (
        webHookData["fromMe"] ||
        (obj[innerIndex]["fromMe"] && obj[innerIndex]["userInstance"] === user)
      ) {
        return true;
      }
    }
  }
};
