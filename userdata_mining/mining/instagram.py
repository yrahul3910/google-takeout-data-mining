import os
import json


def parse_insta_ads_viewed(user, data_path='.'):
    """
    Mines 

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} ads viewed on Instagram
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/Instagram/ads_and_content/ads_viewed.json'
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = json.load(f)

    titles = []
    # The conversation key only has metadata, skip it.
    advertisers = data['impressions_history_ads_seen']
    for item in advertisers:
        value = item['string_map_data']['Author']['value']
        titles.append(value)
    
    return titles

def parse_insta_music_heard(user, data_path='.'):
    """
    Mines 

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} music you heard in Instagram advertisements
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/Instagram/ads_and_content/music_heard_in_stories.json'
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = json.load(f)

    titles = []
    # The conversation key only has metadata, skip it.
    advertisers = data['impressions_history_music_heard_in_stories']
    for item in advertisers:
        value = item['string_map_data']['Song']['value']
        titles.append(value)
    
    return titles

def parse_insta_videos_watched(user, data_path='.'):
    """
    Mines 

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} videos you watched in Instagram
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/Instagram/ads_and_content/videos_watched.json'
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = json.load(f)

    titles = []
    # The conversation key only has metadata, skip it.
    advertisers = data['impressions_history_videos_watched']
    for item in advertisers:
        value = item['string_map_data']['Author']['value']
        titles.append(value)
    
    return titles

def parse_insta_ads_interest(user, data_path='.'):
    """
    Mines 

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} your ad interest information created by instagarm
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/Instagram/information_about_you/ads_interests.json'
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = json.load(f)

    titles = []
    # The conversation key only has metadata, skip it.
    advertisers = data['inferred_data_ig_interest']
    for item in advertisers:
        value = item['string_map_data']['Interest']['value']
        titles.append(value)
    
    return titles

def parse_insta_your_topics(user, data_path='.'):
    """
    Mines 

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} your topics shortlisted by instagarm
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/Instagram/your_topics/your_topics.json'
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = json.load(f)

    titles = []
    # The conversation key only has metadata, skip it.
    advertisers = data['topics_your_topics']
    for item in advertisers:
        value = item['string_map_data']['Name']['value']
        titles.append(value)
    
    return titles

def parse_insta_your_reels_topics(user, data_path='.'):
    """
    Mines 

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} topics of your most watched reels
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/Instagram/your_topics/your_reels_topics.json'
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = json.load(f)

    titles = []
    # The conversation key only has metadata, skip it.
    advertisers = data['topics_your_reels_topics']
    for item in advertisers:
        value = item['string_map_data']['Name']['value']
        titles.append(value)
    
    return titles

def parse_insta_your_reels_sentiments(user, data_path='.'):
    """
    Mines 

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} list of sentiments based on reels you watched on Instagram
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/Instagram/your_topics/your_reels_topics.json'
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = json.load(f)

    titles = []
    # The conversation key only has metadata, skip it.
    advertisers = data['topics_your_reels_emotions']
    for item in advertisers:
        value = item['string_map_data']['Name']['value']
        titles.append(value)
    
    return titles

def parse_insta_saved_posts(user, data_path='.'):
    """
    Mines 

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} posts you saved in Instagram
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/Instagram/saved/saved_posts.json'
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = json.load(f)

    titles = []
    # The conversation key only has metadata, skip it.
    advertisers = data['saved_saved_media']
    for item in advertisers:
        value = item['string_map_data']['Shared By']['value']
        titles.append(value)
    
    return titles

def parse_insta_account_searches(user, data_path='.'):
    """
    Mines 

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} list of accounts you searched in Instagram
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/Instagram/recent_searches/account_searches.json'
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = json.load(f)

    titles = []
    # The conversation key only has metadata, skip it.
    advertisers = data['searches_user']
    for item in advertisers:
        value = item['string_map_data']['Search']['value']
        titles.append(value)
    
    return titles

def parse_insta_monetization_eligibility(user, data_path='.'):
    """
    Mines 

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} monetization eligibility
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/Instagram/monetization/eligibility.json'
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = json.load(f)

    titles = []
    # The conversation key only has metadata, skip it.
    advertisers = data['monetization_eligibility']
    for item in advertisers:
        value = item['string_map_data']['Product Name']['value']
        titles.append(value)
    
    return titles

def parse_insta_liked_comments(user, data_path='.'):
    """
    Mines 

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} comments you liked in insatgram 
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/Instagram/likes/liked_comments.json'
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = json.load(f)

    titles = []
    # The conversation key only has metadata, skip it.
    advertisers = data['likes_comment_likes']
    for item in advertisers:
        value = item['title']
        titles.append(value)
    
    return titles

def parse_insta_liked_posts(user, data_path='.'):
    """
    Mines 

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} posts you liked in Instagram
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/Instagram/likes/liked_posts.json'
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = json.load(f)

    titles = []
    # The conversation key only has metadata, skip it.
    advertisers = data['likes_media_likes']
    for item in advertisers:
        value = item['title']
        titles.append(value)
    
    return titles

def parse_insta_post_comments(user, data_path='.'):
    """
    Mines 

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} comments you posted on Instagram
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/Instagram/comments/post_comments.json'
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = json.load(f)

    titles = []
    # The conversation key only has metadata, skip it.
    advertisers = data['comments_media_comments']
    for item in advertisers:
        value = item['title']
        titles.append(value)
    
    return titles

def parse_insta_information_submitted(user, data_path='.'):
    """
    Mines 

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} information you have submitted to advertisers in Instagram
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/Instagram/ads_and_businesses/information_you\'ve_submitted_to_advertisers.json'
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = json.load(f)

    titles = []
    # The conversation key only has metadata, skip it.
    advertisers = data['ig_lead_gen_info']
    for item in advertisers:
        value = item['value']
        titles.append(value)
    
    return titles


def parse_insta_posts_viewed(user, data_path='.'):
    """
    Mines 

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} posts viewed on Instagram
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/Instagram/ads_and_content/posts_viewed.json'
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = json.load(f)

    titles = []
    # The conversation key only has metadata, skip it.
    advertisers = data['impressions_history_posts_seen']
    for item in advertisers:
        value = item['string_map_data']['Author']['value']
        titles.append(value)
    
    return titles

def parse_insta_suggested_accounts_viewed(user, data_path='.'):
    """
    Mines 

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} accounts you viewed on Instagram based on Instagram suggestions
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/Instagram/ads_and_content/suggested_accounts_viewed.json'
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = json.load(f)

    titles = []
    # The conversation key only has metadata, skip it.
    advertisers = data['impressions_history_chaining_seen']
    for item in advertisers:
        value = item['string_map_data']['Username']['value']
        titles.append(value)
    
    return titles

def parse_insta_account_based_in(user, data_path='.'):
    """
    Mines 

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} information about you based on insta accounts
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/Instagram/information_about_you/account_based_in.json'
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = json.load(f)

    titles = []
    # The conversation key only has metadata, skip it.
    advertisers = data['inferred_data_primary_location']
    for item in advertisers:
        value = item['string_map_data']['City Name']['value']
        titles.append(value)
    
    return titles

def parse_insta_comments_allowed_from(user, data_path='.'):
    """
    Mines 

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} permission of comments
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/Instagram/comments_settings/comments_allowed_from.json'
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = json.load(f)

    titles = []
    # The conversation key only has metadata, skip it.
    advertisers = data['settings_allow_comments_from']
    for item in advertisers:
        value = item['string_map_data']['Comments Allowed From']['value']
        titles.append(value)
    
    return titles

def parse_insta_use_cross_app_messaging(user, data_path='.'):
    """
    Mines 

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} permissions to use cross app messaging
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/Instagram/comments_settings/use_cross-app_messaging.json'
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = json.load(f)

    titles = []
    # The conversation key only has metadata, skip it.
    advertisers = data['settings_upgraded_to_cross_app_messaging']
    for item in advertisers:
        value = item['string_map_data']['Upgraded To Cross-App Messaging']['value']
        titles.append(value)
    
    return titles

def parse_insta_emoji_sliders(user, data_path='.'):
    """
    Mines 

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} infromation about insta emoji sliders
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/Instagram/story_sticker_interactions/emoji_sliders.json'
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = json.load(f)

    titles = []
    # The conversation key only has metadata, skip it.
    advertisers = data['story_activities_emoji_sliders']
    for item in advertisers:
        value = item['title']
        titles.append(value)
    
    return titles

def parse_insta_polls(user, data_path='.'):
    """
    Mines 

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} insta polls you participated
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/Instagram/story_sticker_interactions/polls.json'
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = json.load(f)

    titles = []
    # The conversation key only has metadata, skip it.
    advertisers = data['story_activities_polls']
    for item in advertisers:
        value = item['title']
        titles.append(value)
    
    return titles

def parse_insta_quizzes(user, data_path='.'):
    """
    Mines 

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} infromation of quizzes you participated in Instagram
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/Instagram/story_sticker_interactions/quizzes.json'
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = json.load(f)

    titles = []
    # The conversation key only has metadata, skip it.
    advertisers = data['story_activities_quizzes']
    for item in advertisers:
        value = item['title']
        titles.append(value)
    
    return titles

def parse_insta_archived_posts(user, data_path='.'):
    """
    Mines 

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} posts you archived in Instagram
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/Instagram/content/archived_posts.json'
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = json.load(f)

    titles = []
    # The conversation key only has metadata, skip it.
    advertisers = data['ig_archived_post_media']
    for item in advertisers:
        value = item['title']
        titles.append(value)
    
    return titles

def parse_insta_stories(user, data_path='.'):
    """
    Mines 

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} stories you posted in Instagram
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/Instagram/content/stories.json'
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = json.load(f)

    titles = []
    # The conversation key only has metadata, skip it.
    advertisers = data['ig_stories']
    for item in advertisers:
        value = item['title']
        titles.append(value)
    
    return titles

def parse_insta_followers(user, data_path='.'):
    """
    Mines 

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} followers of Instagram
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/Instagram/followers_and_following/followers.json'
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = json.load(f)

    titles = []
    # The conversation key only has metadata, skip it.
    advertisers = data['relationships_followers']
    for item in advertisers:
        values = item['string_list_data']
        for value in values:
            title = value['value']
            titles.append(title)
    
    return titles

def parse_insta_following(user, data_path='.'):
    """
    Mines 

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} people and pages following in Instagram
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/Instagram/followers_and_following/following.json'
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = json.load(f)

    titles = []
    # The conversation key only has metadata, skip it.
    advertisers = data['relationships_following']
    for item in advertisers:
        values = item['string_list_data']
        for value in values:
            title = value['value']
            titles.append(title)
    
    return titles



def parse_insta_hide_story_from(user, data_path='.'):
    """
    Mines 

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} list of people you are hiding stories from 
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/Instagram/followers_and_following/hide_story_from.json'
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = json.load(f)

    titles = []
    # The conversation key only has metadata, skip it.
    advertisers = data['relationships_hide_stories_from']
    for item in advertisers:
        values = item['string_list_data']
        for value in values:
            title = value['value']
            titles.append(title)
    
    return titles

def parse_insta_messages(user, data_path='.'):
    """
    Mines 

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} parses entire messages sent and recieved by you thorugh fb chat
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/Instagram/messages/inbox'
    if not os.path.exists(path):
        return []

    users_inbox = os.listdir(path)
    titles = []
    for user in users_inbox:
        file_path = path +"/" + user + "/message_1.json"
        if not os.path.exists(file_path):
            continue
    
        with open(file_path, 'r') as f:
            data = json.load(f)
    
        # The conversation key only has metadata, skip it.
        messages = data['messages']
        for item in messages:
            message = item.get('content')
            if(message is not None):
                titles.append(message)
    return titles
