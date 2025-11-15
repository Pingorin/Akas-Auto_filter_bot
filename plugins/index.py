# plugins/index.py
from pyrogram import filters, Client
from pyrogram.types import Message, ForceReply
from pyrogram.errors import FloodWait, UserNotParticipant
from info import OWNER_ID
from database.ia_filterdb import add_file, is_file_indexed
import asyncio

# 1. /index कमांड (केवल PM में और केवल ओनर के लिए)
@Client.on_message(filters.command("index") & filters.private & filters.user(OWNER_ID))
async def index_command_pm(client: Client, message: Message):
    """
    Handles the /index command in PM.
    Asks the user to forward a message from the target channel.
    """
    await message.reply(
        text="इंडेक्सिंग शुरू करने के लिए, कृपया उस चैनल से **कोई भी एक मैसेज** (या आखिरी मैसेज) यहाँ फॉरवर्ड करें।\n\n(ध्यान दें: इंडेक्सिंग के लिए बॉट का उस चैनल में एडमिन होना ज़रूरी है।)",
        reply_markup=ForceReply(selective=True) # यह यूज़र को रिप्लाई करने के लिए फ़ोर्स करता है
    )

# 2. फॉरवर्ड किए गए मैसेज को हैंडल करना (केवल PM में और केवल ओनर से)
@Client.on_message(filters.private & filters.user(OWNER_ID) & filters.forwarded)
async def index_forwarded_message(client: Client, message: Message):
    """
    Handles the forwarded message from the owner.
    """
    
    if not message.forward_from_chat:
        await message.reply("एरर: यह फॉरवर्ड किया गया मैसेज किसी चैनल से नहीं है।")
        return

    # 1. चैनल ID और टाइटल प्राप्त करें
    chat_id = message.forward_from_chat.id
    chat_title = message.forward_from_chat.title or "यह चैनल"

    # 2. जांचें कि क्या बॉट उस चैनल में एडमिन है
    try:
        member = await client.get_chat_member(chat_id, "me")
        if member.status not in ('administrator', 'creator'):
             await message.reply(f"एरर: मैं '{chat_title}' में एडमिन नहीं हूँ। कृपया मुझे पहले एडमिन बनाएँ।")
             return
    except UserNotParticipant:
         await message.reply(f"एरर: मैं '{chat_title}' का सदस्य (member) नहीं हूँ। कृपया मुझे पहले चैनल में जोड़ें और फिर एडमिन बनाएँ।")
         return
    except Exception as e:
         await message.reply(f"चैनल की जाँच करते समय एक एरर आया: {e}")
         return

    # 3. इंडेक्सिंग प्रक्रिया शुरू करें
    status_msg = await message.reply(f"'{chat_title}' के लिए इंडेक्सिंग शुरू हो रही है...\n(यह प्रक्रिया धीमी हो सकती है)")
    
    total_files = 0
    indexed_files = 0
    
    try:
        # सही chat_id का उपयोग करके चैनल के मैसेज को इटरेट (iterate) करें
        async for msg in client.iter_messages(chat_id):
            total_files += 1
            
            if total_files % 500 == 0:
                try:
                    await status_msg.edit(f"स्कैन किए गए: {total_files} मैसेज\nइंडेक्स की गई: {indexed_files} फाइलें")
                except FloodWait as e:
                    await asyncio.sleep(e.value)
            
            if msg.media:
                if await is_file_indexed(msg.id, chat_id):
                    continue 
                
                file_name = None
                if msg.document: file_name = msg.document.file_name
                elif msg.video: file_name = msg.video.file_name
                elif msg.audio: file_name = msg.audio.file_name
                
                if not file_name: file_name = "Unknown File" 
                caption = msg.caption if msg.caption else ""
                
                if await add_file(msg.id, chat_id, file_name, caption):
                    indexed_files += 1
                    
    except Exception as e:
        await status_msg.edit(f"इंडेक्सिंग के दौरान एक एरर आया: {e}")
        return
        
    await status_msg.edit(f"**'{chat_title}' के लिए इंडेक्सिंग पूरी हुई!**\n\nकुल स्कैन किए गए मैसेज: {total_files}\nकुल नई फाइलें इंडेक्स की गईं: {indexed_files}")
