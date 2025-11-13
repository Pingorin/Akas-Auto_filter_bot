from motor.motor_asyncio import AsyncIOMotorClient
from info import Info

# MongoDB Client
mongo_client = AsyncIOMotorClient(Info.DB_URI)
db = mongo_client["telegram_bot_db"] # आप डेटाबेस का नाम बदल सकते हैं
