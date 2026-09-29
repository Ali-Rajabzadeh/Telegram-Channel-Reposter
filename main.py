from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from telethon import TelegramClient

from config import API_ID, API_HASH, SOURCE_CHANNELS
from processors import PROCESSORS, FOOTERS

# ============================================================
# Session

Path("sessions").mkdir(exist_ok=True)

client = TelegramClient(
    "sessions/user_session",
    API_ID,
    API_HASH,
)

# ============================================================
# Get date and time range from user

def get_datetime_range(timezone):

    while True:
        print()
        print("=" * 60)
        print("Enter the date and time range")
        print("=" * 60)

        start_date = input(
            "Start date (YYYY-MM-DD): "
        ).strip()

        start_time = input(
            "Start time (HH:MM): "
        ).strip()

        end_date = input(
            "End date (YYYY-MM-DD): "
        ).strip()

        end_time = input(
            "End time (HH:MM): "
        ).strip()

        try:
            start_datetime = datetime.strptime(
                f"{start_date} {start_time}",
                "%Y-%m-%d %H:%M",
            ).replace(tzinfo=timezone)

            end_datetime = datetime.strptime(
                f"{end_date} {end_time}",
                "%Y-%m-%d %H:%M",
            ).replace(tzinfo=timezone)

        except ValueError:
            print()
            print("Invalid date or time format.")
            print("Date format: YYYY-MM-DD")
            print("Time format: HH:MM")
            continue

        if start_datetime >= end_datetime:
            print()
            print(
                "Start datetime must be earlier "
                "than end datetime."
            )
            continue

        return start_datetime, end_datetime

# ============================================================
# Process one source channel

async def process_source_channel(
    source_name,
    destination_name,
    processor_name,
    footer,
    start_datetime,
    end_datetime,
    timezone,
):

    print(f"\n{'=' * 60}")
    print(f"Source: {source_name}")
    print(f"Processor: {processor_name}")
    print(f"{'=' * 60}")

    # --------------------------------------------------------
    # Get processor

    processor = PROCESSORS.get(processor_name)
    if processor is None:
        print(f"Processor not found: {processor_name}")
        return

    # --------------------------------------------------------
    # Get Telegram entities

    try:
        source = await client.get_entity(source_name)

        destination = await client.get_entity(destination_name)

    except Exception as e:
        print(f"Could not resolve channel: {e}")
        return

    # --------------------------------------------------------
    # Get messages inside requested date/time range

    messages = []

    async for message in client.iter_messages(source):
        message_datetime = (message.date.astimezone(timezone))

        # Older than requested range
        if message_datetime < start_datetime:
            break

        # Inside requested range
        if message_datetime <= end_datetime:

            messages.append(message)

    # --------------------------------------------------------
    # Process messages in chronological order

    messages.reverse()
    print(f"Found {len(messages)} messages.")

    for message in messages:
        try:
            # =================================================
            # Text

            if message.text and not message.media:
                new_text = processor(
                    message.text,
                    footer,
                )

                if new_text:
                    await client.send_message(
                        destination,
                        new_text,
                    )
                    print(f"Sent text message: {message.id}")

            # =================================================
            # Media

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
                        f"Skipped message "
                        f"{message.id}: {e}"
                    )
                    continue

        except Exception as e:
            print(
                f"Error processing message "
                f"{message.id}: {e}"
            )
            continue

# ============================================================
# Main

async def main():

    timezone = ZoneInfo("Asia/Tehran")

    # --------------------------------------------------------
    # Get date/time range from terminal

    start_datetime, end_datetime = (
        get_datetime_range(timezone)
    )

    print()
    print("=" * 60)
    print("Selected date/time range")
    print("=" * 60)
    print(f"Start: {start_datetime}")
    print(f"End:   {end_datetime}")
    print(f"Channels: {len(SOURCE_CHANNELS)}")
    print("=" * 60)

    # --------------------------------------------------------
    # Process all source channels

    for source_name, settings in SOURCE_CHANNELS.items():
        destination_name = settings["destination"]
        processor_name = settings["processor"]
        footer_name = settings["footer"]
        footer = FOOTERS.get(footer_name)
        if footer is None:
            print(f"Footer not found: {footer_name}")
            continue

        await process_source_channel(
            source_name=source_name,
            destination_name=destination_name,
            processor_name=processor_name,
            footer=footer,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            timezone=timezone,
        )

# ============================================================
# Run

with client:
    client.loop.run_until_complete(main())