import asyncio
import os
from pyrogram import Client, enums

# Heroku Settings
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
session_string = os.environ.get("SESSION_STRING")

# Message Content
my_message = """🎁 We’ve Launched Our New Bot! 🎁

Experience smoother, faster, and easier service with our brand-new bot. Whether you’re buying OTPs or readymade accounts – everything is now more seamless than ever! ✔️

📞 Support: @DevilComingSoon 🌟
✈️ Bot Link: @OTP_WANTED_ROBOT❤️"""

async def start_bot():
    # Session string use panni Client initialize pandrom
    app = Client(
        "my_account", 
        api_id=api_id, 
        api_hash=api_hash, 
        session_string=session_string,
        in_memory=True
    )
    
    async with app:
        print("UserBot started successfully!")
        while True:
            async for dialog in app.get_dialogs():
                if dialog.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
                    try:
                        await app.send_message(dialog.chat.id, my_message)
                        print(f"Sent to: {dialog.chat.title}")
                        await asyncio.sleep(5) # Rate limit safety
                    except Exception as e:
                        print(f"Error in {dialog.chat.title}: {e}")
            
            print("Round finished. Waiting 10 minutes...")
            await asyncio.sleep(600)

if __name__ == "__main__":
    # Python 3.10+ and 3.14 safety loop
    try:
        asyncio.run(start_bot())
    except (KeyboardInterrupt, SystemExit):
        pass
