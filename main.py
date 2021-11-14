import googlemaps
import numpy as np
import pickle
from userdata_mining.utils import get_key
from userdata_mining.mining import *
from userdata_mining.visualization import EmbeddingVisualizer


if __name__ == '__main__':
    # Check for cache
    if os.path.exists('./saved/embeddings/rahul.pickle'):
        with open('./saved/embeddings/rahul.pickle', 'rb') as f:
            embeddings = pickle.load(f)
    else:
        fbminer = FbInstaDataMiner(user='rahul', data_path='.')
        fb_embeddings = fbminer.mine_data()

        # Save embeddings
        with open('./saved/embeddings/rahul.pickle', 'wb') as f:
            pickle.dump(fb_embeddings, f)

        miner = GoogleDataMiner(user='rahul', data_path='.')
        google_embeddings = miner.mine_data()

        # Save embeddings
        with open('./saved/embeddings/rahul.pickle', 'wb') as f:
            pickle.dump(google_embeddings, f)

        # Merge dictionaries
        google_embeddings |= fb_embeddings
        embeddings = google_embeddings

    keys = list(embeddings.keys())
    keys.remove('Travel')
    embeddings = [np.array(embeddings[x]) for x in keys]

    viz = EmbeddingVisualizer()
    viz.visualize(*embeddings, titles=keys, dpi=150)
