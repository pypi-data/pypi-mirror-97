from ax.service.ax_client import AxClient

import ray
from ray.tune.suggest.ax import AxSearch

from hpogrid.search_space.ax_space import AxSpace

from pdb import set_trace

class AxAlgoWrapper():
    def __init__(self):
        self.algorithm = None
    def create(self, metric, mode, search_space, **args):
        ax_client = AxClient(enforce_sequential_optimization=False, verbose_logging=True)
        search_space = AxSpace(search_space).get_search_space()

        if mode == 'max':
            minimize = False
        elif mode == 'min':
            minimize = True
        else:
            raise ValueError('mode of evaluation metric can only be "min" or "max"')

        ax_client.create_experiment(
            parameters=search_space,
            objective_name=metric,
            minimize=minimize)

        self.algorithm = AxSearch(ax_client, **args)
        return self.algorithm