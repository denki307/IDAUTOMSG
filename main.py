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
    
    # LOG_CHANNEL-ah string-ah edukkom (ID or Username)
    LOG_INPUT = os.environ.get("LOG_CHANNEL")
    if LOG_INPUT.startswith("-100"):
        LOG_CHANNEL = int(LOG_INPUT)
    else:
        LOG_CHANNEL = LOG_INPUT  # Example: "MyLogChannel" or "@MyLogChannel"
        
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

async def safe_log(text):
    """Log channel-ku safe-ah message anuppum"""
    try:
        await app.send_message(LOG_CHANNEL, text)
    except Exception as e:
        print(f"⚠️ Log Failed: {e}")

async def start_bot():
    async with app:
        # Start notification
        await safe_log("🚀 **UserBot Started!**\n30-minute interval mode active.")

        while True:
            all_groups = []
            try:
                # Limit 300 dialogs to find groups
                async for dialog in app.get_dialogs(limit=300):
                    if dialog.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
                        all_groups.append(dialog)
            except Exception as e:
                print(f"⚠️ Error fetching groups: {e}")

            if not all_groups:
                print("❌ No groups found. Retrying in 5 mins...")
                await asyncio.sleep(300)
                continue

            random.shuffle(all_groups)
            total_groups = len(all_groups)
            success_count = 0
            failed_count = 0

            # Batch processing (50 groups)
            for i in range(0, total_groups, 50):
                batch = all_groups[i : i + 50]
                await safe_log(f"📦 **Starting Batch:** Groups {i+1} to {min(i+50, total_groups)}")

                for group in batch:
                    try:
                        await app.send_message(group.chat.id, MY_MESSAGE)
                        success_count += 1
                        
                        # Log success
                        await safe_log(f"✅ **Success:** `{group.chat.title}`")
                        
                        # 5 to 10s gap between messages
                        await asyncio.sleep(random.randint(5, 10))
                    except Exception as e:
                        failed_count += 1
                        print(f"Failed in {group.chat.title}: {e}")
                        await asyncio.sleep(3)

                # 5-minute break after each batch of 50
                if i + 50 < total_groups:
                    await safe_log("⏳ **Batch Done.** 5-minute break...")
                    await asyncio.sleep(300)

            # Round summary
            await safe_log(f"📊 **Round Done!**\n✅ Success: {success_count}\n❌ Failed: {failed_count}\n💤 Next round in 30 mins.")
            
            # Wait 30 minutes for the next full round
            await asyncio.sleep(1800)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())
