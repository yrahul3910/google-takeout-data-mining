import csv

from bs4 import BeautifulSoup
from googleapiclient.discovery import build
import os
import json

user= "rmullap"
api_key = "AIzaSyAdUxMzJB8zhy-3VM_SN7F5xVbNTFFg4KY"

def parse_YT_watch_history(user,data_path='.'):
    """
       Mines a user's youtube watch history.
       :param {str} user - The user directory.
       :param {str} data_path - Path to the data/ directory, NOT ending in a /.
       :return {list} List of dictionaries of the format
        {
            'Video Link': String,
            'Name': String,
        }
       """
    # path = f'{data_path}/data/{user}/Takeout/YouTube and YouTube Music/history/watch-history.html'

    path = "E:/ramya/ALDA/Project/data/rmullap/Takeout/YouTube and YouTube Music/history/watch-history.html"

    # whether if the directory exists.
    if not os.path.exists(path):
        return []

    # mine the data and retrieve the needed distinctions
    watched_summary = []
    with open(path,encoding="utf8") as f:
        s = BeautifulSoup(f, 'html.parser')

        for href in s.findAll('a'):
            record = {'VideoLink': href.get("href"), 'Name': href.text}
            watched_summary.append(record)
    return watched_summary

# for i in parse_YT_watch_history(user):
  #  print(i)

def parse_YT_liveChat_history(user):
    """
        Mines a user's youtube live chat messages history on any video.
        :param {str} user - The user directory.
        :param {str} data_path - Path to the data/ directory, NOT ending in a /.
        :return {list} List of dictionaries of the format
        {
            'Video Link': String,
            'Message': String,
        }
    """

    path = "E:/ramya/ALDA/Project/data/rmullap/Takeout/YouTube and YouTube Music/my-live-chat-messages/my-live-chat-messages.html"
    # whether if the directory exists.
    if not os.path.exists(path):
        return []

    chat_summary = []
    with open(path,encoding="utf8") as f:
        s = BeautifulSoup(f, 'html.parser')
        for href in s.findAll('li'):
            record = {'VideoLink': href.find('a').get("href"), 'Message': href.find('br').next_element.strip()}
            chat_summary.append(record)
    return chat_summary

# for i in parse_YT_commented_history(user):
  #  print(i)

def parse_YT_comments(user):
    """
            Mines a user's youtube comment history on any video.
            :param {str} user - The user directory.
            :param {str} data_path - Path to the data/ directory, NOT ending in a /.
            :return {list} List of dictionaries of the format
            {
                'Video Link': String,
                'Comment': String,
            }
    """
    path = "E:/ramya/ALDA/Project/data/rmullap/Takeout/YouTube and YouTube Music/my-comments/my-comments.html"
    # whether if the directory exists.
    if not os.path.exists(path):
        return []

    commented_summary = []
    with open(path, encoding="utf8") as f:
        s = BeautifulSoup(f, 'html.parser')
        for href in s.findAll('li'):
            record = {'VideoLink': href.findAll('a')[-1], 'Comment': href.find('br').next_element.strip()}
            commented_summary.append(record)
    return commented_summary

parse_YT_comments(user)

def parse_subscribed_channels():
    """
        Mines a user's youtube subscribed channels of given data.
        :param {str} user - The user directory.
        :param {str} data_path - Path to the data/ directory, NOT ending in a /.
        :return {list} List of dictionaries of the format
        {
            'channel id': String,
            'Title': String,
        }
    """
    path = "E:/ramya/ALDA/Project/data/rmullap/Takeout/BACKEDYouTube and YouTube Music/subscriptions/subscriptions.json"
    subscribed_channels_list = []
    with open(path, encoding="utf8") as f:
        data = json.load(f)
        for s in data:
            record = {'channel id': s.get('snippet').get('resourceId').get('channelId'), 'Title': s.get('snippet').get('title')}
            subscribed_channels_list.append(record)
    return subscribed_channels_list

parse_subscribed_channels(user)

def parse_liked_videos(user):
    """
            Mines a user's youtube liked videos of given user.
            :param {str} user - The user directory.
            :param {str} data_path - Path to the data/ directory, NOT ending in a /.
            :return {list} List of titles of liked videos
    """
    path = "E:/ramya/ALDA/Project/data/rmullap/Takeout/YouTube and YouTube Music/playlists/Liked videos.csv"
    if not os.path.exists(path):
        return []

    liked_video_ids=[]
    with open(path, newline='') as f:
        read = csv.reader(f)
        for r in read:
            if(r is not None):
                liked_video_ids.append(r[0])

    youtube = build("youtube", "v3", developerKey=api_key)

    liked_video_titles = []
    for i in liked_video_ids:
        res = youtube.videos().list(part='snippet', id=i).execute()
        if(res['items'] != []):
            stats = res['items'][0]['snippet']['title']
            liked_video_titles.append(stats)
    return liked_video_titles

parse_liked_videos(user)
