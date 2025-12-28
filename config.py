from os import getenv

API_ID = int(getenv("API_ID", ""))
API_HASH = getenv("API_HASH", "")
BOT_TOKEN = getenv("BOT_TOKEN", "")
OWNER_ID = list(map(int, getenv("OWNER_ID", "").split()))
MONGO_DB = getenv("MONGO_DB", "")
LOG_GROUP = getenv("LOG_GROUP", "")
CHANNEL_ID = int(getenv("CHANNEL_ID", ""))
FREEMIUM_LIMIT = int(getenv("FREEMIUM_LIMIT", "1"))
PREMIUM_LIMIT = int(getenv("PREMIUM_LIMIT", "500000000000000000"))
WEBSITE_URL = getenv("WEBSITE_URL", "linkpays.in")
AD_API = getenv("AD_API", "b157b12a7401a9aea61e840e39a282f819a40a44")
STRING = getenv("STRING", None)
YT_COOKIES = getenv("YT_COOKIES", None)
INSTA_COOKIES = getenv("INSTA_COOKIES", None)
SECONDS = 300  # for example, a 5-minute delay
