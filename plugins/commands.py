# plugins/commands.py
from bot import app  # Main client instance from bot.py
from pyrogram import filters, Client
from pyrogram.types import CallbackQuery, Message, InlineKeyboardButton, InlineKeyboardMarkup

# Class-based imports (जैसा आपने अपने कोड में इस्तेमाल किया)
from info import Info 
from Script import Script 

# Database imports
from database.users_chats_db import add_user
from database.ia_filterdb import get_file_details

@app.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message):
    user_name = message.from_user.first_name
    
    # Add user to database
    try:
        await add_user(message.from_user.id, message.from_user.username)
    except Exception as e:
        print(f"DB Error in start: {e}")
        
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
        caption=Script.START_TXT.format(user=user_name), # {user} का प्रयोग करें
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# --- Single Callback Query Handler (Best Practice) ---

@app.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    data = query.data

    # --- 1. File Forwarding Logic (पुराना लॉजिक) ---
    if data.startswith("fwd_"):
        try:
            link_id = int(data.split("_")[1])
            details = await get_file_details(link_id)
            
            if not details:
                await query.answer("Error: फाइल नहीं मिली (शायद हटा दी गई है)", show_alert=True)
                return
                
            await client.copy_message(
                chat_id=query.from_user.id,
                from_chat_id=details['chat_id'],
                message_id=details['msg_id']
            )
            await query.answer("फाइल भेजी जा रही है...", show_alert=False)
        except Exception as e:
            await query.answer(f"Error: {e}", show_alert=True)
            print(f"Forwarding error: {e}")
        return # हैंडलर से बाहर निकलें

    # --- 2. "About" Logic (आपका नया लॉजिक) ---
    elif data == "about":
        # अलर्ट के रूप में दिखाएँ
        await query.answer(Script.ABOUT_TXT, show_alert=True)
        return

    # --- 3. "Start Back" Logic (आपका नया लॉजिक) ---
    elif data == "start_back":
        buttons = [
            [InlineKeyboardButton("+ Add me to your group +", url=f"https://t.me/{client.me.username}?startgroup=true")],
            [
                InlineKeyboardButton("Update Channel", url=Info.UPDATE_CHANNEL),
                InlineKeyboardButton("Earn Money", callback_data="earn_money")
            ],
            [
                InlineKeyboardButton("Main Channel", url=Info.MAIN_CHANNEL),
                InlineKeyboardButton("Owner", url=f"https://t.me/{Info.OWNER_USERNAME}")
            ],
            [InlineKeyboardButton("About", callback_data="about")]
        ]
        try:
            # फोटो नहीं बदल रहे हैं, सिर्फ कैप्शन और बटन एडिट कर रहे हैं
            await query.message.edit_caption(
                caption=Script.START_TXT.format(user=query.from_user.first_name),
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        except Exception as e:
            print(f"Start Back Error: {e}")
        await query.answer()
        return

    # --- 4. "Earn Money" Main Menu (आपका नया लॉजिक) ---
    elif data == "earn_money":
        lang_buttons = [
            [
                InlineKeyboardButton("English", callback_data="lang_en"),
                InlineKeyboardButton("हिन्दी", callback_data="lang_hi")
            ],
            [
                InlineKeyboardButton("Telugu", callback_data="lang_te"),
                InlineKeyboardButton("Tamil", callback_data="lang_ta")
            ],
            [InlineKeyboardButton("« Back", callback_data="start_back")]
        ]
        try:
            # हम फोटो के नीचे कैप्शन और बटन बदल रहे हैं
            await query.message.edit_caption(
                caption="Please select your language:",
                reply_markup=InlineKeyboardMarkup(lang_buttons)
            )
        except Exception as e:
            print(f"Earn Money Error: {e}")
        await query.answer()
        return

    # --- 5. Language Selection Logic (आपका नया लॉजिक) ---
    elif data.startswith("lang_"):
        lang_code = data.split("_")[1]
        text = ""
        
        if lang_code == "en":
            text = Script.EARN_MONEY_ENGLISH
        elif lang_code == "hi":
            text = Script.EARN_MONEY_HINDI
        elif lang_code == "te":
            text = Script.EARN_MONEY_TELUGU
        elif lang_code == "ta":
            text = Script.EARN_MONEY_TAMIL

        buttons = [
            [InlineKeyboardButton("« Back", callback_data="earn_money")] # वापस भाषा सूची पर जाएँ
        ]
        
        try:
            # *** महत्वपूर्ण सुधार: edit_text की जगह edit_caption ***
            await query.message.edit_caption(
                caption=text,
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        except Exception as e:
            print(f"Language Select Error: {e}")
        await query.answer()
        return

    # --- Default answer ---
    await query.answer()
