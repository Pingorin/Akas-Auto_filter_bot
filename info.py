import os

class Info(object):
    # Telegram Bot Credentials
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN")
    API_ID = int(os.environ.get("API_ID", "123456"))
    API_HASH = os.environ.get("API_HASH", "YOUR_API_HASH")

    # Database
    DB_URI = os.environ.get("DB_URI", "YOUR_MONGO_DB_URI")

    # Bot Info
    Norm_pic = os.environ.get("Norm_pic", "https://telegra.ph/file/your_image_link.jpg")
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME", "YourUsername")
    
    # Channel Links
    UPDATE_CHANNEL = os.environ.get("UPDATE_CHANNEL", "https://t.me/YourChannel")
    MAIN_CHANNEL = os.environ.get("MAIN_CHANNEL", "https://t.me/YourMainChannel")

    # Web Server for Render
    PORT = os.environ.get("PORT", "8080")
