import os
import json
import yaml
import shutil
from copy import deepcopy
from datetime import datetime
from distutils import dir_util

from hpogrid.configuration import (ConfigurationBase, ModelConfiguration, 
                                   HPOConfiguration, GridConfiguration,
                                   SearchSpaceConfiguration)

from hpogrid.utils.helper import get_base_path, copytree

class ProjectConfiguration(ConfigurationBase):
    _CONFIG_TYPE_ = 'project'
    _CONFIG_DISPLAY_NAME_ = 'project'
    _DESCRIPTION_ = 'Manage a project for hyperparamter optimization'
    _LIST_COLUMNS_ = ['Project Title']
    _NAME_HELP_ = 'Name given to the project'
    _CONFIG_FORMAT_ = \
        {
            'scripts_path': {
                'abbr': 'p',
                'description': 'Path to the location of training scripts'+\
                               ' (or the directory containing the training scripts)',
                'required': True,
                'type': str
            },
            'model_config': {
                'abbr': 'm',
                'description': 'Name of the model configuration to use',
                'required': True,
                'type': str
            },
            'search_space': {
                'abbr': 's',
                'description': 'Name of the search space configuration to use',
                'required': True,
                'type':str
            },
            'hpo_config': {
                'abbr': 'o',
                'description': 'Name of the hpo configuration to use',
                'required': True,
                'type':str
            },
            'grid_config': {
                'abbr': 'g',
                'description': 'Name of the grid configuration to use',
                'required': True,
                'type':str
            }
        }
    _CONFIG_CLS_ = {
        'model_config': ModelConfiguration,
        'hpo_config': HPOConfiguration,
        'grid_config': GridConfiguration,
        'search_space': SearchSpaceConfiguration
    }
    
    def __init__(self):
        super().__init__()
        self._scripts_path = None
        
    @classmethod
    def get_config_dir(cls):
        base_path = get_base_path()
        return os.path.join(base_path, 'projects')
    
    
    @classmethod
    def get_project_dir(cls, project_name):
        project_dir = os.path.join(cls.get_config_dir(), project_name)
        return project_dir
    
    @classmethod
    def get_config_path(cls, project_name:str=None, extension:str='json'):
        """Returns the full path of a configuration file
        
        Args:
            project_name: str
                Name of the project
            extension: str, default='json'
                File extension for configuration file
        """
        
        project_dir = cls.get_project_dir(project_name)
        project_path = os.path.join(project_dir, 'config',
                                    'project_config.{}'.format(extension))
        return project_path
    
    @classmethod
    def get_scripts_dir(cls, project_name:str=None):
        """Returns the path to the training scripts of a project
        
        Args:
            project_name: str
                Name of the project
        """
        
        project_dir = cls.get_project_dir(project_name)
        scripts_path = os.path.join(project_dir, 'scripts')
        return scripts_path
    
    @classmethod
    def get_proj_config_dir(cls, project_name:str=None):
        """Returns the path to the configuration file of a project
        
        Args:
            project_name: str
                Name of the project
        """
        
        project_dir = cls.get_project_dir(project_name)
        project_config_dir = os.path.join(project_dir, 'config')
        return project_config_dir    
    
    def _validate_arguments(self, **args):
        args = super()._validate_arguments(**args)
        scripts_path = args.pop('scripts_path', None)
        if (scripts_path == ConfigurationBase._DEFAULT_OPT_ARG_):
            print('INFO: Path to training scripts is not specified. Skipping...')
            scripts_path = None
        elif (scripts_path is not None) and (not os.path.exists(scripts_path)):
            raise FileNotFoundError('Path to training scripts {} does not exist.'.format(scripts_path))
            
        self._scripts_path = scripts_path

        # check if input configuration files exist
        for config_type in self._CONFIG_CLS_:
            config_cls = self._CONFIG_CLS_[config_type]
            if (config_type in args) and (args[config_type] != ConfigurationBase._DEFAULT_OPT_ARG_):
                config_name = args[config_type]
                args[config_type] = config_cls.load(config_name)
            else:
                print('INFO: Path to {} configuration is not specified. '
                      'Skipping...'.format(config_cls._CONFIG_DISPLAY_NAME_))
        return args
    
    @classmethod
    def validate(cls, config):
        proj_config = deepcopy(config)
        for config_type in cls._CONFIG_CLS_:
            config_cls = cls._CONFIG_CLS_[config_type]
            proj_config[config_type] = config_cls.validate(config[config_type])
        return proj_config
    
    @classmethod
    def _validate(cls, config):
        print('INFO: Started validation process for project configurations.')
        result = cls.validate(config)
        print('Info: Validation complete.')
        return result
    
    def save(self, name=None, config=None, scripts_path=None, action='create'):        
        if (name is None) and (config is None):
            name = self._name
            config = self._config
        if name is None: 
            raise ValueError('configuration name undefined')
        config = {'project_name':name, **config}
        project_dir = self.get_project_dir(name)
        
        action_map = {
            'create': 'Creating',
            'recreate': 'Recreating',
            'update': 'Updating'
        }
        
        print('INFO: {} project "{}"'.format(action_map.get(action, action.title()), name))
        if (os.path.exists(project_dir)):
            if  action == 'create':
                print('ERROR: Project "{}" already exists. If you want to overwrite,'
                    ' use "recreate" or "update" action instead of "create".'.format(name))
                return None
            elif action == 'recreate':
                backup_dir = self.get_project_dir('backup')
                os.makedirs(backup_dir, exist_ok=True)
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                backup_proj_dir = os.path.join(backup_dir, '{}_{}'.format(name, timestamp))
                shutil.move(project_dir, backup_proj_dir)
                print('INFO: Recreating project. Original project moved to backup directory {}.'.format(
                    backup_proj_dir))
        
        # create directories if not already exist
        config_dir = self.get_proj_config_dir(name)
        scripts_dir = self.get_scripts_dir(name)
        if not os.path.exists(project_dir):
            os.makedirs(project_dir)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        if not os.path.exists(scripts_dir):
            os.makedirs(scripts_dir)
        
        if scripts_path is None:
            scripts_path = self._scripts_path
        
        # copy training scripts
        if (scripts_path is not None):
            if os.path.exists(scripts_path):
                # copy training scripts to the project directory
                print('INFO: Copying training scripts from {} to {}'.format(scripts_path, scripts_dir))
                # copy contents of directory to project/scrsipts/
                if os.path.isdir(scripts_path):
                    copytree(scripts_path, scripts_dir)
                else:
                    shutil.copy2(scripts_path, scripts_dir)
            else:
                raise FileNotFoundError('Path to training scripts {} does not exist.'.format(scripts_path))
        
        config_path = self.get_config_path(name)
        config_path_yaml = self.get_config_path(name, extension='yaml')
        if (os.path.exists(config_path)) and (action=='create'):
            print('ERROR: {} configuration "{}" already exists.'
                'If you want to overwrite, use "recreate" or "update" instead.'.format(
                self._CONFIG_DISPLAY_NAME_.title(), config_path))
        else:
            with open(config_path, 'w') as config_file:
                json.dump(config, config_file, indent=2)
            with open(config_path_yaml, 'w') as config_file_yaml:
                yaml.dump(config, config_file_yaml, default_flow_style=False, sort_keys=False)
            action_map = {'create': 'Created', 'recreate': 'Recreated', 'update': 'Updated'}
            print('INFO: {} {} configuration {}'.format(action_map[action], self._CONFIG_TYPE_, config_path))
            print('INFO: {} {} configuration {}'.format(action_map[action], self._CONFIG_TYPE_, config_path_yaml))
            self.show(name)