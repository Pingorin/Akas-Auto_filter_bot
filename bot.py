# bot.py
import asyncio
import os
from aiohttp import web
from pyrogram import Client, idle
from info import API_ID, API_HASH, BOT_TOKEN

# ज़रूरी इम्पोर्ट
from database.ia_filterdb import create_indexes 

# Define plugins root
plugins = dict(root="plugins")

# Initialize the Pyrogram Client
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
    
    # --- यहाँ इंडेक्स बनाएँ ---
    await create_indexes() 
    
    await app.start()
    print("Bot started!")
    
    # Start the web server
    await web_server()
    
    # Keep the bot running
    await idle()
    
    print("Stopping bot...")
    await app.stop()
    print("Bot stopped.")

if __name__ == "__main__":
    asyncio.run(main())
