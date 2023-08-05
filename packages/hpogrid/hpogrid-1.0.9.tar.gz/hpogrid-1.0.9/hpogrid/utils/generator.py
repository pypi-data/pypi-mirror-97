from abc import ABC
from typing import List, Union
import argparse
import copy
from functools import partial

from hpogrid import algorithm as algo
from hpogrid import search_space as space

class Generator(ABC):
    def __init__(self, search_space, metric, mode, **args):
        self.evaluated_points = []
        self.metric = metric
        self.mode = mode
        self.search_space = search_space
        if mode == "max":
            self.signature = -1.
        elif mode == "min":
            self.signature = 1.
        self.searcher = self.get_searcher(search_space, metric, mode, **args)

    @abstractmethod    
    def get_searcher(self, search_space, metric, mode, **args):
        pass

    @abstractmethod    
    def tell(self, point, result):
        pass

    def feed(self, points:List, results:List, redo=False):
        if redo:
            self.clear_history()
        for point, result in zip(points, results):
            self.tell(point, result)

    @abstractmethod    
    def ask(self, n_points:int =None):
        pass

    @abstractmethod  
    def clear_history(self):
        pass


class NeverGradGenerator(Generator):
    def __init__(self, search_space, metric, mode):
        self.reset()

    def get_searcher(self, search_space, metric, mode, **args):
        from algo.nevergrad_algorithm import NeverGradAlgoWrapper
        return NeverGradAlgoWrapper(metric, mode, search_space, **args)

    def tell(self, point, value):


class HyperOptGenerator(Generator):
    def get_searcher(self, search_space, metric, mode, **args):
        import hyperopt as hpo
        from hyperopt.fmin import generate_trials_to_calculate
        searcher = hpo.tpe.suggest
        if 'gamma' in args:
            searcher = partial(searcher, gamma=gamma)
        from hpogrid.search_space.hyperopt_space import HyperOptSpace
        hyperopt_space = HyperOptSpace(search_space).get_search_space()
        self.domain = hpo.Domain(lambda spc: spc, hyperopt_space)
        self.trials = hpo.Trials()
        self.rstate = np.random.RandomState()
        return searcher


    def ask(self, n_points:int =None):
        points = []
        trial_ids = self.trials.new_trial_ids(n_points)
        self.trials.refresh()
        new_trials = self.searcher(trial_ids, self.domain, self.trials,
            self.rstate.randint(2**31 - 1))
        for trial in new_trials:
            config = hpo.base.spec_from_misc(trial["misc"])
            memo = self.domain.memo_from_config(config)
            point = hpo.pyll.rec_eval(self.domain.expr, memo=memo)
            points.append(copy.deepcopy(point))
        return points

    def clear_history(self):
        self.trials.delete_all()

    def tell(self, point, value):
        fake_trial = generate_trials_to_calculate([point])
        fake_trial.refresh()
        trial = fake_trial._trials[0]
        trial['state'] = hpo.base.JOB_STATE_DONE
        trial['result'] = {"loss": self.signature * value, "status": "ok"}
        self.trials.insert_trial_doc(trial)
        self.trials.refresh()

        
class SkOptGenerator(Generator):
    def get_searcher(self, search_space, metric, mode, **args):
        from ax.service.ax_client import AxClient
        ax_client = AxClient(enforce_sequential_optimization=False, verbose_logging=False)
        from hpogrid.search_space.ax_space import AxSpace
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

class AxGenerator(Generator):
    def get_searcher(self, search_space, metric, mode):
        from ax.service.ax_client import AxClient
        ax_client = AxClient(enforce_sequential_optimization=False, verbose_logging=False)
        from hpogrid.search_space.ax_space import AxSpace
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

    def tell(self, point, value):
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
            points.append(point)
        return points

    def clear_history(self):
        self.searcher = self.get_searcher(self.search_space, self.metric, self.mode)