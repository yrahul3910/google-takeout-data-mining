import glob
import csv
import os
from userdata_mining.utils import warn


def parse_pay_data(user, data_path='.'):
    """
    Parse the Google Pay purchase data of the user.

    Args:
        user (str): The user to parse.
        data_path (str): The path to the data.

    Returns:
        list: A list of Google Pay purchase descriptions.
    """
    # First, check for cache
    if os.path.exists(f'{data_path}/saved/embeddings/pay.pickle'):
        return None

    path = f'{data_path}/data/{user}/Takeout/Google Pay/Google transactions/transactions_*.csv'

    # Does the directory exist?
    if not os.path.exists(path):
        warn('Google Pay data path does not exist.')
        return []

    transaction_descriptions = []
    for file in glob.glob(f'{path}'):
        with open(file, 'r') as f:
            read = csv.reader(f)
            for r in read:
                if r is not None and len(r) > 0 and r[2] != '' and r[2] != 'Description':
                    transaction_descriptions.append(r[2])

    transaction_descriptions = set(transaction_descriptions)
    return transaction_descriptions
