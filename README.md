# Telegram Channel Reposter

A lightweight Python tool for collecting posts from multiple Telegram channels, processing their text and captions, and reposting them to configured destination channels.

The project uses a **personal Telegram account through Telethon** instead of the Telegram Bot API. This allows the account to read and repost content from channels that the account has access to, without requiring the source channel to add a bot as an administrator.

## Features

* Monitor multiple Telegram source channels
* Configure a different destination channel for each source
* Configure a different text processor for each source channel
* Configure a different footer for each source channel
* Process both text messages and media captions
* Repost:

  * Text messages
  * Images
  * Videos
  * Other media supported by Telethon
* Processing messages tailored to the structure of each channel
* Add custom footers to processed posts
* Process only messages published during the current day
* Process messages in chronological order
* Use public usernames or private Telegram channel IDs
* Continue processing if an individual message cannot be reposted
* Run once and exit instead of continuously monitoring channels

---

## How It Works

The application follows this workflow:

```text
                    Telegram
                       │
          ┌────────────┴────────────┐
          │                         │
          ▼                         ▼
   Source Channel 1         Source Channel 2
          │                         │
          ▼                         ▼
     Processor 1               Processor 2
          │                         │
          └────────────┬────────────┘
                       │
                       ▼
                Processed Content
                       │
             ┌─────────┴─────────┐
             │                   │
             ▼                   ▼
       Destination 1       Destination 2
```

Each source channel can have its own configuration:

```text
Source Channel
      │
      ├── Destination
      ├── Processor
      └── Footer
```

This makes it possible to handle different source channels differently without changing the main application logic.

---

## Requirements

* Python 3.10+
* A Telegram account
* Access to the source channels
* Permission to post in the destination channels
* Telegram `API_ID`
* Telegram `API_HASH`

---

## Installation

Clone the repository and install the required dependencies:

```bash
python -m pip install telethon tzdata
```

---

## Getting Telegram API Credentials

Telegram API credentials can be obtained from:

https://my.telegram.org/auth

Sign in using the Telegram account that will be used by Telethon.

Create an application and obtain:

```text
API ID
API Hash
```

These credentials are required to create the Telethon client.

---

## Configuration

Create a `config.py` file.

A basic configuration looks like this:

```python
API_ID = 12345678
API_HASH = "YOUR_API_HASH"


SOURCE_CHANNELS = {
    "@channel_one": {
        "destination": "@destination_channel_one",
        "processor": "channel_one",
        "footer": "Footer_channel_one",
    },

    "@channel_two": {
        "destination": "@destination_channel_two",
        "processor": "channel_two",
        "footer": "Footer_channel_two",
    },

    "@channel_three": {
        "destination": "@destination_channel_three",
        "processor": "channel_three",
        "footer": "Footer_channel_three",
    },
}
```

The application processes each source channel independently.

## Private Channels

Private Telegram channels usually do not have a public username.

In this case, use the Telegram channel ID:

```python
SOURCE_CHANNELS = {
    -1001234567890: {
        "destination": -1009876543210,
        "processor": "channel_one",
        "footer": "Footer_channel_one",
    },
}
```

Telegram channel IDs normally look like:

```text
-1001234567890
```

The Telegram account used by Telethon must have access to the source channel and permission to post in the destination channel.

---

## Text Processing

Text processing is handled separately from the main application.

Processors are defined in:

```text
processors.py
```
Processors are registered in:

```python
PROCESSORS = {
    "channel_one": process_channel_one,
    "channel_two": process_channel_two,
    "channel_three": process_channel_three,
}
```

This allows each source channel to have its own processing logic.

---


## Custom Footers

Each source channel can have its own footer.

Footers are registered in:

```python
FOOTERS = {
    "Footer_channel_one": Footer_channel_one,
    "Footer_channel_two": Footer_channel_two,
    "Footer_channel_three": Footer_channel_three,
}
```

The configuration determines which footer is used for each source channel:

---

## Project Structure

```text
telegram-channel-reposter/
│
├── main.py
├── config.py
├── processors.py
├── README.md
│
└── sessions/
    └── user_session.session
```

### `main.py`

Contains the main Telegram client and the message processing workflow.

### `config.py`

Contains:

* Telegram API credentials
* Source channels
* Destination channels
* Processor configuration
* Footer configuration

### `processors.py`

Contains:

* Text processing functions
* Username removal
* Source-line removal
* Footer definitions
* Processor mappings

### `sessions/`

Contains the Telethon session file created after authentication.

The session allows future executions to reuse the authenticated Telegram account without logging in again.

---

## Running the Project

Run:

```bash
python main.py
```

On the first run, Telethon will ask for the Telegram account phone number and verification code.

For example:

```text
Please enter your phone:
```

Enter the phone number using international format:

```text
+98912******7
```

After successful authentication, Telethon creates a session file inside:

```text
sessions/
```

Future executions can reuse this session.

---

## Daily Processing

The application does not continuously monitor Telegram channels.

Each time the application is executed, it:

1. Connects to Telegram.
2. Identifies the current date.
3. Checks every configured source channel.
4. Retrieves messages published during the current day.
5. Processes each message using the configured processor.
6. Adds the configured footer.
7. Sends the processed message or media to the configured destination.
8. Continues if an individual message fails.
9. Exits after all configured channels have been processed.

---

## Media Handling

The application can repost Telegram media together with its processed caption.

Supported media can include:

* Images
* Videos
* Documents
* Other media supported by Telethon

For example:

```text
Source message
      │
      ▼
   Image
      +
   Caption
      │
      ▼
Process caption
      │
      ▼
Add footer
      │
      ▼
Destination channel
```

If a media caption exceeds Telegram's allowed caption length, the message may be skipped rather than stopping the entire process.

---

## Error Handling

Individual message errors do not necessarily stop the entire application.

For example:

```text
Processing channel: @channel_one

Message 101  ✓
Message 102  ✓
Message 103  Skipped
Message 104  ✓
Message 105  ✓

Processing channel: @channel_two

Message 201  ✓
Message 202  ✓
```

This allows the application to continue processing other messages and channels when an individual post cannot be reposted.

---

## Security

Do not commit sensitive Telegram credentials or session files to GitHub.

The following should not be uploaded to a public repository:

```text
API_HASH
*.session
config.py
```

For production or public repositories, sensitive configuration should preferably be stored using environment variables or another secure configuration mechanism.

---

## Important Telegram Considerations

The application uses a personal Telegram account through Telethon.

Therefore:

* The account must have access to the source channels.
* The account must have permission to post in destination channels.
* Private channels can be accessed using their Telegram IDs when the account has access.
* The Telethon session file should be treated as sensitive because it represents an authenticated Telegram session.

---

## Disclaimer

This project is intended for channels and content that you are authorized to access and repost.

Make sure your use of the tool complies with:

* Telegram's terms and policies
* The rules of the source channels
* Copyright requirements
* Applicable content-sharing laws and regulations
