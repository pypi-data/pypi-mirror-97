import nevergrad as ng

import ray
from ray.tune.suggest.nevergrad import NevergradSearch

from hpogrid.search_space.nevergrad_space import NeverGradSpace

class NeverGradAlgoWrapper():
    
    def __init__(self):
        self.algorithm = None
        self.default_method = 'RandomSearch'
        self.default_budget = 100

    def create(self, metric, mode, search_space, **args):
        search_space = NeverGradSpace(search_space).get_search_space()
        method = args.pop('method', self.default_method)
        optimizer = ng.optimizers.registry[method](
                parametrization=search_space, budget=self.default_budget)
        self.algorithm = NevergradSearch(optimizer, None, metric=metric, mode=mode, **args)
        return self.algorithm