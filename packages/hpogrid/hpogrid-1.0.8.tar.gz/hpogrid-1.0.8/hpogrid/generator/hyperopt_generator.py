import copy
from typing import List, Union
from functools import partial

import numpy as np

import hyperopt as hpo
from hyperopt.fmin import generate_trials_to_calculate

from hpogrid.generator.base_generator import Generator
from hpogrid.search_space.hyperopt_space import HyperOptSpace


class HyperOptGenerator(Generator):
    def get_searcher(self, search_space, metric:str, mode:str, **args):
        searcher = hpo.tpe.suggest
        if 'gamma' in args:
            searcher = partial(searcher, gamma=gamma) 
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

    def tell(self, point, value):
        value = self._to_metric_values(value)
        fake_trial = generate_trials_to_calculate([point])
        fake_trial.refresh()
        trial = fake_trial._trials[0]
        trial['state'] = hpo.base.JOB_STATE_DONE
        trial['result'] = {"loss": self.signature * value, "status": "ok"}
        self.trials.insert_trial_doc(trial)
        self.trials.refresh()

    def clear_history(self):
        self.trials.delete_all()