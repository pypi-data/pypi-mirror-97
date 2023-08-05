import os
import sys
import json
import yaml
import shutil
import inspect
import tarfile
import fnmatch
import argparse
import multiprocessing
from typing import List, Dict
from contextlib import contextmanager
from subprocess import Popen, PIPE
import shlex

from hpogrid.components.defaults import *  
from hpogrid.components.environment_settings import *

def run_command(cmd):
    args = shlex.split(cmd, posix=False)
    with Popen(args, stdout=PIPE, bufsize=1, universal_newlines=True) as p:
        while True:
            line = p.stdout.readline()
            if not line:
                break
            print(line)    
        exit_code = p.poll()
    return exit_code


class NpEncoder(json.JSONEncoder):
    import numpy as np
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)
###############################################################################################
#################### Project Configuration Related         ####################################
###############################################################################################

def set_base_path(path:str) -> None:
    os.environ[kHPOGridEnvPath] = path
    print('INFO: Environment variable {} is set to {}'.format(kHPOGridEnvPath, path))    

def get_base_path():
    if kHPOGridEnvPath not in os.environ:
        print('WARNING: {} environment variable not set.'
            'Will set to current working directory by default.'.format(kHPOGridEnvPath))
        set_base_path(os.getcwd())
    return os.environ.get(kHPOGridEnvPath, os.getcwd())         

def get_config_dir(config_type:str):
    """Returns the directory that stores configuration files of a particular configuration type
    
    Args:
        config_type:str
            Type of configuration
    """
    config_dir = os.path.join(get_base_path(), kConfigPaths[config_type])
    return config_dir
    
def get_project_path(proj_name:str):
    if get_run_mode() in ['GRID', 'IDDS']:
        proj_path = get_workdir()
    elif get_run_mode() == 'LOCAL':
        proj_dir = get_config_dir('project')
        proj_path = os.path.join(proj_dir, proj_name)
    return proj_path

def get_project_config_path(proj_name:str):
    project_path = get_project_path(proj_name)
    config_path = os.path.join(project_path, 'config', kProjectConfigNameJson)
    return config_path
                        
def get_project_config(proj_name:str):
    config_path = get_project_config_path(proj_name)
    if not os.path.exists(config_path):
        raise FileNotFoundError('Missing project configuration file: {}'.format(config_path))
    config = load_configuration(config_path)
    return config     

def get_project_list(expr=None):
    if get_run_mode() in ['GRID', 'IDDS']:
        config_path = os.path.join(get_workdir(), 'config', kProjectConfigNameJson)
        config = load_configuration(config_path)
        project_list = [config['project_name']]
    elif get_run_mode() == 'LOCAL':
        base_path = get_base_path()
        proj_dir = os.path.join(base_path, kConfigPaths['project'])
        project_list = [d for d in os.listdir(proj_dir) if 
                        os.path.isdir(os.path.join(proj_dir, d))]
    expr = expr if expr is not None else '*'
    project_list = fnmatch.filter(project_list, expr)
    project_list = [p for p in project_list if p!='backup']

    return project_list

def is_project(obj:str):
    if not isinstance(obj, str):
        return False
    return obj in get_project_list()      

def load_configuration(config_input:[Dict, str]) -> Dict:
    """Returns project configuration given input
    
    Args:
        config_input: dict, str
            If dict, it is the configuration itself
            If str, it is either the name of the project,
            of path to a configuration file.
    """
    if isinstance(config_input, dict):
        return config_input
    elif isinstance(config_input, str):
        ext = os.path.splitext(config_input)[1]
        # check if config_input is a project name
        if not ext:
            if is_project(config_input):
                return get_project_config(config_input)
            else:
                raise ValueError('Project "{}" does not exist'.format(config_input))
        # check if configuration file exists
        if not (os.path.exists(config_input)):
            raise FileNotFoundError("Configuration file {} does not exist.".format(config_input))
        # load configuration file
        with open(config_input, 'r') as file:
            if ext in ['.txt', '.yaml']:
                config = yaml.safe_load(file)
            elif ext == '.json':
                config = json.load(file)
            else:
                raise ValueErrror('The configuration file has an unsupported '
                              'file extension: {}\n Supported file extensions '
                              'are .txt, .yaml or .json'.format(ext))
        return config
    else:
        raise ValueError('Unknown configuration format: {}'.format(type(config_input)))

        
def set_scripts_path(scripts_path, undo=False):
    if (scripts_path in sys.path) and (undo==True):
        print('INFO: Removed {} from $PYTHONPATH'.format(scripts_path))
        sys.path.remove(scripts_path)
        os.environ["PYTHONPATH"].replace(scripts_path+":","")
        
    if (scripts_path not in sys.path) and (undo==False):
        print('INFO: Adding {} to $PYTHONPATH'.format(scripts_path))
        sys.path.append(scripts_path)
        os.environ["PYTHONPATH"] = scripts_path + ":" + os.environ.get("PYTHONPATH", "")

def get_scripts_path(proj_name):
    project_path = get_project_path(proj_name)
    scripts_path = os.path.join(project_path, 'scripts')
    return scripts_path
     
        
def set_scripts_path_from_project(proj_name, undo=False):
    project_path = get_project_path(proj_name)
    scripts_path = os.path.join(project_path, 'scripts')
    set_scripts_path(scripts_path, undo=undo)   
    
################################################################################################ 
################################################################################################ 

def pretty_path(path:str):
    return os.path.abspath(os.path.realpath(os.path.expandvars(os.path.expanduser(path))))

def pretty_dirname(path:str):
    path = pretty_path(path)
    if os.path.isdir(path):
        return path
    else:
        return os.path.dirname(path)
        
@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)

def get_physical_devices(device_type='GPU'):
    import tensorflow as tf
    physical_devices = tf.config.list_physical_devices(device_type)
    return physical_devices

def get_n_gpu():
    '''
    import torch
    return torch.cuda.device_count()
    '''
    return len(get_physical_devices(device_type='GPU'))

def get_n_cpu():
    return multiprocessing.cpu_count()


def extract_tarball(in_path:str, out_path:str) ->List[str]:
    tarfiles = [ f for f in os.listdir(in_path) if f.endswith('tar.gz')]
    extracted_files = []
    for f in tarfiles:
        tar = tarfile.open(f, "r:gz")
        print('INFO: Untaring the file {}'.format(f))
        tar.extractall(path=out_path)
        extracted_files += tar.getnames()
        tar.close()
    return extracted_files

def remove_files(files:List[str]):
    for f in files:
        if os.path.isfile(f):
            os.remove(f)
        elif os.path.isdir(f):
            shutil.rmtree(f)        
            
def is_function_or_method(obj):
    """Check if an object is a function or method.
    Args:
        obj: The Python object in question.
    Returns:
        True if the object is an function or method.
    """
    return inspect.isfunction(obj) or inspect.ismethod(obj) or is_cython(obj)


def is_class_method(f):
    """Returns whether the given method is a class_method."""
    return hasattr(f, "__self__") and f.__self__ is not None  


"""
import socket
hostname = socket.gethostname()
"""
