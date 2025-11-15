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
    """
    await message.reply(
        text="इंडेक्सिंग शुरू करने के लिए, कृपया उस चैनल से **कोई भी एक मैसेज** (या आखिरी मैसेज) यहाँ फॉरवर्ड करें।\n\n(ध्यान दें: इंडेक्सिंग के लिए बॉट का उस चैनल में एडमिन होना ज़रूरी है।)",
        reply_markup=ForceReply(selective=True) 
    )

# 2. फॉरवर्ड किए गए मैसेज को हैंडल करना
@Client.on_message(filters.private & filters.user(OWNER_ID) & filters.forwarded)
async def index_forwarded_message(client: Client, message: Message):
    """
    Handles the forwarded message from the owner.
    """
    
    if not message.forward_from_chat:
        await message.reply("एरर: यह फॉरवर्ड किया गया मैसेज किसी चैनल से नहीं है।")
        return

    chat_id = message.forward_from_chat.id
    chat_title = message.forward_from_chat.title or "यह चैनल"

    # --- DEBUGGING (डीबगिंग) ---
    try:
        print(f"Checking permissions for chat_id: {chat_id}...") # यह Render Log में प्रिंट होगा
        member = await client.get_chat_member(chat_id, "me")
        
        # यह Render Log में प्रिंट होगा
        print(f"Bot status in channel is: {member.status}") 
        
        if member.status not in ('administrator', 'creator'):
             print("Bot is NOT an admin. Failing.") # यह Render Log में प्रिंट होगा
             await message.reply(f"एरर: मैं '{chat_title}' में एडमिन नहीं हूँ। कृपया मुझे पहले एडमिन बनाएँ।")
             return
             
    except UserNotParticipant:
         print("Bot is not a participant in the channel.") # यह Render Log में प्रिंट होगा
         await message.reply(f"एरर: मैं '{chat_title}' का सदस्य (member) नहीं हूँ। कृपया मुझे पहले चैनल में जोड़ें और फिर एडमिन बनाएँ।")
         return
    except Exception as e:
         print(f"Error during permission check: {e}") # यह Render Log में प्रिंट होगा
         await message.reply(f"चैनल की जाँच करते समय एक एरर आया: {e}")
         return
    # --- END DEBUGGING ---

    # 3. इंडेक्सिंग प्रक्रिया शुरू करें
    print("Bot is admin. Starting indexing...") # यह Render Log में प्रिंट होगा
    status_msg = await message.reply(f"'{chat_title}' के लिए इंडेक्सिंग शुरू हो रही है...\n(यह प्रक्रिया धीमी हो सकती है)")
    
    total_files = 0
    indexed_files = 0
    
    try:
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
        print(f"Error during indexing: {e}") # यह Render Log में प्रिंट होगा
        await status_msg.edit(f"इंडेक्सिंग के दौरान एक एरर आया: {e}")
        return
        
    await status_msg.edit(f"**'{chat_title}' के लिए इंडेक्सिंग पूरी हुई!**\n\...कुल नई फाइलें इंडेक्स की गईं: {indexed_files}")
