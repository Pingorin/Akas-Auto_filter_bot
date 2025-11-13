import os

class Info(object):
    # Telegram Bot Credentials
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN")
    API_ID = int(os.environ.get("API_ID", "20638104"))
    API_HASH = os.environ.get("API_HASH", "6c884690ca85d39a4c5ad7c15b194e42")

    # Database
    DB_URI = os.environ.get("DB_URI", "mongodb+srv://anu77:anu77@cluster0.8ohtzju.mongodb.net/")

    # Bot Info
    Norm_pic = os.environ.get("Norm_pic", "https://graph.org/file/4d61886e61dfa37a25945.jpg")
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME", "YourUsername")
    
    # Channel Links
    UPDATE_CHANNEL = os.environ.get("UPDATE_CHANNEL", "https://t.me/YourChannel")
    MAIN_CHANNEL = os.environ.get("MAIN_CHANNEL", "https://t.me/YourMainChannel")

    # Web Server for Render
    PORT = os.environ.get("PORT", "8080")
