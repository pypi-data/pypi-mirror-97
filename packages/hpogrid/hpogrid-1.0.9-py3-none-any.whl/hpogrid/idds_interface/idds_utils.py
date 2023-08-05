import os
import sys
import glob
import argparse
import json
from typing import Optional
import tempfile

from hpogrid.utils.cli_parser import CLIParser
from hpogrid.components.defaults import *
from hpogrid.utils import helper, stylus
from hpogrid.components import environment_settings
from hpogrid.components.validation import validate_project_config

def transpose_config(config):
    project_name = config['project_name']
    evaluation_container = config['grid_config']['container']
    search_space = config['search_space']
    library = config['hpo_config']['algorithm']
    if config['hpo_config']['algorithm_param']:
        method = config['hpo_config']['algorithm_param'].get('method', None)
    else:
        method = None
    max_point = config['hpo_config']['num_trials']
    max_concurrent = config['hpo_config']['max_concurrent']


    # format generator command
    generator_options = {}
    generator_options['n_point'] = '%NUM_POINTS'
    generator_options['max_point'] = '%MAX_POINTS'
    generator_options['infile'] = os.path.join(kiDDSBasePath, '%IN')
    generator_options['outfile'] = os.path.join(kiDDSBasePath, '%OUT')
    generator_options['lib'] = library
    if (library == 'nevergrad') and method:
        generator_options['method'] = method
    generator_cmd = 'hpogrid generate {}'.format(stylus.join_options(generator_options))

    # format idds configuration
    idds_config = {}
    idds_config['steeringExec'] = ("run --rm -v \"$(pwd)\":{idds_base_path} {container} " +\
    "/bin/bash -c \"{cmd}\" ").format(idds_base_path=kiDDSBasePath, container=kDefaultiDDSContainer, cmd=generator_cmd)
    #idds_config['steeringExec'] = ("run --rm -v \"$(pwd)\":{idds_base_path} {container} " +\
    #"/bin/bash -c \"{cmd}\" ").format(idds_base_path="/HPOiDDS", container="gitlab-registry.cern.ch/zhangruihpc/steeringcontainer:0.0.2", cmd=generator_cmd)

    idds_config['evaluationExec'] = "pip install --upgrade hpogrid && " + \
                                    "hpogrid run {project_name} --mode idds".format(project_name=project_name)
    idds_config['evaluationContainer'] = evaluation_container
    idds_config['evaluationInput'] = kiDDSHPinput
    idds_config['evaluationOutput'] = kiDDSHPoutput
    idds_config['evaluationMeta'] = kGridSiteMetadataFileName
    idds_config['nParallelEvaluation'] = max_concurrent
    idds_config['maxPoints'] = max_point
    return idds_config, search_space


def get_search_points():
    if not environment_settings.is_idds_job():
        raise RuntimeError('Cannot get search points for non-idds environment')
    
    workdir = helper.get_workdir()
    search_point_path = os.path.join(workdir, kiDDSHPinput)
    if not os.path.exists(search_point_path):
        raise FileNotFoundError('No such file or directory: \'{}\''.format(search_point_path))
    with open(search_point_path,'r') as search_point_file:
        search_points = json.load(search_point_file)
    return search_points

def create_idds_output_from_metadata(metadata):
    idds_output = {}
    idds_output['status'] = 0
    loss = []
    metric = metadata['metric']
    for index in metadata['result']:
        loss.append(metadata['result'][index][metric])
    if len(loss) == 1:
        loss = loss[0]
    idds_output['loss'] = loss
    idds_output['message'] = ''
    return idds_output


def save_idds_output_from_metadata(metadata):
    if not environment_settings.is_idds_job():
        raise RuntimeError('save_output should not be called in non-idds environment')    
        
    output = create_idds_output_from_metadata(metadata)
    workdir = helper.get_workdir()
    output_path = os.path.join(workdir, kiDDSHPoutput)
    with open(output_path, 'w') as output_file:
        print('INFO: Saved idds output at {}'.format(output_path))
        json.dump(output, output_file, cls=helper.NpEncoder)
        
class IDDSInterface():
    _USAGE_ = 'hpogrid idds_log <task_id>'
    _DESCRIPTION_ = 'Tool for retrieving iDDS logs'      
    
    @staticmethod
    def get_parser(**kwargs):
        parser = CLIParser(description=IDDSInterface._DESCRIPTION_,
                           usage=IDDSInterface._USAGE_, **kwargs)           
        parser.add_argument('task_id', help='Task ID for iDDS job', type=int)      
        return parser
    
    @staticmethod
    def run_parser(args=None):
        parser = IDDSInterface.get_parser()
        args = vars(parser.parse_args(args))
        task_id = args['task_id']
        IDDSInterface.check_log(workload_id=task_id)
    
    @staticmethod
    def check_log(workload_id:int, request_id=None,
                  idds_config_path=kDefaultiDDSConfigPath,
                  proxy_path=kDefaultProxyPath):
        os.environ['IDDS_CONFIG'] = idds_config_path
        original_proxy = os.environ.get('X509_USER_PROXY', None)
        os.environ['X509_USER_PROXY'] = proxy_path
        from idds.client.client import Client
        from idds.common.utils import get_rest_host
        host = get_rest_host()
        client = Client(host=host)

        print('INFO: Fetching iDDS log files for the task: {}'.format(workload_id))
        filename = client.download_logs(workload_id=workload_id, request_id=request_id, dest_dir='/tmp')
        print('INFO: iDDS log files can be found at:')
        print(filename)
        if original_proxy:
            os.environ['X509_USER_PROXY'] = original_proxy
        
        