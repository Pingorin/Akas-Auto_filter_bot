# plugins/pm_filter.py
from bot import app
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from database.ia_filterdb import find_files

@app.on_message(filters.private & filters.text & ~filters.regex(r"^\/"))
async def pm_filter_handler(client: Client, message: Message):
    query = message.text
    results = await find_files(query, max_results=10)
    
    if not results:
        await message.reply("माफ़ करें, इस क्वेरी के लिए कोई फाइल नहीं मिली।")
        return
        
    buttons = []
    for file in results:
        buttons.append([
            InlineKeyboardButton(
                text=file['file_name'],
                callback_data=f"fwd_{file['link_id']}"
            )
        ])
        
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply(
        f"आपकी '{query}' क्वेरी के लिए यह परिणाम मिले:",
        reply_markup=reply_markup
    )
