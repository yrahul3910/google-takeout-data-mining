import os
import json
import numpy as np


def parse_hangouts_data(user, data_path='.'):
    """
    Mines a user's Hangouts messages. While it is possible to mine the user's
    (or, the people the user is speaking to) data selectively, we do not
    do that distinction here. If cache exists, returns None.

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} user messages
    """
    # First, check for cache
    if os.path.exists(f'{data_path}/saved/embeddings/hangouts.pickle'):
        return None

    # Does the directory exist?
    path = f'{data_path}/data/{user}/Takeout/Hangouts/Hangouts.json'
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = json.load(f)

    # The conversation key only has metadata, skip it.
    conversations = [x['events'] for x in data['conversations']]
    messages = []

    for conversation in conversations:
        content = [x['chat_message']['message_content'].get('segment', [{'type': 'foo'}])
                   for x in conversation if 'chat_message' in x]
        segments = [[y['text'].encode('ascii', 'ignore').decode('ascii') for y in x if y['type'] == 'TEXT']
                    for x in content]
        segments = np.array(segments)

        if segments.shape[0] > 1:
            segments = segments.squeeze()
        messages.extend(segments)

    # Return the messages.
    return messages
