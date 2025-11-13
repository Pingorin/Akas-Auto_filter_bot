from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from info import Info
from Script import Script

@Client.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    user_name = message.from_user.first_name
    
    # स्टार्ट मैसेज के लिए बटन
    buttons = [
        [
            InlineKeyboardButton("+ Add me to your group +", url=f"https://t.me/{client.me.username}?startgroup=true")
        ],
        [
            InlineKeyboardButton("Update Channel", url=Info.UPDATE_CHANNEL),
            InlineKeyboardButton("Earn Money", callback_data="earn_money")
        ],
        [
            InlineKeyboardButton("Main Channel", url=Info.MAIN_CHANNEL),
            InlineKeyboardButton("Owner", url=f"https://t.me/{Info.OWNER_USERNAME}")
        ],
        [
            InlineKeyboardButton("About", callback_data="about")
        ]
    ]
    
    await message.reply_photo(
        photo=Info.Norm_pic,
        caption=Script.START_TXT.format(user_name),
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# --- Callback Query Handlers ---

@Client.on_callback_query(filters.regex("earn_money"))
async def earn_money_callback(client, query: CallbackQuery):
    # भाषा चुनने के लिए बटन
    lang_buttons = [
        [
            InlineKeyboardButton("English", callback_data="lang_en"),
            InlineKeyboardButton("हिन्दी", callback_data="lang_hi")
        ],
        [
            InlineKeyboardButton("Telugu", callback_data="lang_te"),
            InlineKeyboardButton("Tamil", callback_data="lang_ta")
        ],
        [
            InlineKeyboardButton("« Back", callback_data="start_back")
        ]
    ]
    
    await query.message.edit_reply_markup(
        reply_markup=InlineKeyboardMarkup(lang_buttons)
    )

@Client.on_callback_query(filters.regex(r"^lang_"))
async def language_callback(client, query: CallbackQuery):
    lang_code = query.data.split("_")[1]
    text = ""
    
    if lang_code == "en":
        text = Script.EARN_MONEY_ENGLISH
    elif lang_code == "hi":
        text = Script.EARN_MONEY_HINDI
    elif lang_code == "te":
        text = Script.EARN_MONEY_TELUGU
    elif lang_code == "ta":
        text = Script.EARN_MONEY_TAMIL

    # भाषा डिटेल्स दिखाने के लिए बटन
    buttons = [
        [InlineKeyboardButton("« Back", callback_data="earn_money")] # वापस भाषा सूची पर जाएँ
    ]
    
    await query.message.edit_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True
    )

@Client.on_callback_query(filters.regex("about"))
async def about_callback(client, query: CallbackQuery):
    # About टेक्स्ट को अलर्ट के रूप में दिखाएँ
    await query.answer(Script.ABOUT_TXT, show_alert=True)

@Client.on_callback_query(filters.regex("start_back"))
async def start_back_callback(client, query: CallbackQuery):
    # मुख्य स्टार्ट मेनू पर वापस जाएँ
    buttons = [
        [
            InlineKeyboardButton("+ Add me to your group +", url=f"https://t.me/{client.me.username}?startgroup=true")
        ],
        [
            InlineKeyboardButton("Update Channel", url=Info.UPDATE_CHANNEL),
            InlineKeyboardButton("Earn Money", callback_data="earn_money")
        ],
        [
            InlineKeyboardButton("Main Channel", url=Info.MAIN_CHANNEL),
            InlineKeyboardButton("Owner", url=f"https://t.me/{Info.OWNER_USERNAME}")
        ],
        [
            InlineKeyboardButton("About", callback_data="about")
        ]
    ]
    
    # फोटो नहीं बदल रहे हैं, सिर्फ कैप्शन और बटन एडिट कर रहे हैं
    await query.message.edit_caption(
        caption=Script.START_TXT.format(query.from_user.first_name),
        reply_markup=InlineKeyboardMarkup(buttons)
    )
