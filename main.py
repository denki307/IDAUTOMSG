import asyncio
import os
from pyrogram import Client, enums

# Heroku Settings
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
session_string = os.environ.get("SESSION_STRING")
log_channel = int(os.environ.get("-1003735021874"))

my_message = os.environ.get("MY_MESSAGE")

app = Client(
    "my_account", 
    api_id=api_id, 
    api_hash=api_hash, 
    session_string=session_string,
    in_memory=True
)

async def start_bot():
    async with app:
        # Bot start aagum podhu log
        await app.send_message(log_channel, "🚀 **UserBot Started!**\nAuto-messaging is now active.")
        
        while True:
            success_count = 0
            failed_count = 0
            
            async for dialog in app.get_dialogs():
                if dialog.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
                    group_name = dialog.chat.title
                    try:
                        await app.send_message(dialog.chat.id, my_message)
                        success_count += 1
                        
                        # Ovvoru group success aagum podhum log anupum
                        await app.send_message(
                            log_channel, 
                            f"✅ **Success:** Message sent to `{group_name}`"
                        )
                        
                        # Flood safety-ku 5 seconds gap (Idhu kandaipa venum)
                        await asyncio.sleep(5) 
                        
                    except Exception as e:
                        failed_count += 1
                        # Failed aana log
                        await app.send_message(
                            log_channel, 
                            f"❌ **Failed:** `{group_name}`\n**Error:** `{e}`"
                        )
                        await asyncio.sleep(2) # Error vandha chinna gap
            
            # Final Report for the round
            report = (
                f"📊 **Current Round Completed**\n\n"
                f"✅ Total Success: {success_count}\n"
                f"❌ Total Failed: {failed_count}\n\n"
                f"Next round starts in 10 minutes..."
            )
            await app.send_message(log_channel, report)
            
            # 10 minutes wait
            await asyncio.sleep(600)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())
