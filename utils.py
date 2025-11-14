# utils.py
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from info import BOT_USERNAME, UPDATE_CHANNEL, MAIN_CHANNEL, OWNER_USERNAME
from Script import Script

def gen_start_keyboard():
    """Generates the main start keyboard."""
    buttons = [
        [InlineKeyboardButton("+ Add me to your group +", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
        [
            InlineKeyboardButton("Update Channel", url=UPDATE_CHANNEL),
            InlineKeyboardButton("Earn Money", callback_data="earn_money")
        ],
        [
            InlineKeyboardButton("Main Channel", url=MAIN_CHANNEL),
            InlineKeyboardButton("Owner", url=f"https://t.me/{OWNER_USERNAME}")
        ],
        [InlineKeyboardButton("About", callback_data="about")]
    ]
    return InlineKeyboardMarkup(buttons)

def gen_earn_keyboard():
    """Generates the 'Earn Money' language selection keyboard."""
    buttons = [
        [
            InlineKeyboardButton("English", callback_data="earn_lang_english"),
            InlineKeyboardButton("Hindi", callback_data="earn_lang_hindi")
        ],
        [
            InlineKeyboardButton("Telugu", callback_data="earn_lang_telugu"),
            InlineKeyboardButton("Tamil", callback_data="earn_lang_tamil")
        ],
        [InlineKeyboardButton("⬅️ Back", callback_data="start_back")]
    ]
    return InlineKeyboardMarkup(buttons)

def gen_back_keyboard(back_to="start_back"):
    """Generates a simple 'Back' keyboard."""
    buttons = [[InlineKeyboardButton("⬅️ Back", callback_data=back_to)]]
    return InlineKeyboardMarkup(buttons)
