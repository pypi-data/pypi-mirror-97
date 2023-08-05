import os
from hpogrid.components.defaults import *  

def get_run_mode():
    return os.environ.get('HPOGRID_RUN_MODE', 'LOCAL')

def get_datadir():
    return os.environ.get('HPOGRID_DATA_DIR', os.getcwd())

def get_workdir():
    return os.environ.get('HPOGRID_WORK_DIR', os.getcwd())

def grid_workdir():
    if os.path.exists(kGridSiteWorkDir):
        return kGridSiteWorkDir
    else:
        return os.getcwd()

def is_grid_job():
    return (get_run_mode() in ['GRID', 'IDDS'])

def is_idds_job():
    return (get_run_mode() == 'IDDS')

def is_local_job():
    return (get_run_mode() == 'LOCAL')
    
def setup(run_mode:str='local'):
    allowed_modes = ['local', 'grid', 'idds']
    run_mode = run_mode.lower()
    if run_mode not in allowed_modes:
        raise ValueError('Unknown running mode: {}. '
                         'Allowed running modes are {}'.format(run_mode, allowed_modes))
    print('INFO: Setting up HPO task')

    if run_mode == 'local':
        os.environ['HPOGRID_RUN_MODE'] = 'LOCAL'
        os.environ['HPOGRID_DATA_DIR'] = os.getcwd()
        os.environ['HPOGRID_WORK_DIR'] = os.getcwd()
    elif run_mode == 'grid':
        os.environ['HPOGRID_RUN_MODE'] = 'GRID'
        os.environ['HPOGRID_DATA_DIR'] = grid_workdir()
        os.environ['HPOGRID_WORK_DIR'] = grid_workdir()
    elif run_mode == 'idds':
        os.environ['HPOGRID_RUN_MODE'] = 'IDDS'
        os.environ['HPOGRID_DATA_DIR'] = grid_workdir()
        os.environ['HPOGRID_WORK_DIR'] = grid_workdir()
        
    print('INFO: HPO task will run in {} environment'.format(run_mode))
    print('INFO: Work directory is set to "{}"'.format(get_workdir()))
    print('INFO: Data directory is set to "{}"'.format(get_datadir()))
    
def reset():
    os.environ.pop('HPOGRID_RUN_MODE', None)
    os.environ.pop('HPOGRID_DATA_DIR', None)
    os.environ.pop('HPOGRID_WORK_DIR', None)