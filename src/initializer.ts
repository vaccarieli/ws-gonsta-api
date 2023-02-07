import { useMultiFileAuthState } from "@adiwajshing/baileys";
import { Paths } from "./utils";

export const initializer = async (user: string) => {
  const { state, saveCreds } = await useMultiFileAuthState(
    Paths.user_keys_folder(user)
  );
  return { state, saveCreds };
};
