import ray

from ray.tune.schedulers import AsyncHyperBandScheduler

# use with
# ax
# tune
# hyperopt
class AsyncHyperBandSchedulerWrapper():
    def __init__(self):
        self.scheduler = None
    def create(self, metric, mode, **args):
        self.scheduler = AsyncHyperBandScheduler(metric=metric, mode=mode, **args)
        return self.scheduler
