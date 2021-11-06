from userdata_mining.utils import get_username, debug, info
from userdata_mining.mining import parse_fit_data
from userdata_mining.mining import parse_autofill, parse_browser_history
from userdata_mining.mining import parse_maps_data
from userdata_mining.mining import parse_maps
from userdata_mining.mining import parse_hangouts_data
from userdata_mining.mining import parse_mail_data
from userdata_mining.mining import parse_yt_comments, parse_yt_watch_history
from userdata_mining.mining import parse_subscribed_channels, parse_liked_videos
from userdata_mining.mining import parse_chats_data
from userdata_mining.mining import parse_play_data
from userdata_mining.mining import parse_pay_data
from userdata_mining.mining import parse_access_log_data
from userdata_mining.embedding import Embedding
from abc import ABC
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil import parser
import pickle
import numpy as np
import pandas as pd


class DataMiner(ABC):
    """
    A base class for data miners. Presents high-level functions that
    can be used by both users and subclasses, which provide more
    detailed functionality.
    """

    def __init__(self, data_path='.', user=None):
        """
        Initializes the data miner.

        :param {str} data_path - Path to the data/ folder.
        :param {str} user - The user name. If None, infers it automatically.
        """
        self.data_path = data_path

        if user is None:
            self.user = get_username(self.data_path)
        else:
            self.user = user

    def __getitem__(self, key):
        return self.__getattribute__(key)

    def __repr__(self):
        """
        Returns a string representation of the data stored by
        the object.
        """
        string = ''
        variables = [x for x in dir(self) if not x.startswith(
            '_') and not callable(self[x])]
        for key in variables:
            string += f'{key}: {self[key]}\n'
        return string

    def mine_data(self, data_path='.'):
        return NotImplemented


class GoogleDataMiner(DataMiner):
    """
    Mines Google data.
    """

    def mine_data(self):
        """
        Mines all data.

        :return {dict} A dictionary with mined, embedded data
        """
        fit_data = parse_fit_data(self.user, data_path=self.data_path)
        maps_data = parse_maps_data(self.user, data_path=self.data_path)
        autofill_data = parse_autofill(self.user, data_path=self.data_path)
        browser_data = parse_browser_history(
            self.user, data_path=self.data_path)
        hangouts_data = parse_hangouts_data(
            self.user, data_path=self.data_path)
        mail_data = parse_mail_data(self.user, data_path=self.data_path)
        maps_places_data = parse_maps(self.user, self.data_path)
        yt_comments_data = parse_yt_comments(self.user, self.data_path)
        yt_history_data = parse_yt_watch_history(self.user, self.data_path)
        yt_subscribed_data = parse_subscribed_channels(
            self.user, self.data_path)
        yt_liked_data = parse_liked_videos(self.user, self.data_path)
        chats_data = parse_chats_data(self.user, self.data_path)
        movies_data = parse_play_data(self.user, 'movies', self.data_path)
        apps_data = parse_play_data(self.user, 'apps', self.data_path)
        transactions_data = parse_pay_data(self.user, self.data_path)
        activities_data = parse_access_log_data(self.user, self.data_path)

        info('Data parsed.')

        # Extract features from Fit data
        # First, get total distance, total distance in past year,
        # total calories, total calories in past year.
        today = datetime.today()

        if fit_data:
            total_distance = sum([x['distance'] for x in fit_data])
            total_calories = sum([x['calories'] for x in fit_data])
            total_dist_year = sum([x['distance'] for x in fit_data if parser.parse(
                max(x['dates'])).replace(tzinfo=None) < today - relativedelta(years=1)])
            total_cal_year = sum([x['calories'] for x in fit_data if parser.parse(
                max(x['dates'])).replace(tzinfo=None) < today - relativedelta(years=1)])
        else:
            total_distance = 0
            total_calories = 0
            total_dist_year = 0
            total_cal_year = 0

        self.mined_fit_data = {
            'total_dist': total_distance,

            'total_cal': total_calories,
            'total_dist_yr': total_dist_year,
            'total_cal_yr': total_cal_year
        }

        info('Embedding text data. This may take a while.')
        embedding = Embedding(model='bert-base-uncased')

        if activities_data:
            self.activities_embeddings = [
                embedding.embed(x) for x in activities_data]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/activities.pickle', 'wb') as f:
                pickle.dump(self.activities_embeddings, f)
        else:
            self.activities_embeddings = []

        if apps_data:
            info('Embedding Google Play Apps data. This may take a while.')
            self.apps_embeddings = [
                embedding.embed(x) for x in apps_data]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/apps.pickle', 'wb') as f:
                pickle.dump(self.apps_embeddings, f)
        else:
            self.apps_embeddings = []

        if autofill_data:
            self.autofill_place_embeddings = [
                embedding.embed(x) for x in autofill_data]
        else:
            self.autofill_place_embeddings = []

        if browser_data:
            self.history_embeddings = [
                embedding.embed(x) for x in browser_data]
        else:
            self.history_embeddings = []

        if hangouts_data:
            info('Embedding Hangouts data. This may take a while.')
            self.messages_embeddings = [
                embedding.embed(x) for x in hangouts_data]
            self.messages_embeddings = [
                x for x in self.messages_embeddings if x is not None]
            
            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/hangouts.pickle', 'wb') as f:
                pickle.dump(self.messages_embeddings, f)
        else:
            self.messages_embeddings = []
        
        if chats_data:
            info('Embedding Google Chat data. This may take a while.')
            self.chats_embeddings = [
                embedding.embed(x) for x in chats_data]
        else:
            self.chats_embeddings = []

        if movies_data:
            info('Embedding Google Play Movies data. This may take a while.')
            self.movies_embeddings = [
                embedding.embed(x) for x in movies_data]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/movies.pickle', 'wb') as f:
                pickle.dump(self.movies_embeddings, f)
        else:
            self.movies_embeddings = []

        if transactions_data:
            info('Embedding Google Pay transaction data. This may take a while.')
            self.transactions_embeddings = [
                embedding.embed(x) for x in transactions_data]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/pay.pickle', 'wb') as f:
                pickle.dump(self.transactions_embeddings, f)
        else:
            self.transactions_embeddings = []

        self.distance_traveled = maps_data['total_distance']
        self.nearby_places_embeddings = [
            embedding.embed(x) for x in maps_data['places']]
        self.maps_places_embeddings = [
            embedding.embed(x) for x in maps_places_data
        ]
        self.yt_comments_embeddings = [
            embedding.embed(x) for x in yt_comments_data
        ]
        self.yt_history_embeddings = [
            embedding.embed(x) for x in yt_history_data
        ]
        self.yt_subscribed_embeddings = [
            embedding.embed(x) for x in yt_subscribed_data
        ]
        self.yt_liked_embeddings = [
            embedding.embed(x) for x in yt_liked_data
        ]

        # Join nearby places with data from Maps (your places)
        self.nearby_places_embeddings = np.vstack(
            (self.nearby_places_embeddings, self.maps_places_embeddings))

        if activities_data is None:
            # Load cached embeddings
            with open(f'{self.data_path}/saved/embeddings/activities.pickle', 'rb') as f:
                self.activities_embeddings = pickle.load(f)

        if apps_data is None:
            # Load cached embeddings
            with open(f'{self.data_path}/saved/embeddings/apps.pickle', 'rb') as f:
                self.apps_embeddings = pickle.load(f)

        if chats_data is None:
            # Load cached embeddings
            with open(f'{self.data_path}/saved/embeddings/chat.pkl', 'rb') as f:
                self.chats_embeddings = pickle.load(f)

        if hangouts_data is None:
            # Load cached embeddings
            with open(f'{self.data_path}/saved/embeddings/hangouts.pickle', 'rb') as f:
                self.messages_embeddings = pickle.load(f)

        if mail_data is None:
            # Load cached embeddings
            with open(f'{self.data_path}/saved/embeddings/mail.pickle', 'rb') as f:
                self.email_embeddings = pickle.load(f)

        if movies_data is None:
            # Load cached embeddings
            with open(f'{self.data_path}/saved/embeddings/movies.pickle', 'rb') as f:
                self.movies_embeddings = pickle.load(f)

        if transactions_data is None:
            # Load cached embeddings
            with open(f'{self.data_path}/saved/embeddings/pay.pickle', 'rb') as f:
                self.transactions_embeddings = pickle.load(f)

        else:
            info('Embedding email data. This may take a while.')
            self.email_embeddings = [embedding.embed(x) for x in mail_data]
            self.email_embeddings = [
                x for x in self.email_embeddings if x is not None]
            # Cache email embeddings
            with open(f'{self.data_path}/saved/embeddings/mail.pickle', 'wb') as f:
                pickle.dump(self.email_embeddings, f)

        info(f'Embedding complete. Data details:\n' +
             f'Activities: {len(self.activities_embeddings)} item(s).\n' +
             f'Apps: {len(self.apps_embeddings)} item(s).\n' +
             f'Autofill: {len(self.autofill_place_embeddings)} item(s).\n' +
             f'Browser history: {len(self.history_embeddings)} item(s).\n' +
             f'Hangouts: {len(self.messages_embeddings)} item(s).\n' +
             f'Google Chat: {len(self.chats_embeddings)} item(s).\n' +
             f'Google Pay Transactions: {len(self.transactions_embeddings)} item(s).\n' +
             f'Monthly travel estimate: {self.distance_traveled} km.\n' +
             f'Nearby places: {len(self.nearby_places_embeddings)} item(s).\n' +
             f'Email: {len(self.email_embeddings)} item(s).\n' +
             f'Movies: {len(self.movies_embeddings)} item(s). \n' +
             f'YouTube comments: {len(self.yt_comments_embeddings)} item(s).\n' +
             f'YouTube subscriptions: {len(self.yt_subscribed_embeddings)} item(s).\n' +
             f'YouTube liked videos: {len(self.yt_liked_embeddings)} item(s).\n' +
             f'YouTube watch history: {len(self.yt_history_embeddings)} item(s).')

        return {
            'Activities': self.activities_embeddings,
            'Apps': self.apps_embeddings,
            'Autofill': self.autofill_place_embeddings,
            'Browser History': self.history_embeddings,
            'Chat': self.chats_embeddings,
            'Hangouts': self.messages_embeddings,
            'Travel': self.distance_traveled,
            'Nearby Places': self.nearby_places_embeddings,
            'Email': self.email_embeddings,
            'Movies': self.movies_embeddings,
            'Pay Transactions': self.transactions_embeddings,
            'YouTube comments': self.yt_comments_embeddings,
            'YouTube subscriptions': self.yt_subscribed_embeddings,
            'YouTube liked videos': self.yt_liked_embeddings,
            'YouTube watch history': self.yt_history_embeddings
        }
