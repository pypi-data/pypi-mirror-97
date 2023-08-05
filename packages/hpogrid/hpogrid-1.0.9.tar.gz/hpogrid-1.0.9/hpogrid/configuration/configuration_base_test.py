import sys, os
import argparse
import json
import fnmatch

from hpogrid.utils import stylus
from hpogrid.components.defaults import *
from hpogrid.utils.helper import load_configuration, get_base_path, get_config_dir
from json import JSONDecodeError

kActionList = ['create', 'recreate', 'update', 'list', 'show', 'remove']  



class ConfigurationBase(object):
    @staticmethod
    def get_parser(config_type, parent_parser=None, **kwargs):
        parser = argparse.ArgumentParser(**kwargs) 
        subparsers = parser.add_subparsers(help='actions')
        def get_usage_str(action):
            return 'hpogrid {} {} [<options>]'.format(config_type, action)
        # action = list
        parser_list = subparsers.add_parser('list', 
        description='List all configuration files',
        usage=get_usage_str('list'),
        prog=get_usage_str('list'))
        parser_list.add_argument('-e', '--expression', metavar='',
                help='Filter out configuration files that matches the expression',
                required=False)
        
        # action = show
        parser_show = subparsers.add_parser('show', 
        description='Display the content of a configuration file',
        usage=get_usage_str('show'),
        prog=get_usage_str('show'))
        parser_show.add_argument('name', help='Name of the configuration file to show')
        
        # action = remove
        parser_remove = subparsers.add_parser('remove', 
        description='Remove a configuration file',
        usage=get_usage_str('remove'),
        prog=get_usage_str('remove'))
        parser_remove.add_argument('name', help='Name of the configuration file to remove')
        
        if parent_parser is None:
            parent_parser = argparse.ArgumentParser(add_help=False)
        
        # action = create
        parser_create = subparsers.add_parser('create', 
        description='Create a new configuration file',
        usage=get_usage_str('create'),
        prog=get_usage_str('create'),
        parents=[parent_parser])
        
        # action = update
        parser_update = subparsers.add_parser('update', 
        description='Update a configuration file',
        usage=get_usage_str('update'),
        prog=get_usage_str('update'),
        parents=[parent_parser])
        
        # action = recreate
        parser_recreate = subparsers.add_parser('recreate', 
        description='Recreate a configuration file',
        usage=get_usage_str('recreate'),
        prog=get_usage_str('recreate'),
        parents=[parent_parser])        
        return parser
    
  

class ConfigurationBaseDeprecated():
    
    config_type = 'SUPPRESS'
    description = 'Manage configuration'
    usage = 'hpogrid <config_type> <action> <config_name> [<options>]'
    list_columns = []
    show_columns = []
    json_interpreted = []
           
    def get_base_parser(self):
        parser = argparse.ArgumentParser(
            description=self.description,
            usage=self.usage) 
        return parser
    
    @staticmethod
    def get_parser_test(config_type, parent_parser=None, **kwargs):
        parser = argparse.ArgumentParser(**kwargs) 
        subparsers = parser.add_subparsers(help='actions')
        def get_usage_str(action):
            return 'hpogrid {} {} [<options>]'.format(config_type, action)
        # action = list
        parser_list = subparsers.add_parser('list', 
        description='List all configuration files',
        usage=get_usage_str('list'),
        prog=get_usage_str('list'))
        parser_list.add_argument('-e', '--expression', metavar='',
                help='Filter out configuration files that matches the expression',
                required=False)
        
        # action = show
        parser_show = subparsers.add_parser('show', 
        description='Display the content of a configuration file',
        usage=get_usage_str('show'),
        prog=get_usage_str('show'))
        parser_show.add_argument('name', help='Name of the configuration file to show')
        
        # action = remove
        parser_remove = subparsers.add_parser('remove', 
        description='Remove a configuration file',
        usage=get_usage_str('remove'),
        prog=get_usage_str('remove'))
        parser_remove.add_argument('name', help='Name of the configuration file to remove')
        
        if parent_parser is None:
            parent_parser = argparse.ArgumentParser(add_help=False)
        
        # action = create
        parser_create = subparsers.add_parser('create', 
        description='Create a new configuration file',
        usage=get_usage_str('create'),
        prog=get_usage_str('create'),
        parents=[parent_parser])
        
        # action = update
        parser_update = subparsers.add_parser('update', 
        description='Update a configuration file',
        usage=get_usage_str('update'),
        prog=get_usage_str('update'),
        parents=[parent_parser])
        
        # action = recreate
        parser_recreate = subparsers.add_parser('recreate', 
        description='Recreate a configuration file',
        usage=get_usage_str('recreate'),
        prog=get_usage_str('recreate'),
        parents=[parent_parser])        
        return parser

    def get_parser(self, action=None):
        parser = self.get_base_parser()           
        if not action:
            parser.add_argument('action', help='Action to be performed', choices=kActionList)    
        elif action == 'list':
            parser.add_argument('--expr', metavar='',
                help='Filter out config files that matches the expression')
        elif action == 'show':
            parser.add_argument('name', help='Name of config file to show')
        elif action == 'remove':
            parser.add_argument('name', help='Name of config file to remove')
        else:
            raise ValueError('Unknown method: {}'.format(action))
        return parser

    def get_updated_config(self, config):
        non_updated_keys = []
        for key in config:
            if config[key] is None:
                non_updated_keys.append(key)
        for key in non_updated_keys:
            config.pop(key, None)
        config_path = self.get_config_path(config['name'])
        if not os.path.exists(config_path):
            raise FileNotFoundError('Configuration file {} not found. Update aborted.'.format(config_path))
        old_config = json.load(open(config_path))
        config = {**old_config, **config}
        return config

    def _retain_only_updated_options(self):
        parser = self.get_parser('update')
        for action in parser._actions:
            if (len(action.option_strings) > 0) and (action.default != '==SUPPRESS=='):
                action.default=None
        args = parser.parse_args(sys.argv[3:])
        return args

    def configure(self, args, action='create'):
        if action == 'update':
            args = self._retain_only_updated_options()

        config = vars(args)
        
        if action == 'update':
            config = self.get_updated_config(config)

        self.process_config(config)
        config_name = config.pop('name', None)
        if config is not None:
            self.save(config, config_name, action)
        return config

    def process_config(self, config):
        for key in config:
            if isinstance(config[key], bool):
                config[key] = int(config[key])            
            if (key in self.json_interpreted) and isinstance(config[key], str):
                try:
                    config[key] = json.loads(config[key])
                except JSONDecodeError:
                    raise ValueError('ERROR: Cannot decode the value of {} into json format.'
                        'Please check your input.'.format(key))   
        return config

    def save(self, config, name, action='create'):

        config_path = self.get_config_path(name)
        if (os.path.exists(config_path)) and (action=='create'):
            print('ERROR: {} configuration with name {} already exists.'
                'If you want to overwrite, use "recreate" or "update" action instead of "create".'.format(
                self.config_type, name))
        else:
            with open(config_path, 'w') as config_file:
                json.dump(config, config_file, indent=2)
            action_map = { 'create': 'Created', 'recreate': 'Recreated', 'update': 'Updated'}
            print('INFO: {} {} configuration {}'.format(action_map[action], self.config_type, config_path))
            self.show(name)

    @classmethod
    def get_config_dir(cls, force_create:bool=True):
        """Returns the directory under which the specific type of configuration files
        are stored
        
        Args:
            force_create: boolean, default=True
                Whether to force create the directory if not already exists
        """
        config_dir = get_config_dir(cls.config_type)

        if (not os.path.exists(config_dir)) and force_create:
            os.makedirs(config_dir, exist_ok=True)
        return config_dir
    
    @classmethod
    def get_config_path(cls, config_name:str=None, extension='.json'):
        """Returns the full path of a configuration file
        
        Args:
            config_name: str
                Name of the configuration file
            extension: str
                File extension for configuration file
        """

        config_dir = cls.get_config_dir()
        config_base_name = '{}{}'.format(config_name, extension)
        config_path = os.path.join(config_dir, config_base_name)
        return config_path
    
    @classmethod
    def get_config_list(cls, expr:str=None):
        """Returns a list of configuration files for a specific type of configuration
        
        Args:
            expr: str
                Regular expression for filtering name of configuration files
        """
        expr = expr if expr is not None else '*'
        
        config_dir = cls.get_config_dir()
        config_list = [os.path.splitext(d)[0] for d in os.listdir(config_dir) if not d.startswith('.')]
        if expr is not None:
            config_list = fnmatch.filter(config_list, expr)
        return config_list
    
    @classmethod
    def load(cls, name:str):
        """Returns a specified configuration file
        
        Args:
            name: str
                Name of configuration file
        """
        config_path = cls.get_config_path(name)
        config = load_configuration(config_path)
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
        table = stylus.create_table(config_list, cls.list_columns)
        print(table)
    
    @classmethod
    def show(cls, name:str):
        """Display the content of a configuration file
        
        Args:
            name: str
                Name of configuration file        
        """
        config = cls.load(name)
        #table = stylus.create_table(config.items(), self.show_columns, indexed=False)
        table = stylus.create_formatted_dict(config, cls.show_columns, indexed=False)
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