import os
import json


def parse_hangouts_data(user, data_path='.'):
    """
    Mines a user's Hangouts messages. While it is possible to mine the user's
    (or, the people the user is speaking to) data selectively, we do not
    do that distinction here.

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} user messages
    """
    # Does the directory exist?
    path = f'{data_path}/{user}/Takeout/Hangouts/Hangouts.json'
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = json.load(f)

    # The conversation key only has metadata, skip it.
    conversations = data['conversations']['events']
    messages = []

    for conversation in conversations:
        content = conversation['chat_message']['message_content']
        segments = content['segment']
        cur_text = ''

        # Mine the text segments
        for segment in segments:
            if segment['type'] == 'TEXT':
                cur_text += segment['text'] + '\n'

        # Remove the trailing \n.
        cur_text = cur_text[:-1]
        messages.append(cur_text)

    # Return the messages.
    return messages
