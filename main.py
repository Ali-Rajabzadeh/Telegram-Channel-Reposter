from datetime import datetime, time
from zoneinfo import ZoneInfo
import re
from telethon import TelegramClient


from config import (
    API_ID,
    API_HASH,
    SOURCE_CHANNEL,
    DESTINATION_CHANNEL,
)


# -----------------------------
# Telegram Client
# -----------------------------

client = TelegramClient(
    "sessions/user_session",
    API_ID,
    API_HASH,
)


# -----------------------------
# Text Processing
# -----------------------------

def remove_usernames(text):
    if not text:
        return ""

    # Delete usernames with @
    text = re.sub(r'@[A-Za-z0-9_]+', '', text)

    return text

FOOTER = """
ــــــــــــــــــــــــــــــ
برای اطلاعات بیشتر با ما در تماس باشید.
"""

def add_footer(text):
    if not text:
        return FOOTER.strip()

    return text.rstrip() + "\n\n" + FOOTER.strip()

def process_text(text):

    if not text:
        return ""

    text = remove_usernames(text)
    text = add_footer(text)

    return text

# -----------------------------
# Main
# -----------------------------

async def main():

    print("Connecting to Telegram...")

    # Get information account
    me = await client.get_me()

    print(f"Logged in as: {me.first_name}")
    print(f"Username: @{me.username}")

    # Channels
    source = await client.get_entity(SOURCE_CHANNEL)
    destination = await client.get_entity(DESTINATION_CHANNEL)

    print(f"Source: {source.title}")
    print(f"Destination: {destination.title}")

    # -----------------------------
    # Today's date
    # -----------------------------

    timezone = ZoneInfo("Asia/Tehran")

    now = datetime.now(timezone)

    start_of_day = datetime.combine(
        now.date(),
        time.min,
        tzinfo=timezone,
    )

    end_of_day = datetime.combine(
        now.date(),
        time.max,
        tzinfo=timezone,
    )

    print(
        f"Reading messages from: "
        f"{start_of_day} → {end_of_day}"
    )

    # -----------------------------
    # Get today's messages
    # -----------------------------

    messages = []

    async for message in client.iter_messages(source):

        # Converting Telegram message timestamps to Tehran time zone
        message_date = message.date.astimezone(timezone)

        if message_date < start_of_day:
            break

        if message_date <= end_of_day:
            messages.append(message)

    # -----------------------------
    # Process messages
    # -----------------------------

    for message in messages:

        print(f"Processing message {message.id}")

        # -------------------------
        # Text only
        # -------------------------

        if message.text and not message.media:

            new_text = process_text(
                message.text
            )

            await client.send_message(
                destination,
                new_text,
            )

        # -------------------------
        # Photo / Video / File
        # -------------------------

        elif message.media:

            new_caption = process_text(
                message.text or ""
            )

            try:
                await client.send_file(
                    destination,
                    message.media,
                    caption=new_caption,
                )

            except Exception as e:
                print(
                    f"Skipped message {message.id}: {e}"
                )
                continue

        # -------------------------
        # Other messages
        # -------------------------

        else:

            print(
                f"Skipped message {message.id}"
            )

    print("Done.")


# -----------------------------
# Run
# -----------------------------

with client:
    client.loop.run_until_complete(main())