# bot.py
import asyncio
import os
from aiohttp import web
from pyrogram import Client
from info import API_ID, API_HASH, BOT_TOKEN
from database.ia_filterdb import create_indexes 

# --- AIOHTTP Web Server for Render ---
routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response({"status": "bot is running"})

# --- Main Bot Function ---
async def main():
    print("Starting bot...")
    await create_indexes() 
    
    # --- यहाँ बदलाव किया गया है ---
    # Client को main() के अंदर शुरू करें
    plugins = dict(root="plugins")
    
    app = Client(
        "my_telegram_bot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
        plugins=plugins
    )
    
    # Client को 'app' वेरिएबल पास करने के लिए
    # web_app.app = app 
    
    await app.start()
    print("Bot started!")
    
    # --- Web server logic (Render के लिए अपडेट किया गया) ---
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    port = int(os.environ.get("PORT", 8080)) # Render यह PORT वेरिएबल देता है
    
    # वेब सर्वर रनर बनाएँ
    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    
    # वेब सर्वर शुरू करें
    await site.start()
    print(f"Web server started on 0.0.0.0:{port}")
    
    # बॉट (और सर्वर) को हमेशा के लिए जीवित रखें
    await asyncio.Event().wait() # यह idle() की जगह लेता है

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped manually.")
