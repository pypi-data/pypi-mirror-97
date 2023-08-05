import os
import sys
import glob
import json
import argparse
from copy import deepcopy
from json import JSONDecodeError

from hpogrid.utils import stylus
from hpogrid.utils.cli_parser import CLIParser
from hpogrid.utils.helper import get_base_path, load_configuration

class ConfigurationBase(object):
    _ACTION_HELP_MESSAGE_ = {
        'list': 'List all configuration files',
        'show': 'Display the content of a configuration file',
        'remove': 'Remove a configuration file',
        'create': 'Create a new configuration file',
        'update': 'Update a configuration file (old configuration will be kept)',
        'recreate': 'Recreate a configuration file (old configuration will be overwritten)',
    }    
    _CONFIG_TYPE_ = '<config_type>'
    _CONFIG_DISPLAY_NAME_ = '<CONFIG>'
    _ACTION_ = '<action>'
    _USAGE_ = 'hpogrid {config_type} [-h|--help] {action} [<args>]'
    _DESCRIPTION_ = 'Tool for management of configuration files'
    _LIST_COLUMNS_ = ['General Configuration']
    _SHOW_COLUMNS_ = ['Attribute', 'Value']    
    _CONFIG_FORMAT_ = {}
    _NAME_HELP_ = 'Name given to the {config_name} configuration file'
    _DEFAULT_OPT_ARG_ = '0'*99
    
    def __init__(self):
        self.parser_mode = False
        self._config = {}
        self._name = None
    
    @staticmethod
    def _make_optional_arguments(parser):
        new_parser = deepcopy(parser)
        for action in new_parser._actions:
            if (len(action.option_strings) > 0) and (action.default != '==SUPPRESS=='):
                action.default = ConfigurationBase._DEFAULT_OPT_ARG_
                action.required = False
        return new_parser

    def get_parser(self, **kwargs):
        usage_str = self._USAGE_.format(config_type=self._CONFIG_TYPE_,
                                        action=self._ACTION_)
        parser = CLIParser(description=self._DESCRIPTION_,
                           usage=usage_str, **kwargs) 
        parser.set_title('The most commonly used actions are')
        action_subparser = parser.add_subparsers(dest="action", parser_class=CLIParser)
        
        # parser for configuration file management
        config_parser = argparse.ArgumentParser(add_help=False)
        config_parser.add_argument('name', help=self._NAME_HELP_.format(config_name=self._CONFIG_DISPLAY_NAME_))
        for arg in self._CONFIG_FORMAT_:
            arg_data = self._CONFIG_FORMAT_[arg]
            full_arg = '--{}'.format(arg)
            if arg_data['abbr'] is None:
                arg_options = (full_arg,)
            else:
                abbr_arg = '-{}'.format(arg_data['abbr'])
                arg_options = (abbr_arg, full_arg)
            extra_options = {}
            extra_options['help'] = arg_data['description']
            if not isinstance(arg_data['type'], tuple):
                arg_type = tuple([arg_data['type']])
            else:
                arg_type = arg_data['type']

            if bool in arg_type:
                extra_options['action'] = 'store_true' if not arg_data['default'] else 'store_false'
            else:
                if dict in arg_type:
                    extra_options['type'] = None
                elif list in arg_type:
                    extra_options['type'] = None
                    extra_options['nargs'] = '+'
                else:
                    extra_options['type'] = arg_type[0]
                extra_options['metavar'] = ''
                extra_options['required'] = arg_data['required']
                if not arg_data['required']:
                    extra_options['default'] = arg_data['default']
            
            if 'choice' in arg_data:
                extra_options['choices'] = arg_data['choice']
                
            config_parser.add_argument(*arg_options, **extra_options)    
        
        action_parsers = {}
        for action, msg in ConfigurationBase._ACTION_HELP_MESSAGE_.items():
            usage_str = self._USAGE_.format(config_type=self._CONFIG_TYPE_, action=action)
            args = {'help': msg, 'description': msg, 'usage': usage_str, 'prog': usage_str}
            if action in ['create', 'recreate']:
                args['parents'] = [config_parser]
            elif action == 'update':
                args['parents'] = [self._make_optional_arguments(config_parser)]
            action_parsers[action] = action_subparser.add_parser(action, **args)  
            
        action_parsers['list'].add_argument('-e', '--expr', metavar='',
                help='Filter out configuration files that matches the expression',
                required=False)
        
        action_parsers['show'].add_argument('name',
                help='Name of the configuration file to show')
        
        action_parsers['remove'].add_argument('name',
                help='Name of the configuration file to remove')
        
        return parser
    
    def run_parser(self, args=None):
        parser = self.get_parser()
        args = vars(parser.parse_args(args))  
        action = args.pop('action')
        if action is None:
            parser.print_help()
            sys.exit(0)
        if not hasattr(self, action):
            print('Unrecognized action: {}'.format(action))
            parser.print_help()
            sys.exit(0)
        self.parser_mode = True
        getattr(self, action)(**args)
        self.parser_mode = False
        
    @property
    def config(self):
        return self._config
    
    @property
    def name(self):
        '''Name of configuration
        '''
        return self._name
        
    @classmethod
    def get_config_dir(cls):
        base_path = get_base_path()
        if cls._CONFIG_TYPE_ == 'project':
            return os.path.join(base_path, 'projects')
        else:
            return os.path.join(base_path, 'config', cls._CONFIG_TYPE_)
    
    @classmethod
    def get_config_path(cls, config_name:str=None, extension:str='json'):
        """Returns the full path of a configuration file
        
        Args:
            config_name: str
                Name of the configuration file
            extension: str, default='json'
                File extension for configuration file
        """
        
        config_dir = cls.get_config_dir()
        if cls._CONFIG_TYPE_ == 'project':
            config_file_name = os.path.join(config_dir, config_name,
                                            'project_config.{}'.format(extension))
        else:
            config_file_name = '{}.{}'.format(config_name, extension)
        config_path = os.path.join(config_dir, config_file_name)
        return config_path    
    
    @classmethod
    def get_config_list(cls, expr:str=None):
        """Returns a list of configuration files for a specific type of configuration
        
        Args:
            expr: str
                Regular expression for filtering name of configuration files
        """
        expr = '*' if expr is None else expr
        
        config_dir = cls.get_config_dir()
        path_expr = os.path.join(config_dir, expr)
        
        config_list = []
        for config_path in glob.glob(path_expr):
            config_name = os.path.basename(config_path)
            # remove extension
            config_name = os.path.splitext(config_name)[0]
            config_list.append(config_name)
            
        return config_list  
    
    @classmethod
    def load(cls, name:str):
        """Returns a specified configuration file
        
        Args:
            name: str
                Name of configuration file
        """
        if not os.path.exists(name):
            config_path = cls.get_config_path(name)
            if not os.path.exists(config_path):
                raise FileNotFoundError('Configuration file {} does not exist.'.format(config_path))
        else:
            config_path = name
        ext = os.path.splitext(config_path)[1]
        
        # load configuration file according to file type
        with open(config_path, 'r') as file:
            if ext in ['.txt', '.yaml']:
                config = yaml.safe_load(file)
            elif ext == '.json':
                config = json.load(file)
            else:
                raise ValueErrror('The configuration file has an unsupported '
                              'file extension: {}\n Supported file extensions '
                              'are .txt, .yaml or .json'.format(ext))
        return config
    
    @classmethod
    def list(cls, expr:str=None):
        """List out configuration files for a specific type of configuration as a table
        
        Args:
            expr: str
                Regular expression for filtering name of configuration files        
            exclude: list[str]
                Configuration files to exclude from listing
        """
        config_list = cls.get_config_list(expr)
        table = stylus.create_table(config_list, cls._LIST_COLUMNS_)
        print(table)    
        
    @classmethod
    def show(cls, name:str):
        """Display the content of a configuration file
        
        Args:
            name: str
                Name of configuration file        
        """
        config = cls.load(name)
        table = stylus.create_formatted_dict(config, cls._SHOW_COLUMNS_, indexed=False)
        print(table)     
        
    @classmethod
    def remove(cls, name):
        """Removes a configuration file
        
        Args:
            name: str
                Name of the configuration file to remove
        """
        config_path = cls.get_config_path(name)
        if os.path.exists(config_path):
            os.remove(config_path)
            print('INFO: Removed file {}'.format(config_path))
        else:
            print('ERROR: Cannot remove file {}. File does not exist.'.format(config_path))  
            
    def _validate_arguments(self, **args):
        if 'name' not in args:
            raise ValueError('missing argument: config_name')
        return args
    
    @classmethod
    def _validate(cls, config):
        print('Info: Validating {} configuration...'.format(cls._CONFIG_DISPLAY_NAME_))
        result = cls.validate(config)
        print('Info: Successfully validated {} configuration'.format(cls._CONFIG_DISPLAY_NAME_))
        return result
    
    @classmethod
    def validate(cls, config):
        validated_config = deepcopy(config)
        config_format = cls._CONFIG_FORMAT_
        for key in config_format:
            if key in config:
                # check if the value type of the config is correct
                value_type = config_format[key]['type']
                # if attribute type is dict, parse string input as dict
                if (value_type == dict) or (isinstance(value_type, tuple) and (dict in value_type)):
                    if isinstance(config[key], str):
                        try:
                            validated_config[key] = json.loads(config[key])
                        except JSONDecodeError:
                            raise RuntimeError('ERROR: Cannot decode the value of "{}" as dictionary.'
                                'Please check your input.'.format(key))
                elif not isinstance(config[key], value_type):
                    if isinstance(value_type, tuple):
                        print_type = stylus.type2str(value_type[0])
                    else:
                        print_type = stylus.type2str(value_type)
                    raise ValueError('The value of "{}" must be of type {}'.format(key, print_type))
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
                    validated_config[key] = config_format[key]['default']
        for key in config:
            if key not in config_format:
                raise ValueError('Unknown item "{}" found in the configuration'.format(key)) 
        return validated_config        
    
    def create(self, **args):
        args = self._validate_arguments(**args)
        return self._configure(action='create', **args)
        
    def recreate(self, **args):
        args = self._validate_arguments(**args)
        return self._configure(action='recreate', **args)
        
    def update(self, **args):
        args = self._validate_arguments(**args)
        config_name = args['name']
        config_path = self.get_config_path(config_name)
        if not os.path.exists(config_path):
            raise FileNotFoundError('Cannot update file {}. File does not exist.'.format(config_path))        
        old_config = self.load(config_name)
        new_config = {k:v for k,v in args.items() if v != ConfigurationBase._DEFAULT_OPT_ARG_}
        updated_config = {**old_config, **new_config}
        return self._configure(action='update', **updated_config)
    
    def _configure(self, action, **args):
        config_name = args.pop('name')
        config = self._validate(args)
        self._name = config_name
        self._config = config
        if self.parser_mode:
            self.save(action=action)
        return config
    
    def save(self, name=None, config=None, action='create'):
        if (name is None) and (config is None):
            name = self._name
            config = self._config
        if name is None: 
            raise ValueError('configuration name undefined')
        config_dir = self.get_config_dir()
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        config_path = self.get_config_path(name)
        if (os.path.exists(config_path)) and (action=='create'):
            display_str = self._CONFIG_DISPLAY_NAME_[0].upper() + self._CONFIG_DISPLAY_NAME_[1:]
            print('ERROR: {} configuration "{}" already exists.'
                'If you want to overwrite, use "recreate" or "update" instead.'.format(
                display_str, config_path))
        else:
            with open(config_path, 'w') as config_file:
                json.dump(config, config_file, indent=2)
            action_map = {'create': 'Created', 'recreate': 'Recreated', 'update': 'Updated'}
            print('INFO: {} {} configuration {}'.format(action_map[action], self._CONFIG_TYPE_, config_path))
            self.show(name)