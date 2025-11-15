# plugins/index.py
from pyrogram import filters, Client # <-- '@Client' यहाँ है
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from info import OWNER_ID
from database.ia_filterdb import add_file, is_file_indexed
import asyncio

# '@Client' का उपयोग करें, '@app' का नहीं
@Client.on_message(filters.command("index") & filters.user(OWNER_ID))
async def index_files_command(client: Client, message: Message):
    """
    /index कमांड हैंडलर
    """
    chat_id = message.chat.id
    status_msg = await message.reply("Indexing started...\n(यह प्रक्रिया धीमी हो सकती है)")
    
    total_files = 0
    indexed_files = 0
    
    try:
        async for msg in client.iter_messages(chat_id):
            total_files += 1
            
            if total_files % 500 == 0:
                try:
                    await status_msg.edit(f"Scanned: {total_files} messages\nIndexed: {indexed_files} files")
                except FloodWait as e:
                    await asyncio.sleep(e.value)
            
            if msg.media:
                if await is_file_indexed(msg.id, chat_id):
                    continue 
                
                file_name = None
                if msg.document:
                    file_name = msg.document.file_name
                elif msg.video:
                    file_name = msg.video.file_name
                elif msg.audio:
                    file_name = msg.audio.file_name
                
                if not file_name:
                    file_name = "Unknown File" 
                    
                caption = msg.caption if msg.caption else ""
                
                if await add_file(msg.id, chat_id, file_name, caption):
                    indexed_files += 1
                    
    except Exception as e:
        await status_msg.edit(f"An error occurred: {e}")
        return
        
    await status_msg.edit(f"**Indexing Complete!**\n\nTotal Messages Scanned: {total_files}\nNew Files Indexed: {indexed_files}")
