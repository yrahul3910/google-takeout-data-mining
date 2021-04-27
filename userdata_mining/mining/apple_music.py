import os
import json
import pandas as pd


def parse_tv_data(user, data_path='.'):
    """
    Mines a user's app store clicks. 

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} user messages
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/Apple Music Play Activity.xlsx'
    if not os.path.exists(path):
        return []

    data = pd.read_excel(path, sheet_name=0, header=1)

    item = data['Artist Name'].dropna()
    pageDescription = data['Content Name'].dropna()
    return item, pageDescription
