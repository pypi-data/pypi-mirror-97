from hpogrid.configuration import ConfigurationBase

class ModelConfiguration(ConfigurationBase):
    _CONFIG_TYPE_ = 'model_config'
    _CONFIG_DISPLAY_NAME_ = 'model'
    _DESCRIPTION_ = 'Manage configuration for machine learning model'
    _LIST_COLUMNS_ = ['Model Configuration']
    _CONFIG_FORMAT_ = \
        {
            'script': {
                'abbr': 's',
                'description': 'Name of the training script where the function or class that defines'+\
                               ' the training model will be called to perform the training',
                'required': True,
                'type': str
            },
            'model': {
                'abbr': 'm',
                'description': 'Name of the function or class that defines the training model',
                'required': True,
                'type': str
            },
            'param': {
                'abbr': 'p',
                'description': 'Extra parameters to be passed to the training model',
                'required': False,
                'type': dict,
                'default': {}
            }
        }