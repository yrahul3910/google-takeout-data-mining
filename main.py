import googlemaps
import numpy as np
from userdata_mining.utils import get_key
from userdata_mining.mining import *
from userdata_mining.visualization import EmbeddingVisualizer


if __name__ == '__main__':
    miner = GoogleDataMiner(user='rahul', data_path='.')
    embeddings = miner.mine_data()

    keys = list(embeddings.keys())
    keys.remove('Travel')
    embeddings = [np.array(embeddings[x]) for x in keys]

    viz = EmbeddingVisualizer()
    viz.visualize(*embeddings, dpi=150)
