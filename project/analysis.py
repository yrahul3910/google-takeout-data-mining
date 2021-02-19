import os
import xml
import json
import datetime

import googlemaps
import numpy as np


def parse_fit_data(user):
    """
    Parses Google Fit data for a user. If no data exists,
    returns None.

    :param {str} user - Username in the data/ directory
    :return {list} List of dictionaries of the format
    {
        'calories': float,
        'distance': float,
        'dates': list
    }
    """
    base_path = f'./data/{user}/Takeout/Fit/Activities'

    if len(os.listdir(base_path)) == 0:
        return None

    activities_summary = []
    for file in os.listdir(base_path):
        filename = f'{base_path}/{file}'
        tree = xml.etree.ElementTree.parse(filename)
        root = tree.getroot()

        activities = root[0]
        cur_file_summary = {'calories': 0, 'distance': 0, 'dates': []}
        for activity in activities:
            # Get the sport and date/time
            sport = activity.attrib['Sport']
            date = activity[0]

            # Walk down the XML tree
            lap = activity[1]
            track = lap[0]
            calories = float(lap.find('Calories').text)
            distance = float(lap.find('DistanceMeters').text)

            cur_file_summary['calories'] += calories
            cur_file_summary['distance'] += distance
            cur_file_summary['dates'].append(date)

        activities_summary.append(cur_file_summary)

    return activities_summary


def get_key():
    # Get the API key from the .env file
    with open('.env', 'r') as f:
        line = f.readline()
        return line.split('=')[1]


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


if __name__ == '__main__':
    print(parse_maps_data('rahul'))
