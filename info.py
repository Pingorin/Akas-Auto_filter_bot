# info.py
import os
import sys

# --- क्रिटिकल वेरिएबल्स (Critical Variables) ---
# ये Render एनवायरनमेंट वेरिएबल्स से आने चाहिए
# इनके बिना बॉट शुरू नहीं होगा

BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
API_ID = os.environ.get("API_ID", None)
API_HASH = os.environ.get("API_HASH", None)
MONGO_DB_URI = os.environ.get("DB_URI", None) # हमने इसे DB_URI से MONGO_DB_URI नाम दिया था
OWNER_ID = os.environ.get("OWNER_ID", None) # /index कमांड के लिए यह ज़रूरी है

# --- जांच करें कि क्रिटिकल वेरिएबल्स सेट हैं या नहीं ---
if BOT_TOKEN is None:
    print("Error: BOT_TOKEN एनवायरनमेंट वेरिएबल सेट नहीं है।")
    sys.exit(1)
if API_ID is None:
    print("Error: API_ID एनवायरनमेंट वेरिएबल सेट नहीं है।")
    sys.exit(1)
if API_HASH is None:
    print("Error: API_HASH एनवायरनमेंट वेरिएबल सेट नहीं है।")
    sys.exit(1)
if MONGO_DB_URI is None:
    print("Error: MONGO_DB_URI (या DB_URI) एनवायरनमेंट वेरिएबल सेट नहीं है।")
    sys.exit(1)
if OWNER_ID is None:
    print("Error: OWNER_ID एनवायरनमेंट वेरिएबल सेट नहीं है। (/index काम नहीं करेगा)")
    sys.exit(1)

# --- वेरिएबल्स को सही टाइप में बदलें ---
try:
    API_ID = int(API_ID)
    OWNER_ID = int(OWNER_ID)
except ValueError:
    print("Error: API_ID और OWNER_ID इंटीजर (नंबर) होने चाहिए।")
    sys.exit(1)


# --- वैकल्पिक वेरिएबल्स (Optional Variables) ---
# ये डिफ़ॉल्ट वैल्यू का उपयोग कर सकते हैं

# Bot Info
Norm_pic = os.environ.get("Norm_pic", "https://graph.org/file/4d61886e61dfa37a25945.jpg")
OWNER_USERNAME = os.environ.get("OWNER_USERNAME", "YourUsername")

# Channel Links
UPDATE_CHANNEL = os.environ.get("UPDATE_CHANNEL", "https://t.me/YourChannel")
MAIN_CHANNEL = os.environ.get("MAIN_CHANNEL", "https://t.me/YourMainChannel")

# (PORT को यहाँ से हटा दिया गया है क्योंकि यह bot.py में पहले से ही हैंडल किया गया है)
