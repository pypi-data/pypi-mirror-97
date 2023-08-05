import os
from ray.tune import Trainable

from hpogrid.components import environment_settings as es

class CustomModel(Trainable):
    
    def initialize(self, config):
        raise NotImplementedError('The "initialize" method must be overriden for initializing the train model.')
        
    def setup(self, config):
        workdir = es.get_workdir()
        os.chdir(workdir)
        self.initialize(config)