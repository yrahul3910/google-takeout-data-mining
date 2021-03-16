from utils import get_key
import os
import json
import googlemaps
import numpy as np


def get_maps_distance(coords):
    """
    Get distances between coordinates using Maps API.

    :param {list} *coords - Coordinates
    :return {float} Sum of distances.
    """
    api_key = get_key()
    client = googlemaps.Client(key=api_key)
    distances = client.distance_matrix(origins=coords, destinations=coords,
                                       units='metric')

    # Add up all the distances
    dist = list(map(
        lambda y: list(map(
            lambda x: x['distance']['value'],
                y['elements'])),
        distances['rows']))
    return np.sum(dist) / 2.


def get_nearby_places(coords):
    """
    Gets places near the coordinates passed.

    :param {list} coords - Coordinates
    :return {list} Places nearby.
    """
    api_key = get_key()
    client = googlemaps.Client(key=api_key)

    places = []
    maps_res = client.places_nearby(location=coords,
                                    radius=1000,
                                    max_price=2,
                                    open_now=True)

    token = maps_res.get('next_page_token', None)
    places.extend(maps_res['results'])
    while token:
        maps_res = client.places_nearby(location=coords,
                                        radius=1000,
                                        max_price=2,
                                        open_noew=True,
                                        page_token=token)
        token = maps_res.get('next_page_token', None)
        places.extend(maps_res['results'])

    return places


def parse_maps_data(user):
    """
    Parses Maps data of a user..

    :param {str} user - Username in the data/ directory.
    :return {float} Estimate of gas usage per month.
    """
    base_path = f'./data/{user}/Takeout/Maps/My labeled places'

    if not os.path.exists(f'{base_path}/Labeled places.json'):
        return {
            'total_distance': 0,
            'places': [],
            'fuel_needed': 0
        }

    with open(f'{base_path}/Labeled places.json', 'r') as f:
        data = json.load(f)
        features = data['features']

        # The coordinates are, for some reason, reversed.
        coords = list(map(lambda x:
                          x['geometry']['coordinates'][::-1], features))
        names = list(map(lambda x: x['properties']['name'], features))

        places = []
        total_distance = 0.

        # Get the total distance
        if 'Home' in names and 'Work' in names:
            # Get distance between home and work addresses
            home = list(
                filter(lambda p: p['properties']['name'] == 'Home', features))[0]
            work = list(
                filter(lambda p: p['properties']['name'] == 'Work', features))[0]

            total_distance += 1.2 * \
                get_maps_distance(
                    [home['geometry']['coordinates'][::-1], work['geometry']['coordinates'][::-1]])
        else:
            # (1. / 1.2) / 2 = 0.416
            total_distance += 0.416 * get_maps_distance(coords)

        # Get the places near work and home
        if 'Work' in names:
            places.extend(get_nearby_places(work['geometry']['coordinates']))

        if 'Home' in names:
            places.extend(get_nearby_places(home['geometry']['coordinates']))

        # 20 days/month, back and forth.
        total_distance *= 40.

        # Average gas mileage = 32mpg, compute total gas usage
        distance_in_miles = total_distance / (1000 * 1.606)
        gallons_needed = distance_in_miles / 32.
        fuel_needed_in_liters = 3.79 * gallons_needed

    return {
        'total_distance': total_distance / 1000,
        'places': places,
        'fuel_needed': fuel_needed_in_liters
    }
