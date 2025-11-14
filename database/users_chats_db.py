# database/users_chats_db.py
import datetime
from database import db

users_coll = db.users

async def add_user(user_id, username):
    """Adds a new user to the database."""
    user = dict(
        _id=int(user_id),
        username=username,
        joined_date=datetime.datetime.now() # Use datetime.datetime.now()
    )
    try:
        await users_coll.update_one(
            {"_id": user_id},
            {"$set": user},
            upsert=True
        )
    except Exception as e:
        print(f"Error adding user: {e}")

async def get_user(user_id):
    """Finds a user by their ID."""
    return await users_coll.find_one({"_id": int(user_id)})
