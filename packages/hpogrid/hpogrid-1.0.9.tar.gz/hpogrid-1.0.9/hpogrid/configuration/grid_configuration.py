from hpogrid.configuration import ConfigurationBase
from hpogrid.components.defaults import kDefaultContainer, kDefaultOutDS

class GridConfiguration(ConfigurationBase):
    _CONFIG_TYPE_ = 'grid_config'
    _CONFIG_DISPLAY_NAME_ = 'grid'
    _DESCRIPTION_ = 'Manage configuration for grid job submission'
    _LIST_COLUMNS_ = ['Grid Configuration']
    _CONFIG_FORMAT_ = \
        {
            'site': {
                'abbr': 's',
                'description': 'Name of the grid site(s) to where the jobs are submitted',
                'required': False,
                'type': (list, str, type(None)),
                'default': None
            },
            'container': {
                'abbr': 'c',
                'description': 'Name of the docker or singularity container in which the jobs are run',
                'required': False,
                'type': str,
                'default': kDefaultContainer
            },
            'inDS': {
                'abbr': 'i',
                'description': 'Name of (rucio) input dataset', 
                'required': False,
                'type': (str, type(None)),
                'default': None
            },
            'outDS': {
                'abbr': 'o',
                'description': 'Name of output dataset',
                'required': False,
                'type': str,
                'default': kDefaultOutDS
            },            
            'retry': {
                'abbr': 'r',
                'description': 'Check to enable retrying faild jobs',
                'required': False,
                'type': (bool, int),
                'default': 0
            },
            'extra': {
                'abbr': 'e',
                'description': 'extra options passed to panda command',
                'required': False,
                'type': dict,
                'default': {}
            }
        }