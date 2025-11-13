# database/__init__.py
from motor.motor_asyncio import AsyncIOMotorClient
from info import MONGO_DB_URI  # <-- यह सही तरीका है (Info.MONGO_DB_URI नहीं)

# Initialize Motor Client
client = AsyncIOMotorClient(MONGO_DB_URI)
db = client.telegram_bot_db  # आप चाहें तो 'telegram_bot_db' का नाम बदल सकते हैं
