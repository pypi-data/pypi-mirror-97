import json
from copy import deepcopy
from json import JSONDecodeError

from hpogrid.configuration import ConfigurationBase

class SearchSpaceConfiguration(ConfigurationBase):
    _CONFIG_TYPE_ = 'search_space'
    _CONFIG_DISPLAY_NAME_ = 'search space'
    _DESCRIPTION_ = 'Manage configuration for hyperparameter search space'
    _LIST_COLUMNS_ = ['Search Space Configuration']
    _CONFIG_FORMAT_ = \
        {
            'search_space': {
                'abbr': 's',
                'description': 'A json decodable string defining the search space',
                'required': True,
                'type': dict,
            }
        }
    
    _SEARCH_SPACE_FORMAT_ = \
        {
            'categorical': {
                'categories' : { 'type': list, 'required': True},
                'grid_search' : { 'type': int, 'required': False, 'default': 0}
            },
            'uniform': {
                'low': { 'type': (float, int), 'required': True},
                'high': { 'type': (float, int), 'required': True}
            },
            'uniformint': {
                'low': { 'type': int, 'required': True},
                'high': { 'type': int, 'required': True}
            },
            'quniform': {
                'low': { 'type': (float, int), 'required': True},
                'high': { 'type': (float, int), 'required': True},
                'q': { 'type': (float, int), 'required': True}
            },
            'loguniform': {
                'low': { 'type': (float, int), 'required': True},
                'high': { 'type': (float, int), 'required': True},
                'base': { 'type': (float, int), 'required': False}
            },
            'qloguniform': {
                'low': { 'type': (float, int), 'required': True},
                'high': { 'type': (float, int), 'required': True},
                'q': { 'type': (float, int), 'required': True},
                'base': { 'type': (float, int), 'required': False}
            },
            'normal': {
                'mu': { 'type': (float, int), 'required': True},
                'sigma': { 'type': (float, int), 'required': True}
            },
            'qnormal': {
                'mu': { 'type': (float, int), 'required': True},
                'sigma': { 'type': (float, int), 'required': True},
                'q': { 'type': (float, int), 'required': True}
            },
            'lognormal': {
                'mu': { 'type': (float, int), 'required': True},
                'sigma': { 'type': (float, int), 'required': True},
                'base': { 'type': (float, int), 'required': False}
            },
            'qlognormal': {
                'mu': { 'type': (float, int), 'required': True},
                'sigma': { 'type': (float, int), 'required': True},
                'base': { 'type': (float, int), 'required': False},
                'q': { 'type': (float, int), 'required': True}
            },
            'fixed': {
                'value': { 'type': None, 'required': True}
            }
        }
    
    @classmethod
    def validate(cls, config):
        if 'search_space' in config:
            search_space = deepcopy(config['search_space'])
        else:
            search_space = config
        # if attribute type is dict, parse string input as dict
        if isinstance(search_space, str):
            try:
                search_space = json.loads(search_space)
            except JSONDecodeError:
                raise RuntimeError('ERROR: Cannot decode the value of "search_space" as dictionary.'
                    'Please check your input.')        
        config_format = cls._SEARCH_SPACE_FORMAT_
        sampling_methods = config_format.keys()
        kHPKeys = set(['method', 'dimension'])
        for hp in search_space:
            if (not isinstance(search_space[hp], dict)) or (set(search_space[hp].keys()) != kHPKeys):
                raise ValueError('Each hyperparameter must be defined by a dictionary containing the keys "method" and "dimension"')
            if not isinstance(search_space[hp]['dimension'], dict):
                raise ValueError('Dimension of a hyperparameter must be a dictionary containing the parameters of its sampling method')
            method = search_space[hp]['method']
            # check if hyperparameter sampling method is supported
            if method not in sampling_methods:
                raise ValueError('Sampling method "{}" is not supported. '
                                 'Supported methods are: {}'.format(method,','.join(sampling_methods)))
            for arg in config_format[method]:
                if arg in search_space[hp]['dimension']:
                    # check if the argument type of the sampling method is correct
                    value_type = config_format[method][arg]['type']
                    if not isinstance(search_space[hp]['dimension'][arg], value_type):
                        raise ValueError('The value of argument "{}" for the sampling method '
                              '"{}" (for hyperparameter "{}") must be of type {}'.format(
                            arg, method, hp, type2str(value_type)))
                else:
                    # check if a required argument for the sampling method is missing
                    if (config_format[method][arg]['required']):
                        raise ValueError('Missing argument "{}" for the sampling method "{}" '
                                         'for the hyperparameter "{}"'.format(arg, method, hp))
                    # set the argument to its default value if not specified
                    if ('default' in config_format[method][arg]):
                        print('Info: The argument "{}" for the sampling method "{}" for'
                              ' the hyperparameter "{}" will be set to its default value {}'.format(
                              arg, method, hp, config_format[method][arg]['default']))
                        search_space[hp]['dimension'][arg] = config_format[method][arg]['default']

        return search_space