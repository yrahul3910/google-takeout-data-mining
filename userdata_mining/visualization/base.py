from abc import ABC


class Visualizer(ABC):
    """
    A base class for visualization classes that provides
    an interface of standard methods to work with.
    """

    def __init__(self, *args, **kwargs):
        pass

    def visualize(self, *args, **fig_kwargs):
        """
        Visualizes the passed parameters.

        :param *args - Arguments passed to the visualization object
        :param *fig_kwargs - Arguments passed to matplotlib.figure
        """
        pass
