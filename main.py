import asyncio
import os
import random
import sys
from pyrogram import Client, enums

# --- Heroku Settings ---
try:
    API_ID = int(os.environ.get("API_ID"))
    API_HASH = os.environ.get("API_HASH")
    SESSION_STRING = os.environ.get("SESSION_STRING")
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL"))
    MY_MESSAGE = os.environ.get("MY_MESSAGE")
except Exception as e:
    print(f"❌ Config Vars Error: {e}")
    sys.exit(1)

app = Client(
    "my_account", 
    api_id=API_ID, 
    api_hash=API_HASH, 
    session_string=SESSION_STRING,
    in_memory=True
)

async def start_bot():
    async with app:
        try:
            await app.send_message(LOG_CHANNEL, "🚀 **UserBot Started!**\n\n✅ **Safety Mode:** Active\n📦 **Batch Size:** 50 Groups\n⏳ **Round Interval:** 30 Minutes")
        except Exception as e:
            print(f"Log Channel Error: {e}")

        while True:
            all_groups = []
            async for dialog in app.get_dialogs():
                if dialog.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
                    all_groups.append(dialog)

            random.shuffle(all_groups)
            total_groups = len(all_groups)
            success_count = 0
            failed_count = 0

            for i in range(0, total_groups, 50):
                batch = all_groups[i : i + 50]
                current_batch_num = (i // 50) + 1
                
                await app.send_message(
                    LOG_CHANNEL, 
                    f"📦 **Starting Batch {current_batch_num}**\nSending to groups {i+1} to {min(i+50, total_groups)}..."
                )

                for group in batch:
                    try:
                        await app.send_message(group.chat.id, MY_MESSAGE)
                        success_count += 1
                        await app.send_message(LOG_CHANNEL, f"✅ **Success:** `{group.chat.title}`")
                        
                        # Ovvoru msg-kum naduvula 5 to 10s gap (neenga code-la irundhadhu)
                        wait_time = random.randint(5, 10)
                        await asyncio.sleep(wait_time)

                    except Exception as e:
                        failed_count += 1
                        print(f"Failed in {group.chat.title}: {e}")
                        await asyncio.sleep(5)

                if i + 50 < total_groups:
                    await app.send_message(LOG_CHANNEL, "⏳ **Batch Completed.** Taking a 5-minute break...")
                    await asyncio.sleep(300) 

            # --- ROUND SUMMARY WITH 30 MINS WAIT ---
            summary = (
                f"📊 **Full Round Completed!**\n\n"
                f"✅ Total Success: {success_count}\n"
                f"❌ Total Failed: {failed_count}\n"
                f"👥 Total Groups: {total_groups}\n\n"
                f"💤 **Next round starts in 30 minutes...**"
            )
            await app.send_message(LOG_CHANNEL, summary)
            
            # 1800 seconds = 30 minutes
            await asyncio.sleep(1800) 

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())
