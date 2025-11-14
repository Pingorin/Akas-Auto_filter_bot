# plugins/commands.py
# 'from bot import app' को हटा दिया गया है
from pyrogram import filters, Client # <-- यहाँ 'Client' इम्पोर्ट करें
from pyrogram.types import CallbackQuery, Message
from info import Norm_pic, OWNER_USERNAME
from Script import Script
from utils import gen_start_keyboard, gen_earn_keyboard, gen_back_keyboard
from database.users_chats_db import add_user
from database.ia_filterdb import get_file_details

# '@app' को '@Client' (बड़े 'C' के साथ) से बदलें
@Client.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message):
    """Handles the /start command."""
    try:
        await add_user(message.from_user.id, message.from_user.username)
    except Exception as e:
        print(f"Error in DB: {e}")
        
    await message.reply_photo(
        photo=Norm_pic,
        caption=Script.START_TXT.format(user=message.from_user.first_name),
        reply_markup=gen_start_keyboard()
    )

# '@app' को '@Client' (बड़े 'C' के साथ) से बदलें
@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    """Handles all callback button clicks."""
    data = query.data
    
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
        
        return 
    
    caption_text = Script.START_TXT.format(user=query.from_user.first_name)
    reply_markup = gen_start_keyboard()

    if data == "about":
        caption_text = Script.ABOUT_TXT.format(owner=OWNER_USERNAME) 
        reply_markup = gen_back_keyboard(back_to="start_back")
    
    elif data == "earn_money":
        caption_text = "Please select your language:"
        reply_markup = gen_earn_keyboard()

    elif data.startswith("earn_lang_"):
        lang = data.split("_")[-1]
        if lang == "english":
            caption_text = Script.EARN_MONEY_TXT_ENGLISH
        elif lang == "hindi":
            caption_text = Script.EARN_MONEY_TXT_HINDI
        elif lang == "telugu":
            caption_text = Script.EARN_MONEY_TXT_TELUGU
        elif lang == "tamil":
            caption_text = Script.EARN_MONEY_TXT_TAMIL
        
        reply_markup = gen_back_keyboard(back_to="earn_money")
    
    try:
        await query.message.edit_caption(
            caption=caption_text,
            reply_markup=reply_markup
        )
    except Exception as e:
        print(f"Callback Error: {e}") 
    
    try:
        await query.answer()
    except:
        pass
