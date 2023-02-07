// custom modules
import config from "./src/config";
import { startSock } from "./src/launcher";
import { userSocks } from "./src/makeWaSocket";
import { app } from "./src/message";
import { event_handler } from "./src/handler";
import { store_data } from "./src/data";

const startApp = async () => {
  store_data();
  await startSock();

  for (const user in userSocks) await event_handler(userSocks, user);

  app.listen(config.APP_PORT, () => {
    console.log(`App listening on ${config.APP_IP}:${config.APP_PORT}`);
  });
};

startApp();
