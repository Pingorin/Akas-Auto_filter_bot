# bot.py
import asyncio
import os
from aiohttp import web
from pyrogram import Client, idle
from info import API_ID, API_HASH, BOT_TOKEN

# ज़रूरी इम्पोर्ट
from database.ia_filterdb import create_indexes 

# प्लगइन्स डिक्शनरी
plugins = dict(root="plugins")

# Pyrogram Client को शुरू करें
app = Client(
    "my_telegram_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=plugins
)

# --- AIOHTTP Web Server for Render ---
routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response({"status": "bot is running"})

async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    port = int(os.environ.get("PORT", 8080))
    await web.TCPSite(web.AppRunner(web_app), "0.0.0.0", port).start()
    print(f"Web server started on 0.0.0.0:{port}")

# --- Main Bot Function ---

async def main():
    print("Starting bot...")
    await create_indexes() 
    await app.start()
    print("Bot started!")
    
    # --- यहाँ बदलाव किया गया है ---
    # वेब सर्वर को एक बैकग्राउंड टास्क के रूप में शुरू करें
    asyncio.create_task(web_server())
    
    # अब idle() मुख्य थ्रेड को ब्लॉक करेगा, लेकिन वेब सर्वर चलता रहेगा
    print("Bot is now idle... (Waiting for updates)")
    await idle()
    
    print("Stopping bot...")
    await app.stop()
    print("Bot stopped.")

if __name__ == "__main__":
    asyncio.run(main())
