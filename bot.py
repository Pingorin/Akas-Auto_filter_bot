import os
import asyncio
from pyrogram import Client
from info import Info

# Render पर बॉट को जगाए रखने के लिए एक वेब सर्वर
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run_web_server():
    app.run(host="0.0.0.0", port=int(Info.PORT))

Thread(target=run_web_server).start()


# Pyrogram Client
class Bot(Client):
    def __init__(self):
        super().__init__(
            "my_telegram_bot",
            api_id=Info.API_ID,
            api_hash=Info.API_HASH,
            bot_token=Info.BOT_TOKEN,
            plugins=dict(root="plugins") # प्लगइन्स फोल्डर को लोड करता है
        )

    async def start(self):
        await super().start()
        print("Bot is running...")

    async def stop(self, *args):
        await super().stop()
        print("Bot stopped.")

# बॉट को चलाएँ
if __name__ == "__main__":
    bot = Bot()
    bot.run()
