import os
import json

def parse_maps(user, data_path='.'):
    """
    Maps(your places) data mining

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} user messages
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/Reviews.json'
    print(path)
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = json.load(f)

    features = data['features']
    coordinates = [x['geometry']['coordinates'][::-1] for x in data['features']]
    return coordinates
