import asyncio
import os
from aiohttp import web
from pyrogram import Client, idle

# आपकी info.py फ़ाइल से Info क्लास को इम्पोर्ट करें
# (हम यह मान रहे हैं कि आपकी info.py में 'Info' नाम की एक क्लास है)
try:
    from info import Info
except ImportError:
    print("Error: 'info.py' not found or 'Info' class not defined.")
    # फ़ॉलबैक, यदि Info क्लास मौजूद नहीं है (हालांकि यह विफल हो सकता है)
    from info import API_ID, API_HASH, BOT_TOKEN, OWNER_ID

# हमारे डेटाबेस इंडेक्सिंग फ़ंक्शन को इम्पोर्ट करें
from database.ia_filterdb import create_indexes

# --- AIOHTTP Web Server (Render के लिए) ---
# यह Flask से बेहतर है क्योंकि यह asyncio-नेटिव है

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    """Render को बताने के लिए कि बॉट ज़िंदा है।"""
    return web.json_response({"status": "bot_is_running"})

async def web_server():
    """असिंक्रोनस वेब सर्वर शुरू करता है।"""
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    
    # Render द्वारा दिया गया PORT या डिफ़ॉल्ट 8080 का उपयोग करें
    port = int(os.environ.get("PORT", 8080))
    
    try:
        await web.TCPSite(web.AppRunner(web_app), "0.0.0.0", port).start()
        print(f"Web server started successfully on 0.0.0.0:{port}")
    except Exception as e:
        print(f"Error starting web server: {e}")

# --- Pyrogram Client Setup ---

# Info क्लास का उपयोग करके वेरिएबल्स को एक्सेस करें
# (अगर Info क्लास मौजूद है)
if 'Info' in globals():
    API_ID = Info.API_ID
    API_HASH = Info.API_HASH
    BOT_TOKEN = Info.BOT_TOKEN

# प्लगइन्स डायरेक्टरी को डिफाइन करें
plugins = dict(root="plugins")

# Pyrogram Client इंस्टेंस बनाएँ
app = Client(
    "my_telegram_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=plugins
)

# --- Main Bot Function ---

async def main():
    """
    सही क्रम में बॉट को शुरू करता है।
    """
    print("Bot starting...")
    
    # 1. सबसे पहले, डेटाबेस इंडेक्स बनाएँ (बहुत ज़रूरी)
    try:
        await create_indexes()
    except Exception as e:
        print(f"Error creating database indexes: {e}")
        # अगर इंडेक्स नहीं बनते हैं तो बॉट को रोक दें
        return

    # 2. Pyrogram क्लाइंट शुरू करें
    await app.start()
    print("Pyrogram client started!")
    
    # 3. Render के लिए वेब सर्वर शुरू करें
    await web_server()
    
    # 4. बॉट को चालू रखें
    print("Bot is now idle and listening for updates.")
    await idle()
    
    # 5. बॉट को रोकें (जब idle() टूटता है)
    print("Stopping bot...")
    await app.stop()
    print("Bot stopped.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot shutdown initiated by user.")
