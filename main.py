import googlemaps
import numpy as np
from userdata_mining.utils import get_key
from userdata_mining.mining import *


def parse_user_data(user):
    fit_data = parse_fit_data(user)
    maps_data = parse_maps_data(user)
    autofill_data = parse_autofill(user)
    browser_data = parse_browser_history(user)
    hangouts_data = parse_hangouts_data(user)
    mail_data = parse_mail_data(user)

    return {
        'maps': maps_data,
        'fit': fit_data,
        'chrome': {
            'autofill': autofill_data,
            'history': browser_data
        },
        'hangouts': hangouts_data,
        'mail': mail_data
    }


if __name__ == '__main__':
    miner = GoogleDataMiner(user='rahul')
    miner.mine_data()
    print(miner)
