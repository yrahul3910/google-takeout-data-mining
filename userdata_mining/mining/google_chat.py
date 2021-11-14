import glob
import json
import os
from userdata_mining.utils import warn



def parse_chats_data(user, data_path='.'):
    """
    Parse the chat data of a user.

    Args:
        user (str): The user to parse.
        data_path (str): The path to the data.

    Returns:
        list: A list of chats.
    """
    # First, check for cache
    if os.path.exists(f'{data_path}/saved/embeddings/chat.pickle'):
        return None

    path = f'{data_path}/data/{user}/Takeout/Google Chat/Groups'

    # Does the directory exist?
    if not os.path.exists(path):
        warn('Hangouts data path does not exist.')
        return []

    for file in glob.glob(f'{path}/**/messages.json'):
        with open(file, 'r') as f:
            data = json.load(f)
            messages = [x['text'] for x in data['messages'] if 'text' in x]

    return messages
