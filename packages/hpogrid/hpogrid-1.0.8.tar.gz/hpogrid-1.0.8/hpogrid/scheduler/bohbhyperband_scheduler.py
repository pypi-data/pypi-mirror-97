import ray

from ray.tune.schedulers import HyperBandForBOHB

# use with
# bohb

class BOHBHyperBandSchedulerWrapper():
    def __init__(self):
        self.scheduler = None
    def create(self, metric, mode, **args):
        self.scheduler = HyperBandForBOHB(metric=metric, mode=mode, **args)
        return self.scheduler
