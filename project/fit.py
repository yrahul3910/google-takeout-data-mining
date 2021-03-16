from utils import get_key
import os
import xml
import datetime


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

    if not os.path.exists(base_path):
        return None

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
