from userdata_mining.visualization.base import Visualizer
from userdata_mining.utils import warn, error
from math import sqrt
from ivis import Ivis
import matplotlib.pyplot as plt


class EmbeddingVisualizer(Visualizer):
    """
    Visualizes the embeddings of the data along with an optional reference point.
    """

    def __init__(self, embedding_dims=2):
        """
        Initializes the visualizer.

        :param {int} embedding_dims - Dimensions to embed to.
        """
        if embedding_dims < 1:
            error('embedding_dims must be positive')
            exit(3)
        elif not isinstance(embedding_dims, int):
            error('embedding_dims must be an integer')
            exit(3)
        elif embedding_dims > 2:
            error('embedding_dims must be 1 or 2')
            exit(3)

        self.embedding_dims = embedding_dims

    def _reduce_dims(self, arg):
        """
        Uses ivis to reduce dimensionality to 2.

        :param {Iterable} arg - an array-like object
        :return {np.ndarray} embedded object
        """
        print(arg.shape)
        m = arg.shape[0]
        if m > 200:
            k = int(0.01 * m)
        elif m > 50:
            k = int(0.1 * m)
        elif m > 10:
            k = int(0.2 * m)
        else:
            k = max(int(0.4 * m), m-3)

        ivis = Ivis(embedding_dims=self.embedding_dims, k=k, batch_size=8)
        return ivis.fit_transform(arg)

    def visualize(self, *args, alpha=0.7, reference=None, **fig_kwargs):
        """
        Visualizes the data given.

        :param *args - Arguments passed to the visualization object
        :param alpha - alpha value for scatterplot
        :param reference - Reference point to plot
        :param *fig_kwargs - Arguments passed to matplotlib.figure
        """
        # How many to embed?
        n_vars = len(args)

        if n_vars == 0:
            warn('No args passed to embed.')
            return

        # Get number of rows
        rows = int(sqrt(n_vars))

        # Get plots
        fig, ax = plt.subplots(rows, rows, **fig_kwargs)

        for i, arg in enumerate(args):
            if arg.shape[0] < 10:
                continue
            # Reduce dimensionality to 2.
            x = self._reduce_dims(arg)

            # Reduce reference point to 2 dims
            if reference is not None:
                x_ref = self._reduce_dims(reference)

            row = int(i // 3)
            col = int(i % 3)

            ax[row][col].scatter(x.T[0], x.T[1], c='b', alpha=alpha)

            if reference is not None:
                ax[row][col].scatter(
                    x_ref.T[0], x_ref.T[1], c='r', alpha=alpha)

        plt.show()
