import csv

from bs4 import BeautifulSoup
from userdata_mining.utils import get_key, warn
from googleapiclient.discovery import build
import os
import ast
import json


def parse_yt_watch_history(user, data_path='.'):
    """
    Mines a user's youtube watch history.
    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} List of titles of videos watched.
    """
    path = f'{data_path}/data/{user}/Takeout/YouTube and YouTube Music/history/watch-history.html'

    # Check if the directory exists.
    if not os.path.exists(path):
        warn('YouTube watch history file does not exist.')
        return []

    # mine the data and retrieve the needed distinctions
    with open(path, encoding="utf8") as f:
        s = BeautifulSoup(f, 'html.parser')

    return [x.text for x in s.findAll('a')]


def parse_yt_comments(user, data_path='.'):
    """
    Mines a user's youtube comment history on any video.
    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} List of comments
    """
    path = f'{data_path}/data/{user}/Takeout/YouTube and YouTube Music/my-comments/my-comments.html'

    # Check if the directory exists.
    if not os.path.exists(path):
        warn('YouTube watch history path does not exist.')
        return []

    with open(path, encoding="utf8") as f:
        s = BeautifulSoup(f, 'html.parser')

    return [x.find('br').next_element.strip() for x in s.findAll('li')]


def parse_subscribed_channels(user, data_path='.'):
    """
    Mines a user's youtube subscribed channels of given data.
    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} List of dictionaries of the format
    """
    path = f'{data_path}/data/{user}/Takeout/YouTube and YouTube Music/subscriptions/subscriptions.json'

    # Check if the directory exists.
    if not os.path.exists(path):
        warn('YouTube watch history path does not exist.')
        return []

    with open(path, encoding="utf8") as f:
        data = json.load(f)

    return [s.get('snippet').get('title') for s in data]


def parse_liked_videos(user, data_path='.'):
    """
    Mines a user's youtube liked videos of given user.
    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} List of titles of liked videos
    """
    cache_dir = f'{data_path}/caches/.yt.cache'

    # Check for a cache
    if os.path.exists(cache_dir):
        f = open(cache_dir, 'r')
        line = f.readline()
        f.close()

        return ast.literal_eval(line)

    path = f'{data_path}/data/{user}/Takeout/YouTube and YouTube Music/playlists/Liked videos.csv'

    if not os.path.exists(path):
        warn('YouTube watch history file does not exist.')
        return []

    liked_video_ids = []
    with open(path, newline='') as f:
        read = csv.reader(f)
        for r in read:
            if r is not None and len(r) > 0:
                liked_video_ids.append(r[0])

    youtube = build("youtube", "v3", developerKey=get_key())

    liked_video_titles = []
    for i in liked_video_ids:
        res = youtube.videos().list(part='snippet', id=i).execute()
        if(res['items'] != []):
            stats = res['items'][0]['snippet']['title']
            liked_video_titles.append(stats)

    # Cache results
    with open(cache_dir, 'w') as f:
        f.write(str(liked_video_titles))

    return liked_video_titles
