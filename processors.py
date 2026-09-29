import re

def remove_usernames(text):
    if not text:
        return ""

    return re.sub(r'@[A-Za-z0-9_]+', '', text)


def add_footer(text, footer):
    if not text:
        return footer

    return text.rstrip() + "\n\n" + footer

# CHANNEL ONE
Footer_channel_one = """
ــــــــــــــــــــــــــــــ
برای اطلاعات بیشتر با ما در تماس باشید.
""".strip()

def process_channel_one(text, footer):
    if not text:
        return ""

    text = remove_usernames(text)
    text = add_footer(text, footer)

    return text

# CHANNEL TWO
Footer_channel_two = """
ــــــــــــــــــــــــــــــ
ما را در تلگرام دنبال کنید
@amoozesh_channel
""".strip()

def process_channel_two(text, footer):
    if not text:
        return ""

    text = remove_usernames(text)
    text = add_footer(text, footer)

    return text

# CHANNEL THREE
Footer_channel_three = """
ــــــــــــــــــــــــــــــ
#شترموتور_اخبار
""".strip()

def process_channel_three(text, footer):
    if not text:
        return ""

    # Removing the last line of post (The specific post format on this channel)
    text = re.sub(
        r'(?m)^\s*@\w+\s*\|\s*[^\n]+\s*$',
        '',
        text
    )
    text = add_footer(text, footer)

    return text


PROCESSORS = {
    "channel_one": process_channel_one,
    "channel_two": process_channel_two,
    "channel_three": process_channel_three,
}

FOOTERS = {
    "Footer_channel_one": Footer_channel_one,
    "Footer_channel_two": Footer_channel_two,
    "Footer_channel_three": Footer_channel_three,
}