from database import db

# 1. आपके दो कलेक्शन्स
files_data = db.files_data
files_search = db.files_search

# 2. कस्टम इंटीजर ID के लिए काउंटर्स कलेक्शन
counters = db.counters

async def get_next_sequence_id(name="file_id"):
    """
    कस्टम ऑटो-इंक्रीमेंटिंग इंटीजर ID (जैसे 1, 2, 3...) जेनरेट करता है।
    """
    ret = await counters.find_one_and_update(
        {'_id': name},
        {'$inc': {'seq': 1}},
        upsert=True,
        return_document=True
    )
    if ret is None:
        await counters.update_one({'_id': name}, {'$set': {'seq': 1}}, upsert=True)
        return 1
    return ret['seq']

async def create_indexes():
    """
    तेज़ सर्चिंग के लिए टेक्स्ट इंडेक्स बनाता है।
    """
    print("Creating database indexes...")
    
    # [UPDATE] Text index is now only on the new 'search_tags' field for efficiency
    # and case-insensitive search.
    await files_search.create_index(
        [('search_tags', 'text')],
        name='search_index',
        default_language='none' # सभी भाषाओं को सपोर्ट करने के लिए
    )
    
    # files_data पर msg_id और chat_id का इंडेक्स (डुप्लिकेट चेकिंग के लिए)
    await files_data.create_index(
        [
            ('msg_id', 1),
            ('chat_id', 1)
        ],
        name='file_index',
        unique=True # एक ही फाइल दोबारा सेव नहीं होगी
    )
    
    # [NEW] Added an index on link_id for potential faster lookups
    await files_search.create_index('link_id', name='link_id_index')
    
    print("Indexes created successfully.")


async def add_file(msg_id, chat_id, file_name, caption):
    """
    फाइल को दो-कलेक्शन आर्किटेक्चर में सेव करता है।
    """
    try:
        # 1. नया यूनिक इंटीजर ID प्राप्त करें
        new_id = await get_next_sequence_id()
        
        # 2. Collection 1 (files_data) में फॉरवर्डिंग जानकारी डालें
        await files_data.insert_one({
            '_id': new_id,
            'msg_id': msg_id,
            'chat_id': chat_id
        })
        
        # [UPDATE] Create a combined lowercase string for searching
        search_caption = caption.lower() if caption else ""
        search_tags = f"{file_name.lower()} {search_caption}"
        
        # 3. Collection 2 (files_search) में सर्चिंग जानकारी डालें
        await files_search.insert_one({
            'file_name': file_name,  # Store original file_name for display
            'caption': caption if caption else "", # Store original caption
            'search_tags': search_tags, # Store lowercase tags for searching
            'link_id': new_id  # file_data के _id से लिंक करें
        })
        return True
    except Exception as e:
        # डुप्लिकेट एंट्री होने पर यह एरर देगा, जो ठीक है
        print(f"Error adding file: {e}")
        return False

async def is_file_indexed(msg_id, chat_id):
    """
    जांच करता है कि क्या कोई फाइल पहले से ही files_data में है।
    """
    return bool(await files_data.find_one({"msg_id": msg_id, "chat_id": chat_id}))

async def find_files(query_text, max_results=10):
    """
    टेक्स्ट इंडेक्स का उपयोग करके फ़ाइलों को खोजता है।
    यह file_name और link_id लौटाता है।
    """
    
    # [UPDATE] Search using the lowercase version of the query
    search_query = query_text.lower()
    
    cursor = files_search.find(
        {'$text': {'$search': search_query}},
        # Return the original 'file_name' for display
        {'file_name': 1, 'link_id': 1, '_id': 0} 
    ).limit(max_results)
    
    return [doc async for doc in cursor]

async def get_file_details(link_id):
    """
    फॉरवर्डिंग के लिए 'link_id' का उपयोग करके msg_id और chat_id प्राप्त करता है।
    """
    # _id is already indexed (Primary Key), so this is very fast
    return await files_data.find_one({'_id': int(link_id)})
