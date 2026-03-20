import asyncio
import os
import sys

# Python 3.12+ loop fix
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

from pyrogram import Client, enums

# Heroku Settings
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
session_string = os.environ.get("SESSION_STRING")

my_message = """🎁 We’ve Launched Our New Bot! 🎁

Experience smoother, faster, and easier service with our brand-new bot. Whether you’re buying OTPs or readymade accounts – everything is now more seamless than ever! ✔️

📞 Support: @DevilComingSoon 🌟
✈️ Bot Link: @OTP_WANTED_ROBOT❤️"""

async def start_bot():
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
            try:
                async for dialog in app.get_dialogs():
                    if dialog.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
                        try:
                            await app.send_message(dialog.chat.id, my_message)
                            print(f"Sent to: {dialog.chat.title}")
                            await asyncio.sleep(5) 
                        except Exception as e:
                            print(f"Error: {e}")
                
                print("Round done. Waiting 10 mins...")
                await asyncio.sleep(600)
            except Exception as e:
                print(f"Loop Error: {e}")
                await asyncio.sleep(30)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())
