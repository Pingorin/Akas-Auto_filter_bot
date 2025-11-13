# plugins/index.py
import asyncio
from bot import app
from pyrogram import filters, Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from info import OWNER_ID
from database.ia_filterdb import add_file, is_file_indexed

@app.on_message(filters.command("index") & filters.user(OWNER_ID))
async def index_files_command(client: Client, message: Message):
    """
    /index कमांड हैंडलर
    चैनल/ग्रुप के सभी मैसेजों को इंडेक्स करता है।
    """
    chat_id = message.chat.id
    
    status_msg = await message.reply("Indexing started...\n(यह प्रक्रिया धीमी हो सकती है)")
    
    total_files = 0
    indexed_files = 0
    
    try:
        # iter_messages का उपयोग करके नए से पुराने तक सभी मैसेज प्राप्त करें
        async for msg in client.iter_messages(chat_id):
            total_files += 1
            
            # हर 500 फाइलों पर स्टेटस अपडेट करें
            if total_files % 500 == 0:
                try:
                    await status_msg.edit(f"Scanned: {total_files} messages\nIndexed: {indexed_files} files")
                except FloodWait as e:
                    await asyncio.sleep(e.value) # FloodWait को हैंडल करें
            
            # केवल मीडिया फाइलों (वीडियो/डॉक्यूमेंट/ऑडियो) में रुचि है
            if msg.media:
                # जांचें कि क्या यह पहले से ही इंडेक्स है
                if await is_file_indexed(msg.id, chat_id):
                    continue # अगर है, तो छोड़ दें
                
                # फाइल का नाम प्राप्त करें
                file_name = None
                if msg.document:
                    file_name = msg.document.file_name
                elif msg.video:
                    file_name = msg.video.file_name
                elif msg.audio:
                    file_name = msg.audio.file_name
                
                if not file_name:
                    file_name = "Unknown File" # अगर नाम नहीं मिलता है
                    
                # कैप्शन प्राप्त करें
                caption = msg.caption if msg.caption else ""
                
                # डेटाबेस में जोड़ें
                if await add_file(msg.id, chat_id, file_name, caption):
                    indexed_files += 1
                    
    except Exception as e:
        await status_msg.edit(f"An error occurred: {e}")
        return
        
    await status_msg.edit(f"**Indexing Complete!**\n\nTotal Messages Scanned: {total_files}\nNew Files Indexed: {indexed_files}")
