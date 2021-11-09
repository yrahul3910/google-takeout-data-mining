from userdata_mining.utils import get_username, debug, info
from userdata_mining.mining import parse_fit_data
from userdata_mining.mining import parse_autofill, parse_browser_history
from userdata_mining.mining import parse_maps_data
from userdata_mining.mining import parse_maps
from userdata_mining.mining import parse_mail_data
from userdata_mining.mining import parse_hangouts_data
from userdata_mining.mining import parse_mail_data
from userdata_mining.mining import parse_yt_comments, parse_yt_watch_history
from userdata_mining.mining import parse_subscribed_channels, parse_liked_videos
from userdata_mining.mining import parse_chats_data
from userdata_mining.mining import parse_play_data
from userdata_mining.embedding import Embedding
from userdata_mining.mining import parse_insta_ads_viewed
from userdata_mining.mining import parse_insta_music_heard
from userdata_mining.mining import parse_insta_videos_watched
from userdata_mining.mining import parse_insta_ads_interest
from userdata_mining.mining import parse_insta_your_topics
from userdata_mining.mining import parse_insta_your_reels_topics
from userdata_mining.mining import parse_insta_your_reels_sentiments
from userdata_mining.mining import parse_insta_saved_posts
from userdata_mining.mining import parse_insta_account_searches
from userdata_mining.mining import parse_insta_monetization_eligibility
from userdata_mining.mining import parse_insta_liked_comments
from userdata_mining.mining import parse_insta_liked_posts
from userdata_mining.mining import parse_insta_post_comments
from userdata_mining.mining import parse_insta_information_submitted
from userdata_mining.mining import parse_insta_posts_viewed
from userdata_mining.mining import parse_insta_suggested_accounts_viewed
from userdata_mining.mining import parse_insta_account_based_in
from userdata_mining.mining import parse_insta_comments_allowed_from
from userdata_mining.mining import parse_insta_use_cross_app_messaging
from userdata_mining.mining import parse_insta_emoji_sliders
from userdata_mining.mining import parse_insta_polls
from userdata_mining.mining import parse_insta_quizzes
from userdata_mining.mining import parse_insta_archived_posts
from userdata_mining.mining import parse_insta_stories
from userdata_mining.mining import parse_insta_followers
from userdata_mining.mining import parse_insta_following
from userdata_mining.mining import parse_insta_hide_story_from
from userdata_mining.mining import parse_insta_messages
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


class FbInstaDataMiner(DataMiner):
    """
    Mines Instagram data.
    """
    
    def mine_data(self):
        """
        Mines all data of Instagram and Facebook
        
        :return {dict} A dictonary with mined, embedded data
        """
        ads_data = parse_insta_ads_viewed(self.user, data_path=self.data_path)
        music_heard_data = parse_insta_music_heard(self.user, data_path=self.data_path)
        videos_watched_data = parse_insta_videos_watched(self.user, data_path=self.data_path)
        ads_interest_data = parse_insta_ads_interest(self.user, data_path=self.data_path)
        your_topics_data = parse_insta_your_topics(self.user, data_path=self.data_path)
        reels_topics_data = parse_insta_your_reels_topics(self.user, data_path=self.data_path)
        reels_sentiments_data = parse_insta_your_reels_sentiments(self.user, data_path=self.data_path)
        saved_posts_data = parse_insta_saved_posts(self.user, data_path=self.data_path)
        account_searches_data = parse_insta_account_searches(self.user, data_path=self.data_path)
        memo_data = parse_insta_monetization_eligibility(self.user, data_path=self.data_path)
        liked_comments_data = parse_insta_liked_comments(self.user, data_path=self.data_path)
        liked_posts_data = parse_insta_liked_posts(self.user, data_path=self.data_path)
        post_comments_data = parse_insta_post_comments(self.user, data_path=self.data_path)
        info_submitted_data = parse_insta_information_submitted(self.user, data_path=self.data_path)
        posts_viewed_data = parse_insta_posts_viewed(self.user, data_path=self.data_path)
        accounts_viewed_data = parse_insta_suggested_accounts_viewed(self.user, data_path=self.data_path)
        accounts_based_in_data = parse_insta_account_based_in(self.user, data_path=self.data_path)
        comments_data = parse_insta_comments_allowed_from(self.user, data_path=self.data_path)
        cross_app_data = parse_insta_use_cross_app_messaging(self.user, data_path=self.data_path)
        emojis_data = parse_insta_emoji_sliders(self.user, data_path=self.data_path)
        polls_data = parse_insta_polls(self.user, data_path=self.data_path)
        quizzes_data = parse_insta_quizzes(self.user, data_path=self.data_path)
        archieved_posts_data = parse_insta_archived_posts(self.user, data_path=self.data_path)
        stories_data = parse_insta_stories(self.user, data_path=self.data_path)
        followers_data = parse_insta_followers(self.user, data_path=self.data_path)
        following_data = parse_insta_following(self.user, data_path=self.data_path)
        hide_story_data = parse_insta_hide_story_from(self.user, data_path=self.data_path)
        messages_data = parse_insta_messages(self.user, data_path=self.data_path)
        
        info('Data parsed.')
        
        info('Embedding text data. This may take a while.')
        embedding = Embedding(model='bert-base-uncased')
        
         if ads_data:
            self.ads_data = [
                embedding.embed(x) for x in ads_data]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/apps.pickle', 'wb') as f:
                pickle.dump(self.apps_embeddings, f)
        else:
            self.apps_embeddings = []
            
        if music_heard_data:
            self.music_heard_data = [
                embedding.embed(x) for x in music_heard_data]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/apps.pickle', 'wb') as f:
                pickle.dump(self.apps_embeddings, f)
        else:
            self.apps_embeddings = []
            
        if videos_watched_data:
            self.videos_watched_data = [
                embedding.embed(x) for x in videos_watched_data]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/apps.pickle', 'wb') as f:
                pickle.dump(self.apps_embeddings, f)
        else:
            self.apps_embeddings = []
        
        if ads_interest_data:
            self.ads_interest_data = [
                embedding.embed(x) for x in ads_interest_data]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/apps.pickle', 'wb') as f:
                pickle.dump(self.apps_embeddings, f)
        else:
            self.apps_embeddings = []

        if your_topics_data:
            self.your_topics_data = [
                embedding.embed(x) for x in your_topics_data]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/apps.pickle', 'wb') as f:
                pickle.dump(self.apps_embeddings, f)
        else:
            self.apps_embeddings = []
            
        if reels_topics_data:
            self.reels_topics_data = [
                embedding.embed(x) for x in reels_topics_data]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/apps.pickle', 'wb') as f:
                pickle.dump(self.apps_embeddings, f)
        else:
            self.apps_embeddings = []
            
        if reels_sentiments_data:
            self.reels_sentiments_data = [
                embedding.embed(x) for x in reels_sentiments_data]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/apps.pickle', 'wb') as f:
                pickle.dump(self.apps_embeddings, f)
        else:
            self.apps_embeddings = []
        
        if saved_posts_data:
            self.saved_posts_data = [
                embedding.embed(x) for x in saved_posts_data]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/apps.pickle', 'wb') as f:
                pickle.dump(self.apps_embeddings, f)
        else:
            self.apps_embeddings = []
            
        if account_searches_data:
            self.account_searches_data = [
                embedding.embed(x) for x in account_searches_data]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/apps.pickle', 'wb') as f:
                pickle.dump(self.apps_embeddings, f)
        else:
            self.apps_embeddings = []
    
        if memo_data:
            self.memo_data = [
                embedding.embed(x) for x in memo_data]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/apps.pickle', 'wb') as f:
                pickle.dump(self.apps_embeddings, f)
        else:
            self.apps_embeddings = []
        
        if liked_comments_data:
            self.liked_comments_data = [
                embedding.embed(x) for x in liked_comments_data]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/apps.pickle', 'wb') as f:
                pickle.dump(self.apps_embeddings, f)
        else:
            self.apps_embeddings = []
        
        if liked_posts_data:
            self.liked_posts_data = [
                embedding.embed(x) for x in liked_posts_data]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/apps.pickle', 'wb') as f:
                pickle.dump(self.apps_embeddings, f)
        else:
            self.apps_embeddings = []

        if post_comments_data:
            self.post_comments_data = [
                embedding.embed(x) for x in post_comments_data]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/apps.pickle', 'wb') as f:
                pickle.dump(self.apps_embeddings, f)
        else:
            self.apps_embeddings = []

        if info_submitted_data:
            self.info_submitted_data = [
                embedding.embed(x) for x in info_submitted_data]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/apps.pickle', 'wb') as f:
                pickle.dump(self.apps_embeddings, f)
        else:
            self.apps_embeddings = []

        if posts_viewed_data:
            self.posts_viewed_data = [
                embedding.embed(x) for x in posts_viewed_data]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/apps.pickle', 'wb') as f:
                pickle.dump(self.apps_embeddings, f)
        else:
            self.apps_embeddings = []

        if accounts_viewed_data:
            self.accounts_viewed_data = [
                embedding.embed(x) for x in accounts_viewed_data]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/apps.pickle', 'wb') as f:
                pickle.dump(self.apps_embeddings, f)
        else:
            self.apps_embeddings = []

        if accounts_based_in_data:
            self.accounts_based_in_data = [
                embedding.embed(x) for x in accounts_based_in_data]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/apps.pickle', 'wb') as f:
                pickle.dump(self.apps_embeddings, f)
        else:
            self.apps_embeddings = []

        if comments_data:
            self.comments_data = [
                embedding.embed(x) for x in comments_data]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/apps.pickle', 'wb') as f:
                pickle.dump(self.apps_embeddings, f)
        else:
            self.apps_embeddings = []

        if cross_app_data:
            self.cross_app_data = [
                embedding.embed(x) for x in cross_app_data]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/apps.pickle', 'wb') as f:
                pickle.dump(self.apps_embeddings, f)
        else:
            self.apps_embeddings = []

        if emojis_data:
            self.emojis_data = [
                embedding.embed(x) for x in emojis_data]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/apps.pickle', 'wb') as f:
                pickle.dump(self.apps_embeddings, f)
        else:
            self.apps_embeddings = []

        if polls_data:
            self.polls_data = [
                embedding.embed(x) for x in polls_data]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/apps.pickle', 'wb') as f:
                pickle.dump(self.apps_embeddings, f)
        else:
            self.apps_embeddings = []

        if quizzes_data:
            self.quizzes_data = [
                embedding.embed(x) for x in quizzes_data]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/apps.pickle', 'wb') as f:
                pickle.dump(self.apps_embeddings, f)
        else:
            self.apps_embeddings = []

        if archieved_posts_data:
            self.archieved_posts_data = [
                embedding.embed(x) for x in archieved_posts_data]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/apps.pickle', 'wb') as f:
                pickle.dump(self.apps_embeddings, f)
        else:
            self.apps_embeddings = []

        if stories_data:
            self.stories_data = [
                embedding.embed(x) for x in stories_data]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/apps.pickle', 'wb') as f:
                pickle.dump(self.apps_embeddings, f)
        else:
            self.apps_embeddings = []

        if followers_data:
            self.followers_data = [
                embedding.embed(x) for x in followers_data]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/apps.pickle', 'wb') as f:
                pickle.dump(self.apps_embeddings, f)
        else:
            self.apps_embeddings = []


        if following_data:
            self.following_data = [
                embedding.embed(x) for x in following_data]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/apps.pickle', 'wb') as f:
                pickle.dump(self.apps_embeddings, f)
        else:
            self.apps_embeddings = []

        if hide_story_data:
            self.hide_story_data = [
                embedding.embed(x) for x in hide_story_data]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/apps.pickle', 'wb') as f:
                pickle.dump(self.apps_embeddings, f)
        else:
            self.apps_embeddings = []

        if messages_data:
            self.messages_data = [
                embedding.embed(x) for x in messages_data]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/apps.pickle', 'wb') as f:
                pickle.dump(self.apps_embeddings, f)
        else:
            self.apps_embeddings = []
            
            
        fb_ads_data = parse_fb_advitisors(self.user, data_path=self.data_path)
        fb_apps_data = parse_fb_apps_and_websites(self.user, data_path=self.data_path)
        fb_posts_apps_data = parse_fb_posts_from_apps_and_websites(self.user, data_path=self.data_path)
        fb_your_topics_data = parse_fb_your_topics(self.user, data_path=self.data_path)
        fb_comments_data = parse_fb_comments(self.user, data_path=self.data_path)
        fb_reactions_data = parse_fb_reactions(self.user, data_path=self.data_path)
        fb_search_historydata = parse_fb_search_history(self.user, data_path=self.data_path)
        fb_saved_posts_data = parse_fb_pages_you_follow(self.user, data_path=self.data_path)
        fb_pages_you_follow_data = parse_fb_pages_you_liked(self.user, data_path=self.data_path)
        fb_ads_interest_data = parse_fb_ads_interest(self.user, data_path=self.data_path)
        fb_frnd_peer_group_data = parse_fb_frnd_peer_group(self.user, data_path=self.data_path)
        fb_groups_comments_data = parse_fb_groups_comments(self.user, data_path=self.data_path)
        fb_groups_membership_data = parse_fb_groups_membership(self.user, data_path=self.data_path)
        fb_groups_posts_data = parse_fb_groups_posts(self.user, data_path=self.data_path)
        fb_messages_data = parse_fb_messages(self.user, data_path=self.data_path)

        if fb_ads_data:
            self.fb_ads_data = [
                embedding.embed(x) for x in fb_ads_data]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/apps.pickle', 'wb') as f:
                pickle.dump(self.apps_embeddings, f)
        else:
            self.apps_embeddings = []

        if fb_apps_data:
            self.fb_apps_data = [
                embedding.embed(x) for x in fb_apps_data]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/apps.pickle', 'wb') as f:
                pickle.dump(self.apps_embeddings, f)
        else:
            self.apps_embeddings = []

        if fb_posts_apps_data:
            self.fb_posts_apps_data = [
                embedding.embed(x) for x in fb_posts_apps_data]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/apps.pickle', 'wb') as f:
                pickle.dump(self.apps_embeddings, f)
        else:
            self.apps_embeddings = []

        if fb_your_topics_data:
            self.fb_your_topics_data = [
                embedding.embed(x) for x in fb_your_topics_data]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/apps.pickle', 'wb') as f:
                pickle.dump(self.apps_embeddings, f)
        else:
            self.apps_embeddings = []

        if fb_comments_data:
            self.fb_comments_data = [
                embedding.embed(x) for x in fb_comments_data]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/apps.pickle', 'wb') as f:
                pickle.dump(self.apps_embeddings, f)
        else:
            self.apps_embeddings = []

        if fb_reactions_data:
            self.fb_reactions_data = [
                embedding.embed(x) for x in fb_reactions_data]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/apps.pickle', 'wb') as f:
                pickle.dump(self.apps_embeddings, f)
        else:
            self.apps_embeddings = []

        if fb_search_historydata:
            self.fb_search_historydata = [
                embedding.embed(x) for x in fb_search_historydata]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/apps.pickle', 'wb') as f:
                pickle.dump(self.apps_embeddings, f)
        else:
            self.apps_embeddings = []

        if fb_saved_posts_data:
            self.fb_saved_posts_data = [
                embedding.embed(x) for x in fb_saved_posts_data]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/apps.pickle', 'wb') as f:
                pickle.dump(self.apps_embeddings, f)
        else:
            self.apps_embeddings = []

        if fb_pages_you_follow_data:
            self.fb_pages_you_follow_data = [
                embedding.embed(x) for x in fb_pages_you_follow_data]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/apps.pickle', 'wb') as f:
                pickle.dump(self.apps_embeddings, f)
        else:
            self.apps_embeddings = []

        if fb_ads_interest_data:
            self.fb_ads_interest_data = [
                embedding.embed(x) for x in fb_ads_interest_data]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/apps.pickle', 'wb') as f:
                pickle.dump(self.apps_embeddings, f)
        else:
            self.apps_embeddings = []

        if fb_frnd_peer_group_data:
            self.fb_frnd_peer_group_data = [
                embedding.embed(x) for x in fb_frnd_peer_group_data]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/apps.pickle', 'wb') as f:
                pickle.dump(self.apps_embeddings, f)
        else:
            self.apps_embeddings = []

        if fb_groups_comments_data:
            self.fb_groups_comments_data = [
                embedding.embed(x) for x in fb_groups_comments_data]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/apps.pickle', 'wb') as f:
                pickle.dump(self.apps_embeddings, f)
        else:
            self.apps_embeddings = []


        if fb_groups_membership_data:
            self.fb_groups_membership_data = [
                embedding.embed(x) for x in fb_groups_membership_data]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/apps.pickle', 'wb') as f:
                pickle.dump(self.apps_embeddings, f)
        else:
            self.apps_embeddings = []

        if fb_groups_posts_data:
            self.fb_groups_posts_data = [
                embedding.embed(x) for x in fb_groups_posts_data]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/apps.pickle', 'wb') as f:
                pickle.dump(self.apps_embeddings, f)
        else:
            self.apps_embeddings = []

        if fb_messages_data:
            self.fb_messages_data = [
                embedding.embed(x) for x in fb_messages_data]

            # Cache embeddings
            with open(f'{self.data_path}/saved/embeddings/apps.pickle', 'wb') as f:
                pickle.dump(self.apps_embeddings, f)
        else:
            self.apps_embeddings = []
            
        return {
            'Insta Advertisements Data': self.ads_data,
            'Insta Music heard': self.music_heard_data,
            'Insta Videos watched': self.videos_watched_data,
            'Insta Interests': self.ads_interest_data,
            'Insta Topics': self.your_topics_data,
            'Insta Reels Topics': self.reels_topics_data,
            'Insta Reels Sentiments': self.reels_sentiments_data,
            'Insta Posts Saved': self.saved_posts_data,
            'Insta Account Searches': self.account_searches_data,
            'Insta Memo Data': self.memo_data,
            'Insta Liked Comments': self.liked_comments_data,
            'Insta Liked Posts': self.liked_posts_data,
            'Insta Post Comments': self.post_comments_data,
            'Insta Information Submitted': self.info_submitted_data,
            'Insta Posts viewed': self.posts_viewed_data,
            'Insta Accounts Viewwed': self.accounts_viewed_data,
            'Insta Accounts based': self.accounts_based_in_data,
            'Insta Comments': self.comments_data,
            'Insta Cross App Data': self.cross_app_data,
            'Insta Emojis': self.emojis_data,
            'Insta Polls': self.polls_data,
            'Insta Quizzes': self.quizzes_data,
            'Insta Archieved Posts': self.archieved_posts_data,
            'Insta Stories': self.stories_data,
            'Insta Followers': self.followers_data,
            'Insta Following': self.following_data,
            'Insta Hided story': self.hide_story_data,
            'Insta Messages': self.messages_data,
            'FB Advertisements': self.fb_ads_data,
            'FB Apps': self.fb_apps_data,
            'FB Posts Apps': self.fb_posts_apps_data,
            'FB Topics': self.fb_your_topics_data,
            'FB Comments': self.fb_comments_data,
            'FB Reactions': self.fb_reactions_data,
            'FB Search History': self.fb_search_historydata,
            'FB Saved posts': self.fb_saved_posts_data,
            'FB Pages followed': self.fb_pages_you_follow_data,
            'FB Ad interests': self.fb_ads_interest_data,
            'FB Friend peer group': self.fb_frnd_peer_group_data,
            'FB Group comments': self.fb_groups_comments_data,
            'FB Group membership': self.fb_groups_membership_data,
            'FB Group posts': self.fb_groups_posts_data,
            'FB Messages': self.fb_messages_data
        }
        
        

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

        if apps_data:
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

        if apps_data is None:
            #Load cached embeddings
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
            #Load cached embeddings
            with open(f'{self.data_path}/saved/embeddings/movies.pickle', 'rb') as f:
                self.movies_embeddings = pickle.load(f)

        else:
            info('Embedding email data. This may take a while.')
            self.email_embeddings = [embedding.embed(x) for x in mail_data]
            self.email_embeddings = [
                x for x in self.email_embeddings if x is not None]
            # Cache email embeddings
            with open(f'{self.data_path}/saved/embeddings/mail.pickle', 'wb') as f:
                pickle.dump(self.email_embeddings, f)

        info(f'Embedding complete. Data details:\n' +
             f'Apps: {len(self.apps_embeddings)} item(s).\n' +
             f'Autofill: {len(self.autofill_place_embeddings)} item(s).\n' +
             f'Browser history: {len(self.history_embeddings)} item(s).\n' +
             f'Hangouts: {len(self.messages_embeddings)} item(s).\n' +
             f'Google Chat: {len(self.chats_embeddings)} item(s).\n' +
             f'Monthly travel estimate: {self.distance_traveled} km.\n' +
             f'Nearby places: {len(self.nearby_places_embeddings)} item(s).\n' +
             f'Email: {len(self.email_embeddings)} item(s).\n' +
             f'Movies: {len(self.movies_embeddings)} item(s). \n' +
             f'YouTube comments: {len(self.yt_comments_embeddings)} item(s).\n' +
             f'YouTube subscriptions: {len(self.yt_subscribed_embeddings)} item(s).\n' +
             f'YouTube liked videos: {len(self.yt_liked_embeddings)} item(s).\n' +
             f'YouTube watch history: {len(self.yt_history_embeddings)} item(s).')

        return {
            'Apps': self.apps_embeddings,
            'Autofill': self.autofill_place_embeddings,
            'Browser History': self.history_embeddings,
            'Chat': self.chats_embeddings,
            'Hangouts': self.messages_embeddings,
            'Travel': self.distance_traveled,
            'Nearby Places': self.nearby_places_embeddings,
            'Email': self.email_embeddings,
            'Movies': self.movies_embeddings,
            'YouTube comments': self.yt_comments_embeddings,
            'YouTube subscriptions': self.yt_subscribed_embeddings,
            'YouTube liked videos': self.yt_liked_embeddings,
            'YouTube watch history': self.yt_history_embeddings
        }
