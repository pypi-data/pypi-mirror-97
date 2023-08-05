from hpogrid.configuration import ConfigurationBase
from hpogrid.components.defaults import (kSearchAlgorithms, kSchedulers, 
                                         kMetricMode, kDefaultSearchAlgorithm,
                                         kDefaultScheduler, kDefaultMetric,
                                         kDefaultMetricMode, kDefaultMaxConcurrent)

class HPOConfiguration(ConfigurationBase):
    _CONFIG_TYPE_ = 'hpo_config'
    _CONFIG_DISPLAY_NAME_ = 'HPO'
    _DESCRIPTION_ = 'Manage configuration for hyperparameter optimization'
    _LIST_COLUMNS_ = ['HPO Configuration']
    _CONFIG_FORMAT_ = \
        {
            'algorithm': {
                'abbr': 'a',
                'description': 'Algorithm for hyperparameter optimization',
                'required': False,
                'type': str,
                'choice': kSearchAlgorithms,
                'default': kDefaultSearchAlgorithm
            },
            'scheduler': {
                'abbr': 's',
                'description': 'Trial scheduling method for hyperparameter optimization',
                'required': False,
                'type': str,
                'choice': kSchedulers,
                'default': kDefaultScheduler
            },        
            'metric' : {
                'abbr': 'm',
                'description': 'Evaluation metric to be optimized',
                'required': False,
                'type': str,
                'default': kDefaultMetric
            },
            'extra_metrics': {
                'abbr': 'e',
                'description': 'Additional metrics to be saved during the training',
                'required': False,
                'type': (list, type(None)),
                'default': None
            },
            'mode' : {
                'abbr': 'o',
                'description': 'Mode of optimization (either "min" or "max")',
                'required': False,
                'type': str,
                'choice': kMetricMode,
                'default': kDefaultMetricMode
            },
            'resource': {
                'abbr': 'r',
                'description': 'Resource allocated to each trial',
                'required': False,
                'type': (dict, type(None)),
                'default': None
            },
            'num_trials': {
                'abbr': 'n',
                'description': 'Number of trials (search points)',
                'required': True,
                'type': int,
            },
            'log_dir': {
                'abbr': 'l',
                'description': 'Logging directory',
                'required': False,
                'type': (str, type(None)),
                'default': None
            },
            'verbose': {
                'abbr': 'v',
                'description': 'Verbosity level of Ray Tune',
                'required': False,
                'type': int,
                'default': 0
            },
            'max_concurrent': {
                'abbr': 'c',
                'description': 'Maximum number of trials to be run concurrently',
                'required': False,
                'type': int,
                'default': kDefaultMaxConcurrent
            },
            'stop': {
                'abbr': None,
                'description': 'Stopping criteria for the training',
                'required': False,
                'type': dict,
                'default': {'training_iteration': 1}
            },
            'scheduler_param': {
                'abbr': None,
                'description': 'Extra parameters given to the trial scheduler',
                'required': False,
                'type': (dict, type(None)),
                'default': None
            },
            'algorithm_param': {
                'abbr': None,
                'description': 'Extra parameters given to the hyperparameter optimization algorithm',
                'required': False,
                'type': (dict, type(None)),
                'default': None
            }       
        }