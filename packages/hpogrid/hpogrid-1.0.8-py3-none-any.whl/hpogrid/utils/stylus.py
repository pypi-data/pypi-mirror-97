"""
    Module for formatting tables, texts and figures used in hpogrid
"""

from tabulate import tabulate
import pandas as pd
import yaml
import copy

kDefaultTableStyle = 'psql'
kDefaultStrAlign = 'left'

class ColorCode():
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
    
    
def type2str(typevar):
    if isinstance(typevar, tuple):
        return ', '.join([t.__name__ for t in typevar])
    else:
        return typevar.__name__    

def join_options(options):
    return ' '.join(["--{} {}".format(key,value) for (key,value) in options.items()])

def create_table(data, columns=None, indexed=True, transpose=False,
    tableformat=kDefaultTableStyle, stralign=kDefaultStrAlign):
    df = pd.DataFrame(data, columns=columns)
    if transpose:
        df = df.transpose()
    table = tabulate(df, showindex=indexed, headers=df.columns, 
        tablefmt=tableformat,
        stralign=stralign)
    return table

def create_formatted_dict(data, columns=None, indexed=True, transpose=False,
    tableformat=kDefaultTableStyle, stralign=kDefaultStrAlign):
    _data = copy.deepcopy(data)
    if isinstance(_data, dict):
        for key in _data:
            if isinstance(_data[key], dict):
                _data[key] = yaml.dump(_data[key], allow_unicode=True,
                                       default_flow_style=False, sort_keys=False)
    df = pd.DataFrame(_data.items(), columns=columns)
    if transpose:
        df = df.transpose()
    
    table = tabulate(df, showindex=indexed, headers=df.columns, 
        tablefmt=tableformat,
        stralign=stralign)
    return table