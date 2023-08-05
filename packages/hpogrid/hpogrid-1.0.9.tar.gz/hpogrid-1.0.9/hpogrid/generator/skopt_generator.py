import copy
from typing import List, Dict

from skopt import Optimizer

from hpogrid.generator.base_generator import Generator
from hpogrid.search_space.skopt_space import SkOptSpace

#default_method = "GP"
#methods = ["GP", "RF", "ET", "GBRT"]

class SkOptGenerator(Generator):
    def get_searcher(self, search_space:Dict, metric:str, mode:str, **args):
        search_space = SkOptSpace(search_space).get_search_space()
        searcher = Optimizer(search_space)
        self.labels = [hp.name for hp in search_space]
        return searcher

    def ask(self, n_points:int = None):
        points = []
        for _ in range(n_points):
            point = self.searcher.ask()
            point = dict(zip(self.labels, point))
            points.append(copy.deepcopy(point))
        return points

    def tell(self, point:Dict, value):
        value = self._to_metric_values(value)
        self.searcher.tell(point, self.signature * value)
