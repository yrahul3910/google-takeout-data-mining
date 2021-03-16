import xml
import datetime

import googlemaps
import numpy as np

from utils import get_key
from maps import parse_maps_data
from fit import parse_fit_data


def parse_user_data(user):
    fit_data = parse_fit_data(user)
    maps_data = parse_maps_data(user)

    return {
        'maps': maps_data,
        'fit': fit_data
    }


if __name__ == '__main__':
    print(parse_maps_data('rahul'))
