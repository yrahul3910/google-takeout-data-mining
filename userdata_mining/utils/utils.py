import glob
import os
from collections.abc import Iterable
from typing import Callable


def get_username(data_path='.'):
    """
    Fetches the user whose data is on disk.
    """
    users = os.listdir(f'{data_path}/data')
    if len(users) == 0:
        print('WARN: No users to mine.')
        return None
    else:
        return users[0]


def get_key():
    # Get the API key from the .env file
    with open('.env', 'r') as f:
        line = f.readline()
        return line.split('=')[1]


def flush_caches():
    """
    Flushes all the caches from API data.
    Warning: calling this will permanently delete all the
    caches, requiring new API calls to fetch data. Only do this
    if you are sure.
    """
    for file in glob.glob('caches/.*.cache'):
        os.remove(file)


def _map(obj: Iterable, func: Callable):
    """
    A wrapper around map(...) that behaves more like JS.

    :param {Iterable} - An iterable object.
    :param {Callable} - A function or lambda
    """
    return list(map(func, obj))
