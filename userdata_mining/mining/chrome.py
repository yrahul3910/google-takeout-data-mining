import json
import os
import googlemaps
import ast

from userdata_mining.utils import get_key, warn
from userdata_mining.mining import get_nearby_places


def parse_autofill(user, data_path='.'):
    """
    Parses the user's autofill data.

    :param {str} user - The user directory.
    :return {list} A list of places nearby
    """
    # Check for a cache
    if os.path.exists('caches/.autofill.cache'):
        with open('caches/.autofill.cache', 'r') as f:
            # Safe evaluation with ast
            result = ast.literal_eval(f.readline())

            # Additional sanitary check
            assert isinstance(result, list)
            return result

    path = f'{data_path}/data/{user}/Takeout/Chrome/Autofill.json'
    if not os.path.exists(path):
        warn('Path the Chrome autofill data does not exist.')
        return []

    with open(path, 'r') as f:
        profile = json.load(f)

    profile = profile['Autofill Profile']

    # Is the list of profiles empty?
    if len(profile) == 0:
        return []

    addresses = [p['address_home_street_address'] for p in profile]

    # Geocode the addresses
    client = googlemaps.Client(key=get_key())
    places = []
    for address in addresses:
        coords = client.geocode(address=address)
        coords = list(coords[0]['geometry']['location'].values())
        places.extend(get_nearby_places(coords))

    # Save to cache
    with open('caches/.autofill.cache', 'w') as f:
        f.write(str(places))

    return places


def parse_browser_history(user, data_path='.'):
    """
    Parses the user's browser history.

    :param {str} user - The user name.
    :return {list} A list of page titles.
    """
    path = f'{data_path}/data/{user}/Takeout/Chrome/BrowserHistory.json'
    if not os.path.exists(path):
        warn('BrowserHistory.json does not exist.')
        return []

    with open(path, 'r') as f:
        profile = json.load(f)

    profile = profile['Browser History']

    # Is the history empty?
    if len(profile) == 0:
        return []

    return list(map(lambda p: p['title'], profile))
