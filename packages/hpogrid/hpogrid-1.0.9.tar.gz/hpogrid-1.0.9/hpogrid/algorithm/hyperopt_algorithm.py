import ray
from ray.tune.suggest.hyperopt import HyperOptSearch

from hpogrid.search_space.hyperopt_space import HyperOptSpace

class HyperOptAlgoWrapper():
    def __init__(self):
        self.algorithm = None
    def create(self, metric, mode, search_space, **args):
        search_space = HyperOptSpace(search_space).search_space
        self.algorithm = HyperOptSearch(
            search_space,
            metric=metric,
            mode=mode, **args)
        return self.algorithm