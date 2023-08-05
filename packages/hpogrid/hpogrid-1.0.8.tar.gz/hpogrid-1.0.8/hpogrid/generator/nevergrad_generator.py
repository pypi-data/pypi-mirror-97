import copy
from typing import List, Dict

import nevergrad as ng

from hpogrid.generator.base_generator import Generator
from hpogrid.search_space.nevergrad_space import NeverGradSpace

default_budget = 100
default_method = 'RandomSearch'

class NeverGradGenerator(Generator):
    def get_searcher(self, search_space:Dict, metric:str, mode:str, **args):
        search_space = NeverGradSpace(search_space).get_search_space()
        if ('method' in args) and (args['method']):
            method = args['method']
        else:
            method = default_method
        searcher = ng.optimizers.registry[method](
                parametrization=search_space, budget=default_budget)
        return searcher

    def ask(self, n_points:int = None):
        points = []
        for _ in range(n_points):
            point = self.searcher.ask().kwargs
            points.append(copy.deepcopy(point))
        return points

    def tell(self, point:Dict, value):
        value = self._to_metric_values(value)
        self.searcher.suggest(**point)
        candidate = self.searcher.ask()
        self.searcher.tell(candidate, self.signature * value)
