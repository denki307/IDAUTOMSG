import asyncio
import os
import sys
from pyrogram import Client, enums

# Heroku Settings
try:
    api_id = int(os.environ.get("API_ID"))
    api_hash = os.environ.get("API_HASH")
    session_string = os.environ.get("SESSION_STRING")
    # INGA DHAAN CHANGE: Empty-ah irundha "LOG_CHANNEL" nu mathiruken
    log_channel = int(os.environ.get("LOG_CHANNEL")) 
    my_message = os.environ.get("MY_MESSAGE")
except Exception as e:
    print(f"Config Vars-la edho mistake irukku: {e}")
    sys.exit(1)

app = Client(
    "my_account", 
    api_id=api_id, 
    api_hash=api_hash, 
    session_string=session_string,
    in_memory=True
)

async def start_bot():
    async with app:
        # Bot start aagum podhu log channel-ku msg anupum
        try:
            await app.send_message(log_channel, "🚀 **UserBot Started!**\nAuto-messaging is now active.")
        except Exception as e:
            print(f"Log Channel-ku msg anupa mudiyala: {e}")

        while True:
            success_count = 0
            failed_count = 0
            
            async for dialog in app.get_dialogs():
                # Chat type GROUP or SUPERGROUP-ah nu check pannum
                if dialog.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
                    group_name = dialog.chat.title
                    try:
                        # Unga group-ku msg anupum
                        await app.send_message(dialog.chat.id, my_message)
                        success_count += 1
                        
                        # Log channel-la success update podum
                        await app.send_message(
                            log_channel, 
                            f"✅ **Success:** Message sent to `{group_name}`"
                        )
                        await asyncio.sleep(5) # Flood safety
                        
                    except Exception as e:
                        failed_count += 1
                        # Failed aana log channel-la error update podum
                        try:
                            await app.send_message(
                                log_channel, 
                                f"❌ **Failed:** `{group_name}`\n**Error:** `{e}`"
                            )
                        except:
                            pass
                        await asyncio.sleep(2)
            
            # Round mudinja udane summary
            report = (
                f"📊 **Current Round Completed**\n\n"
                f"✅ Total Success: {success_count}\n"
                f"❌ Total Failed: {failed_count}\n\n"
                f"Next round starts in 10 minutes..."
            )
            await app.send_message(log_channel, report)
            await asyncio.sleep(600)

if __name__ == "__main__":
    # Python 3.10+ loop handling
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())
