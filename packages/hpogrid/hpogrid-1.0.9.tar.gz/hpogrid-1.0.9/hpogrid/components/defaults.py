import json

kHPOGridEnvPath = 'HPOGRID_BASE_PATH'

kProjectConfigNameJson = 'project_config.json'
kProjectConfigNameYaml = 'project_config.yaml'

kiDDSConfigName = 'idds_config.json'
kiDDSSearchSpaceName = 'search_space.json'
kiDDSHPinput = 'input.json'
kiDDSHPoutput = 'output.json'
kiDDSMetrics = "metrics.tgz"

kConfigAction = ['create', 'recreate', 'update']

kAlgoMap = {
    'random': 'tune',
    'bayesian': 'hyperopt'
}

kDefaultiDDSConfigPath = '/afs/cern.ch/work/c/chlcheng/public/hpogrid/idds.cfg'
kDefaultProxyPath = '/etc/pki/tls/cert.pem'
#####################################################
##############    Paths Related      ################
#####################################################
kConfigPaths = {
    'project': 'projects',
    'hpo': 'config/hpo',
    'search_space': 'config/search_space',
    'model': 'config/model',
    'grid': 'config/grid'
}

kDockerBasePath = '/workDir'
kiDDSBasePath = kDockerBasePath
kGridSiteWorkDir = '/srv/workDir/'

#####################################################
############    Grid Site Related      ##############
#####################################################

kGPUSiteNGPU = {
    'ANALY_MANC_GPU_TEST': 10, #single queue, no submission parameters, 1 GPU per job
    'ANALY_QMUL_GPU_TEST': 6, # GPUNumber=x for now is hardcoded in the dev APF JDL,number of GPUs per job limited by cgroups, K80=2*K40, so total of 6 gpu slots avalable.
    'ANALY_MWT2_GPU': 8, #single queue, no submission parameters, 1 GPU per job
    'ANALY_BNL_GPU_ARC': 12, #also shared with Jupyter users who have priority
    'ANALY_INFN-T1_GPU': 2 #single queue, no submission parameters, 1 GPU per job
}

#########################################################
#############    Configuration Defaults    ##############
#########################################################

kDefaultContainer = '/cvmfs/unpacked.cern.ch/gitlab-registry.cern.ch/aml/hyperparameter-optimization/alkaid-qt/hpogrid:latest'
kDefaultContainer2 = '/cvmfs/unpacked.cern.ch/gitlab-registry.cern.ch/clcheng/hyperparameter-optimization-on-the-grid:latest'
kDefaultiDDSContainer = 'gitlab-registry.cern.ch/aml/hyperparameter-optimization/alkaid-qt/hpogrid:latest'
kDefaultContainer4 = 'docker://gitlab-registry.cern.ch/aml/hyperparameter-optimization/alkaid-qt/hpogrid:base'

kSearchAlgorithms = ['hyperopt', 'skopt', 'bohb', 'ax', 'tune', 'random', 'grid', 'bayesian', 'nevergrad']
kSchedulers = ['asynchyperband', 'bohbhyperband', 'pbt']
kMetricMode = ['min', 'max']

kDefaultSearchAlgorithm = 'random'
kDefaultScheduler = 'asynchyperband'
kDefaultMetric = 'loss'
kDefaultMetricMode = 'min'
kDefaultTrials = 1


kDefaultOutDS = 'user.${{RUCIO_ACCOUNT}}.hpogrid.{HPO_PROJECT_NAME}.out.$(date +%Y%m%d%H%M%S)'

kHPOGridMetadataFormat = ['task_time_s', 'start_timestamp', 'project_name', 
                          'result', 'hyperparameters', 'metric', 'start_datetime', 
                          'best_config', 'end_datetime', 'mode']

kProjConfigFormat = {
    'project_name': {
        'required': True,
        'type': str
    },
    'scripts_path': {
        'required': True,
        'type': str
    },
    'model_config': {
        'required': True,
        'type': dict
    },
    'search_space': {
        'required': True,
        'type':dict
    },
    'hpo_config': {
        'required': True,
        'type':dict
    },
    'grid_config': {
        'required': True,
        'type':dict
    }
}

kConfigFormat = {
    'hpo':{
        'algorithm': {
            'required': False,
            'type': str,
            'choice': kSearchAlgorithms,
            'default': 'random'
        },
        'scheduler': {
            'required': False,
            'type': str,
            'choice': kSchedulers,
            'default': 'asynchyperband'
        },        
        'metric' : {
            'required': True,
            'type': str,
        },
        'extra_metrics': {
            'required': False,
            'type': (list, type(None)),
            'default': None
        },
        'mode' : {
            'required': True,
            'type': str,
            'choice': kMetricMode,
        },
        'resource': {
            'required': False,
            'type': (dict, type(None)),
            'default': None
        },
        'num_trials': {
            'required': True,
            'type': int,
        },
        'log_dir': {
            'required': False,
            'type': str,
            'default': None
        },
        'verbose': {
            'required': False,
            'type': int,
            'default': 0
        },
        'max_concurrent': {
            'required': False,
            'type': int,
            'default': 3
        },
        'stop': {
            'required': False,
            'type': dict,
            'default': {'training_iteration': 1}
        },
        'scheduler_param': {
            'required': False,
            'type': dict,
            'default': {}
        },
        'algorithm_param': {
            'required': False,
            'type': dict,
            'default': {}
        }       
    },
    'grid': {
        'site': {
            'required': False,
            'type': (list, str),
            'default': None
        },
        'container': {
            'required': False,
            'type': str,
            'default': kDefaultContainer
        },
        'retry': {
            'required': False,
            'type': int,
            'default': 0
        },
        'inDS': {
            'required': False,
            'type': (str, type(None)),
            'default': None
        },
        'outDS': {
            'required': False,
            'type': str,
            'default': kDefaultOutDS
        },
        'extra': {
            'required': False,
            'type': dict,
            'default': {}
        }
    },
    'model':{
        'script': {
            'required': True,
            'type': str
        },
        'model': {
            'required': True,
            'type': str
        },
        'param': {
            'required': False,
            'type': dict,
            'default': {}
        }
    },
    'search_space':{
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
}

kDefaultGridExtraParam = json.dumps(kConfigFormat['grid']['extra']['default'])
kDefaultSearchAlgorithm = kConfigFormat['hpo']['algorithm']['default']
kDefaultScheduler = kConfigFormat['hpo']['scheduler']['default']
kDefaultMaxConcurrent = kConfigFormat['hpo']['max_concurrent']['default']
kDefaultLogDir = kConfigFormat['hpo']['log_dir']['default']
kDefaultVerbosity = kConfigFormat['hpo']['verbose']['default']
kDefaultStopping = json.dumps(kConfigFormat['hpo']['stop']['default'])
kDefaultResource = json.dumps(kConfigFormat['hpo']['resource']['default'])
kDefaultSchedulerParam = json.dumps(kConfigFormat['hpo']['scheduler_param']['default'])
kDefaultAlgorithmParam = json.dumps(kConfigFormat['hpo']['algorithm_param']['default'])
kDefaultModelParam = json.dumps(kConfigFormat['model']['param']['default'])

kHPOGridMetadataFormat = ['project_name', 'metric', 'mode', 'task_time_s', 'result', 'hyperparameters', 'best_config', 'start_datetime', 'end_datetime', 'start_timestamp']

kGridSiteMetadataFileName = 'userJobMetadata.json' #jobReport.json


#####################################################
################    Deprecated      #################
#####################################################

'''
try:
    from hpogrid.utils.grid_site_info import GridSiteInfo
    kGPUGridSiteList = GridSiteInfo.list_sites()
    kGPUGridSiteList += ['ANALY_CERN-PTEST','ANY', 'UKI-NORTHGRID-MAN-HEP']
except:
    kGPUGridSiteList = None

kStableGPUGridSiteList = ['ANALY_MANC_GPU_TEST', 'ANALY_MWT2_GPU', 'DESY-HH_GPU']
kDefaultGridSite = ','.join(kStableGPUGridSiteList)
'''