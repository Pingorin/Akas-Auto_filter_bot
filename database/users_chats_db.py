from database import db

# 'users' और 'chats' के लिए कलेक्शन
users_coll = db["users"]
chats_coll = db["chats"]

# यहाँ यूजर्स और चैट्स से संबंधित फ़ंक्शन जोड़ें
# उदा:
# async def add_user(user_id):
#     await users_coll.insert_one({'_id': user_id})
