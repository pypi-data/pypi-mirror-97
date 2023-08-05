from pdb import set_trace

import ray

from ray.tune.schedulers import PopulationBasedTraining

from search_space.pbt_space import PBTSpace
# use with
# tune

class PBTSchedulerWrapper():
    def __init__(self):
        self.scheduler = None
    def create(self, metric, mode, space, **args):
        search_space = PBTSpace(space).search_space
        self.scheduler = PopulationBasedTraining(
            metric=metric, 
            mode=mode, 
            hyperparam_mutations = search_space,
            **args)
        return self.scheduler
