from pathlib import Path
from datetime import datetime, time
from zoneinfo import ZoneInfo

from telethon import TelegramClient

from config import API_ID, API_HASH, SOURCE_CHANNELS
from processors import PROCESSORS, FOOTERS


# ============================================================
# Session
# ============================================================

Path("sessions").mkdir(exist_ok=True)

client = TelegramClient(
    "sessions/user_session",
    API_ID,
    API_HASH,
)


# ============================================================
# Process one source channel
# ============================================================

async def process_source_channel(
    source_name,
    destination_name,
    processor_name,
    footer,
    start_of_day,
    end_of_day,
    timezone,
):
    print(f"\n{'=' * 60}")
    print(f"Source: {source_name}")
    print(f"Processor: {processor_name}")
    print(f"{'=' * 60}")

    # --------------------------------------------------------
    # Get processor
    # --------------------------------------------------------

    processor = PROCESSORS.get(processor_name)

    if processor is None:
        print(f"Processor not found: {processor_name}")
        return

    # --------------------------------------------------------
    # Get Telegram entities
    # --------------------------------------------------------

    try:
        source = await client.get_entity(source_name)
        destination = await client.get_entity(destination_name)

    except Exception as e:
        print(f"Could not resolve channel: {e}")
        return

    # --------------------------------------------------------
    # Get today's messages
    # --------------------------------------------------------

    messages = []

    async for message in client.iter_messages(source):

        message_date = message.date.astimezone(timezone)

        # Older than today
        if message_date < start_of_day:
            break

        # Today's message
        if message_date <= end_of_day:
            messages.append(message)

    # --------------------------------------------------------
    # Process messages in chronological order
    # --------------------------------------------------------

    messages.reverse()

    print(f"Found {len(messages)} messages.")

    for message in messages:

        try:

            # =================================================
            # Text
            # =================================================

            if message.text and not message.media:

                new_text = processor(message.text, footer)

                if new_text:
                    await client.send_message(
                        destination,
                        new_text,
                    )

                    print(f"Sent text message: {message.id}")

            # =================================================
            # Media
            # =================================================

            elif message.media:

                new_caption = processor(
                    message.text or "",
                    footer,
                )

                try:

                    await client.send_file(
                        destination,
                        message.media,
                        caption=new_caption,
                    )

                    print(f"Sent media message: {message.id}")

                except Exception as e:

                    print(
                        f"Skipped message {message.id}: {e}"
                    )

                    continue

        except Exception as e:

            print(
                f"Error processing message {message.id}: {e}"
            )

            continue


# ============================================================
# Main
# ============================================================

async def main():

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

    print(f"Today: {now.date()}")
    print(f"Channels: {len(SOURCE_CHANNELS)}")

    # --------------------------------------------------------
    # Process all source channels
    # --------------------------------------------------------

    for source_name, settings in SOURCE_CHANNELS.items():

        destination_name = settings["destination"]
        processor_name = settings["processor"]
        footer_name = settings["footer"]

        footer = FOOTERS.get(footer_name, "")

        await process_source_channel(
            source_name=source_name,
            destination_name=destination_name,
            processor_name=processor_name,
            footer=footer,
            start_of_day=start_of_day,
            end_of_day=end_of_day,
            timezone=timezone,
        )


# ============================================================
# Run
# ============================================================

with client:

    client.loop.run_until_complete(main())