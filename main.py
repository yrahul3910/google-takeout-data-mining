import googlemaps
import numpy as np
from userdata_mining.utils import get_key
from userdata_mining.mining import *


if __name__ == '__main__':
    miner = GoogleDataMiner(user='rahul', data_path='.')
    miner.mine_data()
