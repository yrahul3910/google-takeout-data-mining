import os
import json
import ast
from userdata_mining.mining import get_nearby_places


def parse_maps(user, data_path='.'):
    """
    Maps(your places) data mining

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} user messages
    """
    # Check for a cache
    if os.path.exists(f'{data_path}/caches/.maps_places.cache'):
        f = open(f'{data_path}/caches/.maps_places.cache', 'r')
        return ast.literal_eval(f.readline())

    # Does the directory exist?
    path = f'{data_path}/data/{user}/Reviews.json'
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = json.load(f)

    features = data['features']
    coordinates = [x['geometry']['coordinates'][::-1]
                   for x in data['features']]

    places = []
    for coords in coordinates:
        places.extend(get_nearby_places(coords))

    # Cache results
    with open(f'{data_path}/caches/.maps_places.cache', 'w') as f:
        f.write(str(places))

    return places
