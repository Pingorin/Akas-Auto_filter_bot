from database import db

# 'ia_filters' नाम का एक कलेक्शन बनाएँ
filters_coll = db["ia_filters"]

# यहाँ अपने फिल्टर से संबंधित फ़ंक्शन जोड़ें
# उदा:
# async def add_filter(filter_name, content):
#     await filters_coll.insert_one({'name': filter_name, 'content': content})
