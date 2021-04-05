from userdata_mining.utils import get_username, debug
from userdata_mining.mining import parse_fit_data
from userdata_mining.mining import parse_autofill, parse_browser_history
from userdata_mining.mining import parse_maps_data
from userdata_mining.mining import parse_mail_data
from userdata_mining.mining import parse_hangouts_data
from userdata_mining.mining import parse_mail_data
from userdata_mining.embedding import Embedding
from abc import ABC
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil import parser
import pickle
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

    def mine_data(self):
        return NotImplemented


class GoogleDataMiner(DataMiner):
    """
    Mines Google data.
    """

    def mine_data(self):
        fit_data = parse_fit_data(self.user)
        maps_data = parse_maps_data(self.user)
        autofill_data = parse_autofill(self.user)
        browser_data = parse_browser_history(self.user)
        hangouts_data = parse_hangouts_data(self.user)
        mail_data = parse_mail_data(self.user)

        # Extract features from Fit data
        # First, get total distance, total distance in past year,
        # total calories, total calories in past year.
        today = datetime.today()
        total_distance = sum([x['distance'] for x in fit_data])
        total_calories = sum([x['calories'] for x in fit_data])
        total_dist_year = sum([x['distance'] for x in fit_data if parser.parse(
            max(x['dates'])).replace(tzinfo=None) < today - relativedelta(years=1)])
        total_cal_year = sum([x['calories'] for x in fit_data if parser.parse(
            max(x['dates'])).replace(tzinfo=None) < today - relativedelta(years=1)])

        self.mined_fit_data = {
            'total_dist': total_distance,
            'total_cal': total_calories,
            'total_dist_yr': total_dist_year,
            'total_cal_yr': total_cal_year
        }

        embedding = Embedding(model='bert-base-uncased')
        self.autofill_place_embeddings = [
            embedding.embed(x) for x in autofill_data]
        self.history_embeddings = [embedding.embed(x) for x in browser_data]
        self.messages_embeddings = [embedding.embed(x) for x in hangouts_data]
        self.distance_traveled = maps_data['total_distance']
        self.nearby_places_embeddings = [
            embedding.embed(x) for x in maps_data['places']]
        self.email_embeddings = [embedding.embed(x) for x in mail_data]

        # Cache email embeddings
        with open('.mail.cache', 'wb') as f:
            pickle.dump(self.email_embeddings, f)
