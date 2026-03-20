import asyncio
import os
from pyrogram import Client, enums

# Heroku Settings (Config Vars-la irundhu edukum)
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
session_string = os.environ.get("SESSION_STRING")

# Unga Message
my_message = """🎁 We’ve Launched Our New Bot! 🎁

Experience smoother, faster, and easier service with our brand-new bot. Whether you’re buying OTPs or readymade accounts – everything is now more seamless than ever! ✔️

📞 Support: @DevilComingSoon 🌟
✈️ Bot Link: @OTP_WANTED_ROBOT❤️"""

app = Client("my_account_all", api_id=api_id, api_hash=api_hash, session_string=session_string)

async def main():
    async with app:
        print("UserBot Start aydichu! Ella group-kum msg poga poren...")
        
        while True:
            # Unga account-la irukura ella chats-ayum edukum
            async for dialog in app.get_dialogs():
                # Group or Supergroup matum filter pannum
                if dialog.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
                    try:
                        await app.send_message(dialog.chat.id, my_message)
                        print(f"Sent to: {dialog.chat.title}")
                        
                        # Account safety-kaga 5 seconds gap
                        await asyncio.sleep(5) 
                        
                    except Exception as e:
                        # Permission illadha group-ah irundha skip pannum
                        print(f"Skipping {dialog.chat.title}: {e}")
            
            print("Ellaa group-kum msg anupiyaachu! Next round 10 mins kazhichi...")
            # 600 seconds = 10 minutes wait
            await asyncio.sleep(600) 

app.run(main())

