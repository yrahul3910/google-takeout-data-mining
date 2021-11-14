import json
import os
from userdata_mining.utils import warn


def parse_play_data(user, library_type, data_path='.'):
    """
    Parse the Google Play app data of the user.

    Args:
        user (str): The user to parse.
        library_type (str): Type of data to parse - apps or movies
        data_path (str): The path to the data.

    Returns:
        list: A list of apps downloaded.
    """
    # First, check for cache
    if os.path.exists(f'{data_path}/saved/embeddings/play.pickle'):
        return None

    path = f'{data_path}/data/{user}/Takeout/Google Play Store/Library.json'

    # Does the directory exist?
    if not os.path.exists(path):
        warn('Google Play Library data path does not exist.')
        return []

    f = open(path, 'r')
    data = json.load(f)

    if library_type.lower() == 'apps':
        data_type = 'Android Apps'
    elif library_type.lower() == 'movies':
        data_type = 'Movie'
    else:
        warn('Unsupported data type specified.')
        return []

    titles = []
    for x in data:
        doc = x['libraryDoc']['doc']
        if doc['documentType'] == data_type and doc['title'] != 'Unknown Item':
            title = doc['title']
            titles.append(str.split(doc['title'], '.')[2]) if title.startswith('com.') else titles.append(title)

    f.close()

    return titles
