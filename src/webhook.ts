import axios from "axios";

export const sendWebhook = async (data: any, url: any = "http://localhost:8000/webhook") => {
    try {
        return await axios.post(url, data, {
            headers: {
                "Content-Type": "application/json",
            },
        });
    } catch (error) {
        console.error(error);
    }
};
