import os
import json


def parse_tv_data(user, data_path='.'):
    """
    Mines a user's  TV shows.

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} user messages
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/TV App Favorites and Activity.json'
    print(path)
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = json.load(f)

    # The conversation key only has metadata, skip it.
    shows = data['events']

    tvShows = [p['event_interpretation']
               ['human_readable_media_description'] for p in shows]
    return tvShows
