import json
import os

from hpogrid.components.defaults import kConfigFormat, kProjConfigFormat, kHPOGridMetadataFormat


def type2str(typevar):
    if isinstance(typevar, tuple):
        return ', '.join([t.__name__ for t in typevar])
    else:
        return typevar.__name__
    
    
def validate(config, config_format):
    for key in config_format:
        if key in config:
            # check if the value type of the config is correct
            value_type = config_format[key]['type']
            if not isinstance(config[key], value_type):
                raise ValueError('The value of "{}" must be of type {}'.format(key, type2str(value_type)))
            # check if the value of the config is allowed
            if ('choice' in config_format[key]) and (config[key] not in config_format[key]['choice']):
                raise ValueError('The value of "{}" must be one of the followings: {}'.format(
                                 key, str(config_format[key]['choice']).strip('[]')))
        else:
            if config_format[key]['required']:
                raise ValueError('The required item "{}" is missing from the configuration'.format(key))
            # fill in default config if not specified
            if 'default' in config_format[key]:
                print('Info: Added the item "{}" with default value {} to the configuration'.format(
                    key, str(config_format[key]['default'])))
                config[key] = config_format[key]['default']
    for key in config:
        if key not in config_format:
            raise ValueError('Unknown item "{}" found in the configuration'.format(key)) 
    return config

def validate_config(config, config_type):
    if config_type == 'search_space':
        return validate_search_space(config)
    if config_type not in kConfigFormat:
        raise ValueError('Unknown configuration type "{}"'.format(config_type))
    config_format = kConfigFormat[config_type]
    print('Info: Validating {} configuration'.format(config_type))
    validate(config, config_format)
    print('Info: Successfully validated {} configuration'.format(config_type))
    return config 

def validate_project_config(config):
    print('INFO: Checking validity of configurations')
    config = validate(config, kProjConfigFormat)
    for sub_config in ['model_config', 'search_space', 'hpo_config', 'grid_config']:
        config_type = sub_config.replace('_config', '')
        config[sub_config] = validate_config(config[sub_config], config_type)
    return config
        
def validate_search_space(search_space):
    print('Info: Validating search space configuration...')
    config_format = kConfigFormat['search_space']
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
    print('Info: Successfully validated search space configuration')
    return search_space


def validate_job_metadata(data):
    if not isinstance(data, dict):
        return False
    return all(key in kHPOGridMetadataFormat for key in data)
    
def parse_configuration(config):
    validate_project_config(config)
    