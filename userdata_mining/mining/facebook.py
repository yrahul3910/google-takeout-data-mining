import os
import json


def parse_fb_advertisers(user, data_path='.'):
    """
    Mines 

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} advertisers who uplaoded a contact list with your information
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/facebook/ads_information/advertisers_who_uploaded_a_contact_list_with_your_information.json'
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = json.load(f)

    # The conversation key only has metadata, skip it.
    advertisers = data['custom_audiences_v2']
    
    return advertisers

def parse_fb_apps_and_websites(user, data_path='.'):
    """
    Mines 

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} apps and websotes of facebook user used
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/facebook/apps_and_websites_off_of_facebook/apps_and_websites.json'
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = json.load(f)

    titles = []
    # The conversation key only has metadata, skip it.
    apps_and_websites = data['installed_apps_v2']
    for item in apps_and_websites:
        titles.append(item['name']) 
    
    return titles

def parse_fb_posts_from_apps_and_websites(user, data_path='.'):
    """
    Mines 

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} posts from apps and websotes of facebook user used
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/facebook/apps_and_websites_off_of_facebook/posts_from_apps_and_websites.json'
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = json.load(f)

    titles = []
    # The conversation key only has metadata, skip it.
    apps_and_websites = data['app_posts_v2']
    for item in apps_and_websites:
        titles.append(item['title']) 
    
    return titles


def parse_fb_your_topics(user, data_path='.'):
    """
    Mines 

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} list of topics you are intrested in
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/facebook/your_topics/your_topics.json'
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = json.load(f)

    # The conversation key only has metadata, skip it.
    advertisers = data['inferred_topics_v2']
    
    return advertisers

def parse_fb_comments(user, data_path='.'):
    """
    Mines 

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} comments you posted on posts
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/facebook/comments_and_reactions/comments.json'
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = json.load(f)

    titles = []
    # The conversation key only has metadata, skip it.
    apps_and_websites = data['comments_v2']
    for item in apps_and_websites:
        data = item.get('data')
        if data is not None:
            for message in data:
                titles.append(message['comment']['comment'])
    return titles

def parse_fb_reactions(user, data_path='.'):
    """
    Mines 

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} reactions on different posts
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/facebook/comments_and_reactions/posts_and_comments.json'
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = json.load(f)

    titles = []
    # The conversation key only has metadata, skip it.
    apps_and_websites = data['reactions_v2']
    for item in apps_and_websites:
        titles.append(item['title'])
    return titles

def parse_fb_search_history(user, data_path='.'):
    """
    Mines 

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} facebook search history
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/facebook/search/your_search_history.json'
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = json.load(f)

    titles = []
    # The conversation key only has metadata, skip it.
    apps_and_websites = data['searches_v2']
    for item in apps_and_websites:
        data1=item.get('data')
        for text in data1:
            titles.append(text['text'])
    return titles

def parse_fb_pages_you_follow(user, data_path='.'):
    """
    Mines 

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} list of pages you follow on FB
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/facebook/pages/pages_you_follow.json'
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = json.load(f)

    titles = []
    # The conversation key only has metadata, skip it.
    apps_and_websites = data['pages_followed_v2']
    for item in apps_and_websites:
        data1=item.get('data')
        for text in data1:
            titles.append(text['name'])
    return titles

def parse_fb_pages_you_liked(user, data_path='.'):
    """
    Mines 

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} pages you liked on FB
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/facebook/pages/pages_you\'ve_liked.json'
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = json.load(f)

    titles = []
    # The conversation key only has metadata, skip it.
    apps_and_websites = data['page_likes_v2']
    for item in apps_and_websites:
        titles.append(item['name'])
    return titles

def parse_fb_ads_interest(user, data_path='.'):
    """
    Mines 

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} List of your ad interests
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/facebook/other_logged_information/ads_interests.json'
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = json.load(f)

    titles = []
    # The conversation key only has metadata, skip it.
    apps_and_websites = data['topics_v2']
    for item in apps_and_websites:
        titles.append(item)
    return titles

def parse_fb_friend_peer_group(user, data_path='.'):
    """
    Mines 

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} list of your friend peer groups
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/facebook/other_logged_information/friend_peer_group.json'
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = json.load(f)

    titles = []
    # The conversation key only has metadata, skip it.
    apps_and_websites = data['friend_peer_group_v2']
    for item in apps_and_websites:
        titles.append(item)
    return titles

def parse_fb_groups_comments(user, data_path='.'):
    """
    Mines 

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} list of fb groups comments
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/facebook/groups/your_comments_in_groups.json'
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = json.load(f)

    titles = []
    # The conversation key only has metadata, skip it.
    apps_and_websites = data['group_comments_v2']
    for item in apps_and_websites:
        titles.append(item['title'])
    return titles

def parse_fb_groups_membership(user, data_path='.'):
    """
    Mines 

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list}list of groups you are member in
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/facebook/groups/your_group_membership_activity.json'
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = json.load(f)

    titles = []
    # The conversation key only has metadata, skip it.
    apps_and_websites = data['groups_joined_v2']
    for item in apps_and_websites:
        titles.append(item['title'])
    return titles

def parse_fb_groups_posts(user, data_path='.'):
    """
    Mines 

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} group posts
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/facebook/groups/your_posts_in_groups.json'
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = json.load(f)

    titles = []
    # The conversation key only has metadata, skip it.
    apps_and_websites = data['group_posts_v2']
    for item in apps_and_websites:
        titles.append(item['title'])
    return titles


def parse_fb_messages(user, data_path='.'):
    """
    Mines 

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} parses entire messages sent and recieved by you thorugh fb chat
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/facebook/messages/inbox'
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
