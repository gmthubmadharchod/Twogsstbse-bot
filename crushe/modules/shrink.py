from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, message
import random
import requests
import string
import aiohttp
from crushe import app
from crushe.core.func import *
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DB, WEBSITE_URL, AD_API # you can edit this by any short link provider

# MongoDB setup
tclient = AsyncIOMotorClient(MONGO_DB)
tdb = tclient["telegram_bot"]
token = tdb["tokens"]

# Create a TTL index for sessions collection
async def create_ttl_index():
    await token.create_index("expires_at", expireAfterSeconds=0)


# In-memory parameter storage
Param = {}


async def generate_random_param(length=8):
    """Generate a random parameter."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


async def get_shortened_url(deep_link):
    api_url = f"https://{WEBSITE_URL}/api?api={AD_API}&url={deep_link}"
    
    # Use aiohttp to perform an asynchronous request
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            if response.status == 200:
                data = await response.json()  # Get the JSON response asynchronously
                if data.get("status") == "success":
                    return data.get("shortenedUrl")
    return None


async def is_user_verified(user_id):
    """Check if a user has an active session."""
    session = await token.find_one({"user_id": user_id})
    return session is not None


@app.on_message(filters.command("start"))
async def token_handler(client, message):
    """Handle the /start command."""
    join = await subscribe(client, message)
    if join == 1:
        return

    user = message.from_user
    user_mention = f"[{user.first_name}](tg://user?id={user.id})"

    # Random image selection
    images = [
        "https://ar-hosting.pages.dev/1752942103938.jpg",
        "https://ar-hosting.pages.dev/1752942111453.jpg",
        "https://ar-hosting.pages.dev/1752942103004.jpg",
        "https://ar-hosting.pages.dev/1752942106446.jpg",
        "https://ar-hosting.pages.dev/1752942105659.jpg",
        "https://ar-hosting.pages.dev/1752942104883.jpg",
        "https://ar-hosting.pages.dev/1752942110594.jpg",
        "https://ar-hosting.pages.dev/1752942113175.jpg",
        "https://ar-hosting.pages.dev/1752942112328.jpg",
    ]
    image_url = random.choice(images)

    join_button = InlineKeyboardButton("Join Channel", url="https://t.me/Team_Sonu1")
    premium = InlineKeyboardButton("Get Premium", url="https://t.me/sonuporsa")
    keyboard = InlineKeyboardMarkup([
        [join_button],
        [premium]
    ])

    if len(message.command) <= 1:
        await message.reply_photo(
            photo=image_url,
            caption=(
                f"Hi 👋 {user_mention}, welcome!\n\n"
                "✳️ I can save posts from channels or groups where forwarding is off.\n"
                "✳️ Simply send the post link of a public channel. For private channels, do /login. Send /help to know more."
            ),
            reply_markup=keyboard
        )
        return  
        
    param = message.command[1] if len(message.command) > 1 else None
    freecheck = await chk_user(message, user_id)
    if freecheck != 1:
        await message.reply("You are a premium user no need of token 😉")
        return

    # Handle deep link with parameter
    if param:
        if user_id in Param and Param[user_id] == param:
            # Add user to MongoDB as a verified user for the next 6 hours
            await token.insert_one({
                "user_id": user_id,
                "param": param,
                "created_at": datetime.utcnow(),
                "expires_at": datetime.utcnow() + timedelta(hours=3),
            })
            del Param[user_id]  # Remove the parameter from Param
            await message.reply("✅ You have been verified successfully! Enjoy your session for next 3 hours.")
            return
        else:
            await message.reply("❌ Invalid or expired verification link. Please generate a new token.")
            return

@app.on_message(filters.command("token"))
async def smart_handler(client, message):
    user_id = message.chat.id
    # Check if the user is already verified or premium
    freecheck = await chk_user(message, user_id)
    if freecheck != 1:
        await message.reply("You are a premium user no need of token 😉")
        return
    if await is_user_verified(user_id):
        await message.reply("✅ Your free session is already active enjoy!")
    else:
        # Generate a session and send the link
        param = await generate_random_param()
        Param[user_id] = param  # Store the parameter in Param dictionary

        # Create a deep link
        deep_link = f"https://t.me/{client.me.username}?start={param}"

        # Get shortened URL
        shortened_url = await get_shortened_url(deep_link)
        if not shortened_url:
            await message.reply("❌ Failed to generate the token link. Please try again.")
            return

        # Create a button with the shortened link
        button = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Verify the token now...", url=shortened_url)]]
        )
        await message.reply("Click the button below to verify your free access token: \n\n> What will you get ? \n1. No time bound upto 3 hours \n2. Batch command limit will be FreeLimit + 20 \n3. All functions unlocked", reply_markup=button)
from crushe import app
from crushe.core.func import *
