import copy
from typing import List, Dict

from hpbandster.optimizers.config_generators.bohb import BOHB

from hpogrid.generator.base_generator import Generator
from hpogrid.search_space.bohb_space import BOHBSpace

default_budget = 100

class BOHBResultWrapper():
    def __init__(self, config, loss, budget=default_budget):
        self.result = {"loss": loss}
        self.kwargs = {"budget": budget, "config": config.copy()}
        self.exception = None

class BOHBGenerator(Generator):

    def get_searcher(self, search_space:Dict, metric:str, mode:str, **args):
        search_space = BOHBSpace(search_space).get_search_space()
        searcher = BOHB(search_space)
        return searcher

    def ask(self, n_points:int = None):
        points = []
        for _ in range(n_points):
            point, info = self.searcher.get_config(None)
            points.append(copy.deepcopy(point))
        return points

    def tell(self, point:Dict, value):
        value = self._to_metric_values(value)
        result = BOHBResultWrapper(point, self.signature * value)
        self.searcher.new_result(result)



