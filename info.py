# info.py
import os

# Telegram Bot Token from @BotFather
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# API Keys from my.telegram.org
API_ID = int(os.environ.get("API_ID", 123456))
API_HASH = os.environ.get("API_HASH", "YOUR_API_HASH_HERE")

# Bot Owner ID (https://t.me/userinfobot से अपनी ID प्राप्त करें)
OWNER_ID = int(os.environ.get("OWNER_ID", 123456789))

# MongoDB (Motor)
MONGO_DB_URI = os.environ.get("MONGO_DB_URI", "YOUR_MONGO_DB_URI_HERE")

# Bot settings
BOT_USERNAME = os.environ.get("BOT_USERNAME", "YourBotUsername") # (Without @)
Norm_pic = os.environ.get("Norm_pic", "https://graph.org/file/4d61886e61dfa37a25945.jpg")

# Channel and Owner
UPDATE_CHANNEL = os.environ.get("UPDATE_CHANNEL", "https://t.me/+UWok0DWTWTpkYTA1")
MAIN_CHANNEL = os.environ.get("MAIN_CHANNEL", "https://t.me/+wVUitwQcus82OGVl")
OWNER_USERNAME = os.environ.get("OWNER_USERNAME", "ramSitaam") # (Without @)
