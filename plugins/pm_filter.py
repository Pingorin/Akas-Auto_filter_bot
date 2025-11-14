# plugins/pm_filter.py
from bot import app
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from database.ia_filterdb import find_files

@app.on_message(filters.private & filters.text & ~filters.command) # <-- यह सही लाइन है
async def pm_filter_handler(client: Client, message: Message):
    """
    ऑटो-फिल्टर (सर्च) हैंडलर
    """
    query = message.text
    
    # 1. डेटाबेस में फाइलें खोजें
    results = await find_files(query, max_results=10)
    
    # 2. अगर कुछ नहीं मिला
    if not results:
        await message.reply("माफ़ करें, इस क्वेरी के लिए कोई फाइल नहीं मिली।")
        return
        
    # 3. अगर परिणाम मिलते हैं, तो बटन बनाएँ
    buttons = []
    for file in results:
        # बटन का टेक्स्ट फाइल का नाम होगा
        # कॉलबैक डेटा 'fwd_' + link_id होगा
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
