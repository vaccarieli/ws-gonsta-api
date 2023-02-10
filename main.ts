// custom modules
import config from "./src/config";
import {startSock} from "./src/launcher";
import {app} from "./src/message";
import {store_data} from "./src/data";

const startApp = async () => {
    store_data();
    await startSock();

    app.listen(config.APP_PORT, () => {
        console.log(`App listening on ${config.APP_IP}:${config.APP_PORT}`);
    });
};

(async () => {
    await startApp();
})();
