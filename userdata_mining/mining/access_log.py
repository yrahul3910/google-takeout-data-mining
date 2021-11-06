import glob
import csv
import os
from userdata_mining.utils import warn


def parse_access_log_data(user, data_path='.'):
    """
    Parse the Access Log Activity data of the user

    Args:
        user(str): The user to parse.
        data_path (str): The path to the data.

    Returns:
        list: A list of IP addresses used to access Google services by the user
    """
    # First, check for cache
    if os.path.exists(f'{data_path}/saved/embeddings/access.pickle'):
        return None

    path = f'{data_path}/data/{user}/Takeout/Access Log Activity/Activities - A list of Google services accessed by.csv'

    # Does the directory exist?
    if not os.path.exists(path):
        warn('Access Log Activity data path does not exist.')
        return []

    activities = set()

    for file in glob.glob(f'{path}'):
        with open(file, 'r') as f:
            read = csv.reader(f)
            for r in read:
                if r is not None and len(r) > 0 and r[2] != '' and r[2] != 'IP Address':
                    activities.add(r[2])

    return list(activities)
