# info.py
import os

# यह 4 वेरिएबल्स utils.py के लिए ज़रूरी हैं
BOT_USERNAME = os.environ.get("BOT_USERNAME", "Aks_Auto_F_Sub_bot")
UPDATE_CHANNEL = os.environ.get("UPDATE_CHANNEL", "https://t.me/+wVUitwQcus82OGVl")
MAIN_CHANNEL = os.environ.get("MAIN_CHANNEL", "https://t.me/+UWok0DWTWTpkYTA1")
OWNER_USERNAME = os.environ.get("OWNER_USERNAME", "ramSitaam") # <-- यह लाइन गायब है

# बाकी वेरिएबल्स
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8538484625:AAEMp2gncTCuIFR-VZcmVs_81vBHSNPPwO4")
API_ID = int(os.environ.get("API_ID", 20638104))
API_HASH = os.environ.get("API_HASH", "6c884690ca85d39a4c5ad7c15b194e42")
OWNER_ID = int(os.environ.get("OWNER_ID", 7245547751))
MONGO_DB_URI = os.environ.get("MONGO_DB_URI", "mongodb+srv://anu77:anu77@cluster0.8ohtzju.mongodb.net/")
Norm_pic = os.environ.get("Norm_pic", "https://graph.org/file/4d61886e61dfa37a25945.jpg")
