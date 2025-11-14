# database/__init__.py
from motor.motor_asyncio import AsyncIOMotorClient
from info import MONGO_DB_URI  # <-- यह सही लाइन है

# Initialize Motor Client
client = AsyncIOMotorClient(MONGO_DB_URI)
db = client.telegram_bot_db
