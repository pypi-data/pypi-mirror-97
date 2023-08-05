import os
import sys
import json
import time
import argparse
import tempfile
import importlib
from typing import Optional, Dict, List
from datetime import datetime

import numpy as np

import ray
from ray import tune

import hpogrid
from hpogrid.utils.cli_parser import CLIParser
from hpogrid.components.defaults import *
from hpogrid.utils import helper
from hpogrid.idds_interface import idds_utils


class JobBuilder():
    
    _USAGE_ = 'hpogrid run [<args>]'
    _DESCRIPTION_ = 'Run hyperparameter optimization from a project/configuration file'    
    
    def __init__(self, parser=False):
        self.reset()
        
    def get_parser(self, **kwargs):
        parser = CLIParser(description=self._DESCRIPTION_,
                           usage=self._USAGE_, **kwargs)    
        parser.add_argument('config_input', help='Name of project/configuration file')  
        parser.add_argument('-p', '--search_points', help='A json file containing the manual'
                            ' search points to run', default=None)    
        parser.add_argument('-m', '--mode',  help='Platform for running hyperparameter'
                            ' optimization. Choose from "local", "grid", "idds"',
                            choices=['local', 'grid', 'idds'],
                            default='local')   
        return parser
    
    def run_parser(self, args=None):
        parser = self.get_parser()
        args = vars(parser.parse_args(args))
        self.load(**args)
        self.run()
        
    @property
    def algorithm(self) -> str:
        return self._algorithm
    
    @algorithm.setter
    def algorithm(self, name):
        if name and (name not in kSearchAlgorithms):
            raise ValueError('unrecognized search algorithm: {}'.format(name))
        self._algorithm = kAlgoMap.get(name, name)
    
    @property
    def scheduler(self) -> str:
        return self._scheduler
    
    @scheduler.setter
    def scheduler(self, name):
        if name and (name not in kSchedulers):
            raise ValueError('unrecognized trial scheduler: {}'.format(name))
        self._scheduler = name
        

    @property
    def mode(self) -> str:
        return self._mode
    
    @mode.setter
    def mode(self, value):
        if value not in kMetricMode:
            raise ValueError('metric mode must be either "min" or "max"')
        self._mode = value
    
    @property
    def resource(self):
        return self._resource
    
    @property
    def resource_per_trial(self):
        return self._resource_per_trial
    
    @resource_per_trial.setter
    def resource_per_trial(self, value):
        resource = JobBuilder.get_resource_info()
        resource_per_trial = {}
        num_trials = self.num_trials if self.num_trials != -1 else max(resource['gpu'], 1)
        max_concurrent = min(num_trials, self.max_concurrent)
        for device in ['cpu', 'gpu']:
            n_device = resource[device]
            if n_device >= self.max_concurrent:
                resource_per_trial[device] = int(n_device/max_concurrent)  
            elif n_device > 0:
                resource_per_trial[device] = n_device/max_concurrent
            else:
                resource_per_trial[device] = 0
                
        if isinstance(value, dict):
            for device in ['cpu', 'gpu']:
                if device in value and value[device]:
                    resource_per_trial[device] = min(value[device], resource_per_trial[device])
        print('INFO: Each trial will use {} GPU(s) resource'.format(resource_per_trial['gpu']))
        print('INFO: Each trial will use {} CPU(s) resource'.format(resource_per_trial['cpu']))
        self._resource_per_trial = resource_per_trial
        self._resource = resource
    
    @property
    def algorithm_param(self):
        return self._algorithm_param
    @property
    def scheduler_param(self):
        return self._scheduler_param
    
    @algorithm_param.setter
    def algorithm_param(self, val):
        self._algorithm_param = val if val is not None else {}
            
    @scheduler_param.setter
    def scheduler_param(self, val):
        self._scheduler_param = val if val is not None else {}
        
    @property
    def stop(self):
        return self._stop
    
    @stop.setter
    def stop(self, val):
        self._stop = val if val is not None else {}
        
    @property
    def df(self) -> 'pandas.DataFrame':
        return self._df
    
    @property
    def start_datetime(self) -> str:
        return self._start_datetime
    
    @property
    def end_datetime(self) -> str:
        return self._end_datetime
    
    @property
    def start_timestamp(self) -> float:
        return self._start_timestamp
    
    @property
    def total_time(self) -> float:
        return self._total_time
    
    @property
    def best_config(self) -> Dict:
        return self._best_config

    @property
    def hyperparameters(self):
        return self._hyperparameters
    
    @property
    def log_dir(self) -> str:
        return self._log_dir

    @log_dir.setter
    def log_dir(self, val):
        """
        self._log_dir = val
        if hpogrid.is_local_job() and (not os.path.isabs(val)):
            project_path = helper.get_project_path(self.project_name)
            if os.path.exists(project_path):
                self._log_dir = os.path.join(project_path, val)
        self._log_dir = helper.pretty_path(self._log_dir)
        """
        self._log_dir = val
            
        
            
    def reset(self):
        self.project_name = None
        # model configuration
        self.model_script = None
        self.model_name = None
        self.model_param = kDefaultModelParam  
        # search space
        self.search_space = {}
        # hpo configuration
        self._algorithm = None
        self.metric = None
        self._mode = None
        self._scheduler = None  
        self.algorithm_param = kDefaultAlgorithmParam        
        self.scheduler_param = kDefaultSchedulerParam
        self.num_trials = None
        self.max_concurrent = kDefaultMaxConcurrent
        self.verbose = False
        self._log_dir = kDefaultLogDir
        self.stop = kDefaultStopping
        self._resource = None
        self.extra_metrics = None
        # parameters for logging
        self._df = None
        self._start_datetime = None
        self._end_datetime = None
        self._total_time = None
        self._best_config = None
        self._hyperparameters = {}
        self._start_timestamp = None
        self.idds_job = False
        self.scripts_path = os.getcwd()
        self.search_points = None
        self.summary_fname = kGridSiteMetadataFileName
        self._resource = {"cpu": 0, "gpu": 0}

        
    @staticmethod
    def get_scheduler(name, metric, mode, search_space = None, **args):
        if (name == None) or (name == 'None'):
            return None
        elif name == 'asynchyperband':
            from hpogrid.scheduler.asynchyperband_scheduler import AsyncHyperBandSchedulerWrapper
            return AsyncHyperBandSchedulerWrapper().create(metric, mode, **args)
        elif name == 'bohbhyperband':
            from hpogrid.scheduler.bohbhyperband_scheduler import BOHBHyperBandSchedulerWrapper
            return BOHBHyperBandSchedulerWrapper().create(metric, mode, **args)
        elif name == 'pbt':
            from hpogrid.scheduler.pbt_scheduler import PBTSchedulerWrapper
            if search_space is None:
                raise ValueError('Missing search space definition for pbt scheduler')
            return PBTSchedulerWrapper().create(metric, mode, search_space, **args)

    @staticmethod
    def get_search_space(base_search_space, algorithm):
        if base_search_space is None:
            raise ValueError('search space can not be empty')    
        if algorithm == 'ax':
            from hpogrid.search_space.ax_space import AxSpace
            return AxSpace(base_search_space).get_search_space()
        elif algorithm == 'bohb':
            from hpogrid.search_space.bohb_space import BOHBSpace
            return BOHBSpace(base_search_space).get_search_space()
        elif algorithm == 'hyperopt':
            from hpogrid.search_space.hyperopt_space import HyperOptSpace
            return HyperOptSpace(base_search_space).get_search_space()
        elif algorithm == 'skopt':
            from hpogrid.search_space.skopt_space import SkOptSpace
            return SkOptSpace(base_search_space).get_search_space()
        elif algorithm == 'tune':
            from hpogrid.search_space.tune_space import TuneSpace
            return TuneSpace(base_search_space).get_search_space()
        elif algorithm == 'nevergrad':
            from hpogrid.search_space.nevergrad_space import NeverGradSpace
            return NeverGradSpace(base_search_space).get_search_space() 
        else:
            raise ValueError('Unrecognized search algorithm: {}'.format(name))

    @staticmethod
    def get_algorithm(name, metric, mode, base_search_space, max_concurrent=None, **args):
        if name == 'ax':
            from hpogrid.algorithm.ax_algorithm import AxAlgoWrapper
            algorithm = AxAlgoWrapper().create(metric, mode, base_search_space, **args)
        elif name == 'bohb':
            from hpogrid.algorithm.bohb_algorithm import BOHBAlgoWrapper
            algorithm = BOHBAlgoWrapper().create(metric, mode, base_search_space, **args)
        elif name == 'hyperopt':
            from hpogrid.algorithm.hyperopt_algorithm import HyperOptAlgoWrapper
            algorithm = HyperOptAlgoWrapper().create(metric, mode, base_search_space, **args)
        elif name == 'skopt':
            from hpogrid.algorithm.skopt_algorithm import SkOptAlgoWrapper
            algorithm = SkOptAlgoWrapper().create(metric, mode, base_search_space, **args)
        elif name == 'nevergrad':
            from hpogrid.algorithm.nevergrad_algorithm import NeverGradAlgoWrapper
            algorithm = NeverGradAlgoWrapper().create(metric, mode, base_search_space, **args)
        elif name == 'tune':
            algorithm = None
        else:
            raise ValueError('Unrecognized search algorithm: {}'.format(name))
        # limit max concurrency
        if algorithm and max_concurrent:
            from ray.tune.suggest import ConcurrencyLimiter
            algorithm = ConcurrencyLimiter(algorithm, max_concurrent=max_concurrent) 
        return algorithm

    @staticmethod
    def get_model(script_name, model_name, scripts_path=None):
        scripts_path = os.getcwd() if scripts_path is None else scripts_path
        model = None
        script_name_noext = os.path.splitext(script_name)[0]
        try: 
            helper.set_scripts_path(scripts_path)
            module = importlib.import_module(script_name_noext)
            model = getattr(module, model_name)
        except: 
            raise ImportError('Unable to import function/class {} '
                'from training script: {}.py'.format(model_name, script_name_noext))
        finally:
            helper.set_scripts_path(scripts_path, undo=True)
        print('INFO: Loaded module {}'.format(model.__name__))
        return model

    def create_metadata(self, df) -> Dict:

        summary = {
            'project_name' : self.project_name,
            'start_datetime': self.start_datetime,
            'end_datetime': self.end_datetime,
            'start_timestamp': self.start_timestamp,
            'task_time_s' : self.total_time,
            'hyperparameters': self.hyperparameters,
            'metric': self.metric,
            'mode' : self.mode,
            'best_config' : self.best_config, 
        }
        
        rename_cols = { 'config/{}'.format(hp): hp for hp in self.hyperparameters}
        rename_cols['time_total_s'] = 'time_s'
        
        df = df.rename(columns=rename_cols)
        cols_to_save = ['time_s'] + self.hyperparameters
        if 'metric' in summary:
            cols_to_save.append(summary['metric'])
        if self.extra_metrics:
            cols_to_save += self.extra_metrics
        df = df.filter(cols_to_save, axis=1).transpose()
        summary['result'] = df.to_dict()
        
        return summary

    @staticmethod
    def get_resource_info() -> Dict:
        resource = {}
        n_gpu = helper.get_n_gpu()
        n_cpu = helper.get_n_cpu()
        print('INFO: Number of GPUs detected: ',n_gpu)
        print('INFO: Number of CPUs detected: ',n_cpu)
        resource['gpu'] = n_gpu
        resource['cpu'] = n_cpu
        return resource
    
    def run(self) -> None:
            
        self._start_timestamp = start = time.time()
        self._start_datetime = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

        # get model parameters
        if self.algorithm == 'tune':
            tune_config_space = self.get_search_space(self.search_space, algorithm='tune')
        else:
            tune_config_space = {}

        tune_config_space.update(self.model_param)

        # get search algorithm
        algorithm = self.get_algorithm(
            self.algorithm,
            self.metric,
            self.mode,
            self.search_space,
            self.max_concurrent,
            **self.algorithm_param)
        
        # get trial scheduler
        scheduler = self.get_scheduler(
            self.scheduler,
            self.metric,
            self.mode,
            self.search_space,
            **self.scheduler_param)
        
        # get model
        model = self.get_model(self.model_script, self.model_name, self.scripts_path)
        
        loggers = None
        #loggers = self.get_loggers()
        
        # save something to prevent looping job
        with open(kGridSiteMetadataFileName,'w') as output:
            json.dump({}, output)
        
        temp_dir = tempfile.TemporaryDirectory()
        # HPO starts
        try:
            
            # extract input dataset if it is a tar file
            # (for grid jobs only)
            extracted_files = []
            if hpogrid.is_grid_job():
                datadir = hpogrid.get_datadir()
                extracted_files = helper.extract_tarball(datadir, datadir)
                
            ray.init(include_dashboard=False)
#           lru_evict=True      
            if not self.log_dir:
                local_dir = os.path.join(temp_dir.name, 'log')
            else:
                local_dir = self.log_dir
            if self.num_trials == -1:
                num_samples = max(self.resource.get('gpu'), 1)
            else:
                num_samples = self.num_trials
            analysis = tune.run(
                model,
                name=self.project_name,
                scheduler=scheduler,
                search_alg=algorithm,
                config=tune_config_space,
                num_samples=num_samples,
                resources_per_trial=self.resource_per_trial,
                verbose=self.verbose,
                local_dir=local_dir,
                loggers=loggers,
                stop=self.stop)
#                sync_to_driver=False,
#                global_checkpoint_period=np.inf)
        finally:
            ray.shutdown()
            # remove the extracted tar files
            helper.remove_files(extracted_files)
        
        end = time.time()
        self._total_time = float(end-start)
        self._end_datetime = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

        self._best_config = analysis.get_best_config(metric=self.metric, mode=self.mode)
        
        print("Best config: ", self.best_config)
        print("Time taken in seconds: ", self.total_time)
        
        if self.log_dir:
            print("INFO: Ray Tune log files are saved at {}".format(self.log_dir))

        df = analysis.dataframe(metric=self.metric, mode=self.mode)

        metadata = self.create_metadata(df)
        
        summary_output_path = helper.pretty_path(self.summary_fname)
        # save metadata
        with open(summary_output_path, 'w') as output:
            print('INFO: Job metadata is saved at {}'.format(summary_output_path))
            json.dump(metadata, output, cls=helper.NpEncoder)
        
        # save idds output
        if hpogrid.is_idds_job():
            idds_utils.save_idds_output_from_metadata(metadata)

        # reset environment
        hpogrid.reset()
        temp_dir.cleanup()
    
    def get_loggers(self):
        from ray.tune.logger import NoopLogger, MLFLowLogger
        return [NoopLogger, MLFLowLogger]
    
    def setup(self, mode='local'):
        hpogrid.setup(mode)
        
    def load(self, config_input: [Dict, str], search_points=None, mode='local'):
        
        self.reset()
        self.setup(mode)

        input_as_project = helper.is_project(config_input)
        config = helper.load_configuration(config_input)

        # if input is a project name, set scripts path to 
        # where the scripts are stored in the project directory
        # if input is a configuration file, set scripts path to
        # the scripts path stated in configuration file
        if input_as_project:
            scripts_path = helper.get_scripts_path(config_input)
        else:
            scripts_path = helper.pretty_dirname(config['scripts_path'])
   
        self.project_name = config['project_name']
        self.scripts_path = scripts_path
        
        # Load search space
        self.search_space = config['search_space']

        # Load hpo configuration
        self.algorithm = config['hpo_config']['algorithm']
        self.metric = config['hpo_config']['metric']
        self.mode = config['hpo_config']['mode']
        self.scheduler = config['hpo_config']['scheduler']
        self.scheduler_param = config['hpo_config']['scheduler_param']
        self.algorithm_param = config['hpo_config']['algorithm_param']
        self.num_trials = config['hpo_config']['num_trials']
        self.max_concurrent = config['hpo_config']['max_concurrent']
        self.verbose = config['hpo_config']['verbose']
        self.log_dir = config['hpo_config'].get('log_dir', None)
        self.stop = config['hpo_config'].get('stop', None)

        self.resource_per_trial = config['hpo_config'].get('resource', None)

        self.extra_metrics = config['hpo_config'].get('extra_metrics', None)
        
        # configuration for idds
        if (not search_points) and hpogrid.is_idds_job():
            search_points = idds_utils.get_search_points()

        if search_points:
            if isinstance(search_points, str):
                with open(search_points, 'r') as f:
                    search_points = json.load(f)
            self.search_points = search_points
            from hpogrid.search_space.skopt_space import SkOptSpace
            skopt_search_points = SkOptSpace.transform(search_points, 
                                      reference=job.search_space)
            self.algorithm = 'skopt'
            self.scheduler = None
            self.scheduler_param = {}
            self.algorithm_param = {'points_to_evaluate': skopt_search_points}
            self.num_trials = len(skopt_search_points)

        # Load model configuration
        self.model_script = config['model_config']['script']
        self.model_name = config['model_config']['model']
        self.model_param = config['model_config']['param']

        self._hyperparameters = list(self.search_space.keys())
    
    @classmethod
    def from_input(cls, config_input: [Dict, str],
                    search_points=None,
                    mode='local'):
        job = JobBuilder()
        job.load(config_input, search_points, mode)
        return job
    
