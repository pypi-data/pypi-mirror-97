import os
import sys
import ssl
import json
#import re
import fnmatch

from tqdm import tqdm
import argparse
import datetime
import pandas as pd

try:
    from urllib.parse import urlencode
    from urllib.parse import urljoin
    from urllib.request import urlopen, Request
    from urllib.error import HTTPError, URLError
except ImportError:
    from urllib import urlencode
    from urllib2 import urlopen, Request, HTTPError, URLError
    from urlparse import urljoin

from tabulate import tabulate
from colorama import Fore, Back, Style

try:
    from pandatools import PBookCore
    from pandatools import Client
    from pandatools.PBookCore import PsubUtils
except:
    raise ImportError('No module named \'pandatools\'. Please do '
        '\'setupATLAS\' and \'lsetup panda\' first ')
    
from hpogrid.utils.cli_parser import CLIParser

kPanDA_URL = 'https://bigpanda.cern.ch/'
kPanDA_TaskURL = 'https://bigpanda.cern.ch/tasks/'
kPanDA_JobURL = 'https://bigpanda.cern.ch/jobs/'

kPanDAVerifyPath = {
    'cafile' : '/etc/pki/tls/cert.pem',
    'capath' : '/etc/pki/tls/certs',
}

kHeaders = {'Accept': 'application/json', 'Content-Type':'application/json'}


kTaskActiveSuperstatusList = ['running', 'submitting', 'registered', 'ready']
KTaskFinalSuperstatusList = ['finished', 'failed', 'done', 'broken', 'aborted']
kStandardColumns = ['jeditaskid', 'status', 'pctfinished','taskname']
kOutputColumns = ['jeditaskid', 'status', 'taskname', 'computingsite', 'site', 'metastruct']

kStatusLen = 8
kLine = '_'*90
kStrf = '{jeditaskid:>10}  {status:<{l}}  {pctfinished:>5} {taskname}'
kHead = kStrf.format(l=kStatusLen, status='Status', jeditaskid='JediTaskID',
    pctfinished='Fin%', taskname='TaskName') +'\n' + kLine

RED = '\033[0;91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
BLINK = '\033[5m'
kColorDict = {
    'running': BLUE + BOLD,
    'submitting': CYAN,
    'registered': MAGENTA,
    'ready': MAGENTA,
    'pending': MAGENTA,
    'done': GREEN,
    'finished': YELLOW,
    'broken': RED + BOLD ,
    'exhausted': RED,
    'aborted': RED,
    'failed': RED,
    }


class PandaTaskManager():

    _ACTION_HELP_MESSAGE_ = {
        'show': 'Display PanDA task status',
        'kill': 'Kill a task by JediTaskID',
        'retry': 'Retry a task by JediTaskID',
        'killAndRetry': 'Kill and retry a task by JediTaskID',
    }    

    _USAGE_ = 'hpogrid tasks [-h|--help] {action} [<args>]'
    _DESCRIPTION_ = 'Tool for PanDA task management'    

    def __init__(self):
        print('INFO: Verifying Grid Proxy...')
        self.pbook = PBookCore.PBookCore()
        print('INFO: Verification is Successful.')
        self.context = ssl.SSLContext()
        #self.context = ssl._create_unverified_context()
        self.context.load_verify_locations(**kPanDAVerifyPath)
            
    def get_parser(self, **kwargs):
        usage_str = self._USAGE_.format(action='<action>')
        parser = CLIParser(description=self._DESCRIPTION_,
                           usage=usage_str, **kwargs) 
        parser.set_title('The most commonly used actions are')
        action_subparser = parser.add_subparsers(dest="action", parser_class=CLIParser)   

        action_parsers = {}
        for action, msg in self._ACTION_HELP_MESSAGE_.items():
            usage_str = self._USAGE_.format(action=action)
            args = {'help': msg, 'description': msg, 'usage': usage_str, 'prog': usage_str}
            action_parsers[action] = action_subparser.add_parser(action, **args)  
            
        action_parsers['show'].add_argument('-u','--username',
            help='filter tasks by username')
        action_parsers['show'].add_argument('-l','--limit', type=int, default=1000,
            help='the maximum number of tasks to query')
        action_parsers['show'].add_argument('-d', '--days', type=int, default=30,
            help='filter tasks within the recent N days')
        action_parsers['show'].add_argument('-n', '--taskname', 
            help='filter tasks by taskname (accept wildcards)')
        action_parsers['show'].add_argument('-i', '--jeditaskid',
            help='only show the task with the specified jeditaskid')
        action_parsers['show'].add_argument('-m', '--metadata', action='store_true',
            help='print out the metadata of a task')
        action_parsers['show'].add_argument('-s', '--status', nargs='+',
            help='filter tasks by task status')
        action_parsers['show'].add_argument('-y', '--sync', action='store_true',
            help='force no caching on the PanDA server')
        action_parsers['show'].add_argument('-r', '--taskid_range',
            help='filter tasks by jeditaskid range')
        action_parsers['show'].add_argument('-o', '--output',
            help='output result with the filename if specified')
        action_parsers['show'].add_argument('-c', '--outcol',
            help='data columns to be saved in output',
            default=kOutputColumns)
        
        for action in ['kill', 'retry', 'killAndRetry']:
            action_parsers[action].add_argument('jeditaskid', help='JediTaskID of the task')   

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
        getattr(self, action)(args)        

    def get_response(self, req, out_json=True):
        response = urlopen(req, context=self.context).read().decode('utf-8')
        if out_json:
            response = json.loads(response)
        return response

    def get_request(self, base_url, params, headers=kHeaders):
        url = '{0}?{1}'.format(base_url, urlencode(params))
        req = Request(url, headers=headers)
        return req

    def get_request_url(self, req):
        url = req.get_full_url()
        return url


    def query_job_metadata(self, taskids):
        metadata = []
        pbar = tqdm(taskids)
        for tid in pbar:
            pbar.set_description("Processing taskid %s" % tid)
            metadata.append(Client.getUserJobMetadata(tid, verbose=0)[1])
        return metadata

    #deprecated
    def query_by_jeditaskid(self, taskids):
        params = {
            'json': 1,
            'status': 'done',
            'extra': 'metastruct'
        }
        if not isinstance(taskids, list):
            taskids = [taskids]
        response = []
        pbar = tqdm(taskids)
        for tid in pbar:
            pbar.set_description("Processing taskid %s" % tid)
            params['jeditaskid'] = tid
            req = self.get_request(kPanDA_TaskURL, params)
            response += self.get_response(req)
        return response



    def query_tasks(self, taskname=None, jeditaskid=None, username=None, limit=1000,
                    status=None, superstatus=None, days=30, sync=False, metadata=False, 
                    taskid_range=None, **args):
        if username is None:
            username = self.pbook.username
        
        _status = status if not isinstance(status, list) else None
        
        params = { 
        'json': 1,
        'limit':limit,
        'jeditaskid': jeditaskid,
        'username': username,
        'taskname': taskname,
        'status': _status,
        'superstatus': superstatus,
        'days': days
        }

        params = {k: v for k, v in params.items() if v is not None}
    
        if sync:
            params['sync'] = int(time.time())
        
        if metadata:
            params['extra'] = 'metastruct'
        

        print('INFO: Showing only max {} tasks in last {} days.'
            ' One can set "--days N" to see tasks in last N days,'
            ' \n      and "--limit M" to see at most M latest tasks'
            .format(limit, days))
        response = None
        req = self.get_request(kPanDA_TaskURL, params)
        response = self.get_response(req)

        n_jobs = len(response)
        
       # set_trace()
        if taskid_range:
            response = self.filter_range(response, taskid_range)
        if isinstance(status, list):
            response = self.filter_status(response, status)
        
        new_n_jobs = len(response)
        if metadata and (n_jobs > 100):
            print('INFO: Fetching metadata for {} jobs '
                'which is greater than the maximum limit (100). '
                'Number of jobs after filtering task id range and'
                ' task status is: {}.'
                'Need to fetch metadata individually which '
                'will be slower...\n'
                'TIPS: Try to filter tasks by their task names to '
                'remove irrelevant tasks. For example, if your '
                'tasks have names of the form user.USERNAME.'
                'PROJECTNAME.SOMETHING.ELSE, then you can use '
                '--taskname *.PROJECTNAME.* to filter jobs'.format(n_jobs,new_n_jobs))
            taskids = [res['jeditaskid'] for res in response]
            job_metadata_list = self.query_job_metadata(taskids)
            for task, job_metadata in zip(response, job_metadata_list):
                task['jobs_metadata'] = job_metadata
            """
            overflow_task_ids = [res['jeditaskid'] for res in response[100:]]
            params['limit'] = 100
            req = self.get_request(kPanDA_TaskURL, params)
            response = self.get_response(req)
            response += self.query_job_metadata(overflow_task_ids)
            """

        return response

    def set_status_color(self, params):
        status = params['status']
        color = kColorDict.get(status,ENDC)
        params['status'] = color+status+ENDC
        nonprlen = len(color) + len(ENDC)
        params['l'] = kStatusLen+nonprlen


    def print_standard(self, datasets):
        filtered_data = []
        print(kHead)
        for task in datasets:
            params = { k:task[k] for k in kStandardColumns if not k.startswith('pct')}
            params_pct = { k:'{0}%'.format(task['dsinfo'][k]) for k in kStandardColumns if k.startswith('pct')}
            params.update(params_pct)
            filtered_data.append(params.copy())
            self.set_status_color(params)
            print(kStrf.format(**params))
    @staticmethod
    def extract_metadata(datasets):
        metadata = {}
        # loop over tasks
        for task in datasets:
            # check if jobs metadata exists in a dataset
            if task.get('jobs_metadata',None):
                task_id = task.get('jeditaskid', None)
                if task_id is None:
                    raise ValueError('Unable to extract jeditaskid from url response')
                task_name = task.get('taskname', None)
                if task_name is None:
                    raise ValueError('Unable to extract taskname from url response')
                metadata[task_id] = {'taskname': task_name, 'jobs_metadata':{} }
                # loop over jobs in a task
                for job_id in task['jobs_metadata']:
                    # fill user job metadata from a job
                    metadata[task_id]['jobs_metadata'][job_id] = task['jobs_metadata'][job_id].get('user_job_metadata', {})
                        
        return metadata
    
    @staticmethod
    def print_metadata(datasets):
        metadata = PandaTaskManager.extract_metadata(datasets)
        for task_id in metadata:
            print('INFO: Printing metadata for task: {} (JediTaskID: {})'.format(metadata[task_id]['taskname'], task_id))
            for job_id in metadata[task_id]['jobs_metadata']:
                print('Job ID: {}'.format(job_id))
                print('User Job Metadata:\n{}\n'.format(metadata[task_id]['jobs_metadata'][job_id]))

    # filter task by jeditaskid range
    @staticmethod
    def filter_range(datasets, frange):
        r = frange.split('-')
        if frange[0] == '-':
            datasets = [ds for ds in datasets if int(ds['jeditaskid']) <= int(r[1])]
        elif frange[-1] == '-':
            datasets = [ds for ds in datasets if int(ds['jeditaskid']) >= int(r[0])]
        else:
            datasets = [ds for ds in datasets if int(ds['jeditaskid']) in range(int(r[0]),int(r[1]))]   
        return datasets
    
    # filter task by status
    @staticmethod
    def filter_status(datasets, status):
        if not isinstance(status, list):
            status = [status]
        datasets = [ds for ds in datasets if ds.get('status', None) in status]
        return datasets    

    def filter_datasets(self, datasets, col=kOutputColumns, out_type=list):
        df = pd.DataFrame(datasets)
        df = df.filter(col).transpose()
        if out_type is list:
            df_dict = df.to_dict()
            return [df_dict[key] for key in df_dict]
        elif out_type is dict:
            return df.to_dict()
        else:
            raise TypeError('output data type {} is not supported'.format(out_type))

    def save_datasets(self, datasets, out_path, col=kOutputColumns):
        with open(out_path, 'w') as outfile:
            out_dataset = self.filter_datasets(datasets, col, out_type=dict)
            json.dump(out_dataset, outfile)

    # show task status
    def show(self, args):
        output = args.pop('output', None)
        outcol = args.pop('outcol', None)
        print('INFO: Fetching PanDA Tasks...')
        datasets = self.query_tasks(**args)
        
        print('')
        self.print_standard(datasets)
        
        if args['metadata']:
            print('')
            self.print_metadata(datasets)       

        if output:
            self.save_datasets(datasets, output, col=outcol)


    def get_active_tasks(self):
        return pbookCore.get_active_tasks()

    def kill(self, args):
        task_id = int(args['jeditaskid'])
        self.pbook.kill(task_id)

    def retry(self, args):
        task_id = int(args['jeditaskid'])
        self.pbook.retry(task_id)

    def killAndRetry(self, args):
        task_id = int(args['jeditaskid'])
        self.pbook.killAndRetry(task_id)



    '''
    def deprecated_query(self, params):
                req = self.get_request(kPanDA_JobURL, params)
        response_status = self.get_response(req)['jobs']
        params['fields'] = 'metastruct'
        req = self.get_request(kPanDA_JobURL, params)
        response_metadata = self.get_response(req)['jobs']
        set_trace()
        response = []
        for (status, metadata) in zip(response_status, response_metadata):
            response.append({**status,**metadata})
    '''