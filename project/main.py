import googlemaps
import numpy as np
from userdata_mining.utils import get_key
from userdata_mining.mining import parse_maps_data
from userdata_mining.mining import parse_fit_data


def parse_user_data(user):
    fit_data = parse_fit_data(user)
    maps_data = parse_maps_data(user)

    return {
        'maps': maps_data,
        'fit': fit_data
    }


if __name__ == '__main__':
    print(parse_user_data('rahul'))
