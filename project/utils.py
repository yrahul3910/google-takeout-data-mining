import glob
import os


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
    for file in glob.glob('.*.cache'):
        os.remove(file)
