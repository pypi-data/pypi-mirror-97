import copy
from typing import List, Dict

from ax.service.ax_client import AxClient

from hpogrid.generator.base_generator import Generator
from hpogrid.search_space.ax_space import AxSpace

class AxGenerator(Generator):
    def get_searcher(self, search_space:Dict, metric:str, mode:str, **args):
        ax_client = AxClient(enforce_sequential_optimization=False, verbose_logging=False)
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
        return ax_client

    def tell(self, point:Dict, value):
        value = self._to_metric_values(value)
        _, trial_index = self.searcher.attach_trial(point)
        metric_dict = { self.metric: (value, 0.0)}
        self.searcher.complete_trial(
            trial_index=trial_index, raw_data=metric_dict)

    def ask(self, n_points:int =None):
        points = []
        for _ in range(n_points):
            point, trial_index = self.searcher.get_next_trial()
            trial = self.searcher._get_trial(trial_index=trial_index)
            trial.mark_abandoned()
            points.append(copy.deepcopy(point))
        return points