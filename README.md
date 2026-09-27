# Telegram Channel Reposter

A lightweight Python tool for automatically collecting the posts published on a Telegram channel during the current day, processing their text/captions, and reposting them to another Telegram channel.

The project uses a personal Telegram account through **Telethon**, so the source channel does not need to add a bot as an administrator. The account only needs to have access to the source channel.

## Features

* Read posts from a Telegram source channel
* Process text and captions before reposting
* Remove Telegram usernames such as `@username`
* Add a custom footer to posts
* Repost:

  * Text messages
  * Images
  * Videos
  * Other Telegram media supported by Telethon
* Only process messages published during the current day
* Use a personal Telegram account instead of the Telegram Bot API
* Skip messages that cannot be reposted instead of stopping the entire process

## How It Works

The application follows this workflow:

```text
Source Telegram Channel
          │
          ▼
       Telethon
          │
          ▼
   Today's Messages
          │
          ▼
     Text Processing
          │
          ├── Remove usernames
          ├── Modify text
          └── Add custom footer
          │
          ▼
 Destination Telegram Channel
```

## Requirements

* Python 3.10+
* A Telegram account
* Access to the source channel
* Permission to post in the destination channel
* Telegram `API_ID`
* Telegram `API_HASH`

## Installation

After cloning the repository, install the dependencies:

```bash
python -m pip install telethon tzdata
```

## Getting Telegram API Credentials

Go to:

https://my.telegram.org/auth

Sign in using the Telegram account that has access to the source channel.

Obtain:

```text
API ID
API Hash
```

## Configuration

Create a `config.py` file:

```python
API_ID = 12345678
API_HASH = "YOUR_API_HASH"

SOURCE_CHANNEL = "@source_channel"
DESTINATION_CHANNEL = "@destination_channel"
```

For private channels, you can use the channel ID:

```python
SOURCE_CHANNEL = -1001234567890
DESTINATION_CHANNEL = -1009876543210
```

## Project Structure

```text
telegram-channel-reposter/
│
├── main.py
├── config.py
├── README.md
│
└── sessions/
    └── user_session.session
```

The `sessions` directory contains the Telegram login session created by Telethon.

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

Enter the phone number using the international format:

```text
+98912****567
```

After successful authentication, Telethon creates a session file inside:

```text
sessions/
```

Future executions can reuse this session.

## Daily Processing

The application does not continuously monitor the source channel.

Every time the application is executed, it:

1. Connects to Telegram.
2. Identifies the current date.
3. Reads the messages published today.
4. Processes their text/captions.
5. Sends the processed posts to the destination channel.
6. Exits.


## Media Handling

The application can repost Telegram media together with its processed caption.

The same approach can be used for videos and other supported media.

## Error Handling

If a media message cannot be reposted, the application can skip that message and continue processing the remaining messages.

Example:

```text
Processing message 101
Processing message 102
Skipped message 103
Processing message 104
Processing message 105

Done.
```

This prevents a single problematic post from stopping the entire process.

## Security

Never commit sensitive Telegram credentials or session files.

Do not upload:

```text
API_HASH
*.session
config.py
```

to a public GitHub repository.

A safer production configuration is to use environment variables:

```text
API_ID
API_HASH
SOURCE_CHANNEL
DESTINATION_CHANNEL
```

## Disclaimer

This project is intended for channels and content that you are authorized to access and repost. Make sure your use of the tool complies with Telegram's terms, the source channel's rules, and applicable copyright and content-sharing requirements.