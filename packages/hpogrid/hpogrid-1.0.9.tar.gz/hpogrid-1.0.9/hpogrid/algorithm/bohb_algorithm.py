import ray
from ray.tune.suggest.bohb import TuneBOHB

from hpogrid.search_space.bohb_space import BOHBSpace


class BOHBAlgoWrapper():
    def __init__(self):
        self.algorithm = None
    def create(self, metric, mode, search_space, **args):
        search_space = BOHBSpace(search_space).search_space
        self.algorithm = TuneBOHB(search_space, metric=metric, mode=mode, **args)
        return self.algorithm
