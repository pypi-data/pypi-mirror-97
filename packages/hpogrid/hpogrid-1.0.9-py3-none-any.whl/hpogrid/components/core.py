from typing import Dict, Optional, Union

from hpogrid.utils import helper

def submit(config_input:Union[Dict, str], n_jobs:int=1,
           site:Optional[str]=None, time:int=-1, mode:str='grid'):
    from hpogrid import GridHandler
    GridHandler.submit_job(config_input,
                           n_jobs=n_jobs,
                           site=site,
                           time=time)

def sites(**kwargs):
    from hpogrid import GridSiteInfo
    GridSiteInfo.show(**kwargs)
    
    
def create_project(config:Dict, action:str='create'):
    from hpogrid import ProjectConfiguration
    ProjectConfiguration.save(config, action=action)
    
def run(config_input: [Dict, str],
        search_points=None,
        mode='local'):
    from hpogrid import JobBuilder
    job = JobBuilder.from_input(config_input=config_input,
                                search_points=search_points,
                                mode=mode)
    job.run()