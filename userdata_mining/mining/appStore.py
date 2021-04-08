import os
import json
import pandas as pd

def parse_tv_data(user, data_path='.'):
    """
    Mines a user's app store clicks. While it is possible to mine the user's
    (or, the people the user is speaking to) data selectively, we do not
    do that distinction here.

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, NOT ending in a /.
    :return {list} user messages
    """
    # Does the directory exist?
    path = f'{data_path}/data/{user}/AppStoreClickActivity.xlsx'
    if not os.path.exists(path):
        return []

    data = pd.read_excel(path, sheet_name=0, header=1)

    item = data['Item Descriptions'].dropna()
    pageDescription = data['Page Details'].dropna()
    return item, pageDescription

print(parse_tv_data('madison', '../..'))