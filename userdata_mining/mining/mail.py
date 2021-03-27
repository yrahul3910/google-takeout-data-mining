import os
from bs4 import BeautifulSoup
from mailbox import mbox, Message


def parse_html_content(html):
    """
    Parses HTML content of a message.

    :param {str} html - The HTML content.
    :return {str} The text content
    """
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text()


def parse_single_message(message: Message):
    """
    Parses a single message that is not multipart. If
    the message is multipart, returns a list of the text segments.
    If non-textual message, returns None.

    :param {Message} message - The message to parse
    :return {str} The text content of the message.
    """
    if message.is_multipart():
        content = []
        for part in message:
            part_content = parse_single_message(part)

            # Add to our current list.
            if isinstance(part_content, list):
                content.extend(part_content)
            else:
                content.append(part_content)
        return content

    payload = message.get_payload(decode=True)
    content_type = message.get_content_type()

    if content_type == 'text/plain':
        return payload
    elif content_type == 'text/html':
        return parse_html_content(payload)
    else:
        return None


def parse_mail_data(user, data_path='.'):
    """
    Parses a user's email data in mbox format.

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, without the trailing /.
    :return {list} A list of messages
    """
    path = f'{data_path}/{user}/Takeout/Mail/All mail Including Spam.mbox'

    # Check if path exists
    if not os.path.exists(path):
        return []

    mailbox = mbox(path)
    messages = []
    for message in mailbox:
        message_content = parse_single_message(message)

        if message_content is None:
            continue
        if isinstance(message_content, str):
            messages.append(message_content)
        elif isinstance(message_content, list):
            messages.append(' '.join(message_content))

    return messages
