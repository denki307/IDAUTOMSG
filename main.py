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
        # Start Notification to Log Channel
        try:
            await app.send_message(LOG_CHANNEL, "🚀 **UserBot Started!**\n\n✅ **Safety Mode:** Active\n📦 **Batch Size:** 50 Groups\n⏳ **Delay:** 30-60s per msg")
        except Exception as e:
            print(f"Log Channel Error: {e}")

        while True:
            # 1. Collect all groups from your ID
            all_groups = []
            async for dialog in app.get_dialogs():
                if dialog.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
                    all_groups.append(dialog)

            # 2. Shuffle groups to avoid same pattern (Account Safety)
            random.shuffle(all_groups)
            total_groups = len(all_groups)
            success_count = 0
            failed_count = 0

            # 3. Process in Batches of 50
            for i in range(0, total_groups, 50):
                batch = all_groups[i : i + 50]
                current_batch_num = (i // 50) + 1
                
                await app.send_message(
                    LOG_CHANNEL, 
                    f"📦 **Starting Batch {current_batch_num}**\nSending to groups {i+1} to {min(i+50, total_groups)}..."
                )

                for group in batch:
                    try:
                        # Send the message
                        await app.send_message(group.chat.id, MY_MESSAGE)
                        success_count += 1
                        
                        # Log success to channel
                        await app.send_message(LOG_CHANNEL, f"✅ **Success:** `{group.chat.title}`")
                        
                        # Random Delay between 30 to 60 seconds
                        wait_time = random.randint(5, 10)
                        await asyncio.sleep(wait_time)

                    except Exception as e:
                        failed_count += 1
                        print(f"Failed in {group.chat.title}: {e}")
                        # Short gap if error occurs
                        await asyncio.sleep(5)

                # 4. Break after each batch of 50
                if i + 50 < total_groups:
                    await app.send_message(LOG_CHANNEL, "⏳ **Batch Completed.** Taking a 5-minute break to stay safe...")
                    await asyncio.sleep(300) # 5 minutes break

            # 5. Round Summary
            summary = (
                f"📊 **Full Round Completed!**\n\n"
                f"✅ Total Success: {success_count}\n"
                f"❌ Total Failed: {failed_count}\n"
                f"👥 Total Groups Scanned: {total_groups}\n\n"
                f"Next round starts in 10 minutes..."
            )
            await app.send_message(LOG_CHANNEL, summary)
            
            # Wait 10 mins before starting from the first group again
            await asyncio.sleep(600)

if __name__ == "__main__":
    # Modern Python Async Loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())
