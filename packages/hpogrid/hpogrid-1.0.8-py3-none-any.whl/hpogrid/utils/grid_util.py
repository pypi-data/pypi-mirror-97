import os
import json
import shutil
import subprocess

import tarfile
from pdb import set_trace

#import re
import fnmatch

from hpogrid.components.defaults import kDataDir
from hpogrid.utils import stylus


def extract_inputDS(in_path=kDataDir, out_path=kDataDir):
    tarfiles = [ f for f in os.listdir(in_path) if f.endswith('tar.gz')]
    for f in tarfiles:
        tar = tarfile.open(f, "r:gz")
        print('untaring the file {}'.format(f))
        tar.extractall(path=out_path)
        inputDS = tar.getnames()
        tar.close()

    return inputDS

def remove_inputDS(inputDS):
    for ds in inputDS:
        if os.path.isfile(ds):
            os.remove(ds)
        elif os.path.isdir(ds):
            shutil.rmtree(ds)

kDefultGridSiteType = ['analysis', 'unified']
kDefaultGridSiteInfo = ['state', 'status', 'maxinputsize', 'maxmemory', 'maxtime']

class GridSiteInfo():

    def __init__(self):
        if len(sys.argv) > 1:
            self.run_parser()

    def get_parser(self):
        parser = argparse.ArgumentParser(
                    formatter_class=argparse.RawDescriptionHelpFormatter)          
        parser.add_argument('-n', '--name_filter', help='filter grid site names')
        parser.add_argument('-g', '--non_gpu', action='store_true',
            help='show also non gpu sites')
        parser.add_argument('-a', '--non_active', action='store_true',
            help='show also non active sites')
        parser.add_argument('-t', '--site_type', nargs='+',
            help='filter sites by type', default=kDefultGridSiteType)
        parser.add_argument('-i', '--info', nargs='+',
            help='into to show', default=kDefaultGridSiteInfo)
        return parser

    def run_parser(self):
        parser = self.get_parser()
        args = parser.parse_args(sys.argv[2:])
        kwargs = vars(args)
        kwargs['gpu'] = not kwargs.pop('non_gpu', 'False')
        kwargs['active'] = not kwargs.pop('non_active', 'False')
        GridSiteInfo.show(**kwargs)

    @staticmethod
    def show(name_filter=None, gpu=True, active=True, site_type=kDefultGridSiteType,
        info=kDefaultGridSiteInfo):

        grid_site_info = GridSiteInfo.extract(name_filter, gpu, active, site_type, info)
        print(stylus.create_table(grid_site_info, transpose=True))

    @staticmethod
    def list_sites(name_filter=None, gpu=True, active=True, site_type=kDefultGridSiteType):
        grid_site_info = GridSiteInfo.extract(name_filter, gpu, active, site_type)
        return list(grid_site_info.keys())

    @staticmethod
    def extract(name_filter=None, gpu=True, active=True, site_type=kDefultGridSiteType,
        info=kDefaultGridSiteInfo):
        '''
        retrieve some basic information of PanDA grid sites
        '''
        try:
          jsonfileLocation = os.environ['ALRB_cvmfs_repo'] + '/sw/local/etc/agis_schedconf.json'
        except:
          jsonfileLocation = '/cvmfs/atlas.cern.ch/repo/sw/local/etc/agis_schedconf.json'

        with open(jsonfileLocation,'r') as jsonfile:
          jsondata = json.load(jsonfile)

        if name_filter is None:
            name_filter = '*'

        grid_site_info = {}

        for site in jsondata:
            # filter site names (could also match jsondata[site]['panda_resource'] instead)
            if not fnmatch.fnmatch(site, name_filter):
                continue
            # filter non-active grid sites
            if active and (not jsondata[site]['state'] == 'ACTIVE'):
                continue
            # no good indicator of a GPU site yet will just judge on site name
            if gpu and (not 'GPU' in jsondata[site]['panda_resource']):
                continue
            if jsondata[site]['type'] not in site_type:
                continue
            grid_site_info[site] = {key: jsondata[site][key] for key in info}

        return grid_site_info