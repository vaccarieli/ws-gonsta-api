// custom modules
import config from "./src/config";
import {startSock} from "./src/launcher";
import {app} from "./src/message";
import {store_data} from "./src/data";

const startApp = async () => {
    for (const user of config.WS_USERS) {
        store_data(user);
        if (await startSock(user)) console.log(`Welcome! ${user}!`);
    }

    app.listen(config.APP_PORT, () => {
        console.log(`App listening on ${config.APP_IP}:${config.APP_PORT}`);
    });
};

startApp();
