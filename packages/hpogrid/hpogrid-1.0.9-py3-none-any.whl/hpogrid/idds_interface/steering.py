import os
import sys
import json
from typing import List, Dict
import numpy as np
import argparse

from hpogrid.utils.cli_parser import CLIParser

kDefaultGenerator = 'nevergrad'
kDefaultMetric = 'loss'
kDefaultMode = 'min'

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.bool_):
            return bool(obj)            
        else:
            return super(NpEncoder, self).default(obj)

class SteeringIDDS():
    
    _USAGE_ = 'hpogrid generate [<args>]'
    _DESCRIPTION_ = 'Tool for generation of hyperparamter search points based on input search space'
    
    def __init__(self):
        pass

    def get_parser(self, **kwargs):
        parser = CLIParser(description=self._DESCRIPTION_,
                           usage=self._USAGE_, **kwargs) 
        parser.add_argument('-l', '--lib', default=kDefaultGenerator,
            help='library to use')  
        parser.add_argument('-s', '--space',
            help='search space json file')
        parser.add_argument('-n', '--n_point', type=int, required=True,
            help='number of points to generate')
        parser.add_argument('-m', '--max_point', type=int,
            help='maximum number of points to generate in entire iDDS workflow')
        parser.add_argument('-e', '--metric', default=kDefaultMetric,
            help='evaluation metric')
        parser.add_argument('-d', '--mode', default=kDefaultMode,
            help='evaluation mode')
        parser.add_argument('-i', '--infile', help='iDDS input')
        parser.add_argument('-o', '--outfile', help='iDDS output')
        parser.add_argument('--method', help='optimizer type (nevergrad only)')
        return parser
    
    def run_parser(self, args=None):
        parser = self.get_parser()
        args, extra = parser.parse_known_args(args)
        args = vars(args)
        self.run_generator(**args)    

    def get_generator(self, space, metric=kDefaultMetric, mode=kDefaultMode, lib=kDefaultGenerator, **args):
        if lib == 'nevergrad':
            from hpogrid.generator.nevergrad_generator import NeverGradGenerator
            return NeverGradGenerator(space, metric, mode, **args)
        elif lib == 'skopt':
            from hpogrid.generator.skopt_generator import SkOptGenerator
            return SkOptGenerator(space, metric, mode, **args)
        elif lib == 'hyperopt':
            from hpogrid.generator.hyperopt_generator import HyperOptGenerator
            return HyperOptGenerator(space, metric, mode, **args)
        elif lib == 'ax':
            from hpogrid.generator.ax_generator import AxGenerator
            return AxGenerator(space, metric, mode, **args)
        elif lib == 'bohb':
            from hpogrid.generator.bohb_generator import BOHBGenerator
            return BOHBGenerator(space, metric, mode, **args) 
        elif lib == 'grid':
            from hpogrid.generator.grid_generator import GridGenerator
            return GridGenerator(space, metric, mode, **args)         
        else:
            raise ValueError('Generator from library {} is not supported'.format(lib))

    def validate_idds_input(self, idds_input):
        '''
        old format
        {"points": [[{hyperparameter_point_1}, <loss_or_None>], ..., [{hyperparameter_point_N}, <loss_or_None>]], "opt_space": <opt space>}
        new format
        {"points": [[[<model_id_1>, {hyperparameter_point_1}], <loss_or_None>], ..., [[<model_id_N>, {hyperparameter_point_N}], <loss_or_None>]], "opt_space": ["model_id": <model_id>, "search_space": <search_space>]}
        '''
        keys = ['points', 'opt_space']
        # check main keys
        for key in keys:
            if key not in idds_input:
                raise KeyError('Key {} not found in idds input.'
                    ' Please check idds input format'.format(key))
        if not isinstance(idds_input['points'], List):
            raise ValueError('idds should have the data structure: Dict[List[...]]')

        for point in idds_input['points']:
            if not isinstance(point, List):
                raise ValueError('idds should have the data structure: Dict[List[List[...]]]')
            
            if (not isinstance(point[0], Dict)) and (not (isinstance(point[0], List) and isinstance(point[0][0], int) and isinstance(point[0][1], Dict))):
                raise ValueError('idds should have the data structure: Dict[List[List[Dict, Value]]] or Dict[List[List[List[int, Dict], Value]]]')
        # old format
        if isinstance(idds_input['opt_space'], Dict):
            return 1
        # new format
        elif isinstance(idds_input['opt_space'], List):
            for search_space in idds_input['opt_space']:
                if not isinstance(search_space, Dict):
                    raise ValueError('idds search space should be a dictionary not {}'.format(type(search_space)))
            return 2
        else:
            raise ValueError('invalid format for idds opt_space')

    def parse_idds_input(self, file):
        if not file:
            return None

        with open(file,'r') as input_file:
            idds_data = json.load(input_file)
            
        idds_format = self.validate_idds_input(idds_data)
        
        # old format
        if idds_format == 1:
            points = []
            results = []
            pending = 0
            input_data = idds_data['points']
            for data in input_data:
                point, result = data[0], data[1]
                points.append(point)
                results.append(result)
            search_space = idds_data.get('opt_space', None)
            return (points, results, search_space)
        
        elif idds_format == 2:
            model_results = {}
            for opt_space in idds_data.get('opt_space', []):
                model_id = opt_space.get('model_id', None)
                search_space = opt_space.get('search_space', None)
                if model_id is None:
                    raise ValueError('Cannot extract model id from idds opt space')
                model_results[model_id] = {}
                model_results[model_id]['search_space'] = search_space
                model_results[model_id]['points'] = []
                model_results[model_id]['results'] = []
            for data in idds_data.get('points', []):
                model_id = data[0][0]
                if model_id not in model_results:
                    raise ValueError('missing search space definition for model id: {}'.format(model_id))
                point, result = data[0][1], data[1]
                model_results[model_id]['points'].append(point)
                model_results[model_id]['results'].append(result)
            return model_results
        else:
            raise RuntimeError('Failed to parse idds input')
    
    def generate_points(self, search_space, n_point, metric=kDefaultMetric, mode=kDefaultMode,
                            lib=kDefaultGenerator, max_point=None, points=None,
                            results=None, **args):
        
        if not search_space:
            raise RuntimeError('search space is not specified in either idds input or '
            'through command line argument')
        
        # create generator
        generator = self.get_generator(search_space, metric, mode, lib, **args)

        n_evaluated = 0
        n_pending = 0

        # feed evaluated points
        if points and results:
            generator.feed(points=points, results=results)
            print('INFO: Fed the following results to the {} optimizer'.format(lib))
            generator.show(points=points, results=results)
            n_pending = results.count(None)
            print('INFO: There are {} point(s) pending.'.format(n_pending))
            generator.show_pending(points=points, results=results)
            n_evaluated = len(points) 

        # determine number of points to generate
        max_point = 9999 or max_point
        n_remaining = max_point - n_evaluated 
        if n_remaining < 0:
            raise ValueError('there are already more evaluated points than the'
            ' maximum points to generate for idds workflow')
        if n_point - n_pending <= 0:
            print('INFO: There are more points pending than the number of points to generate. '
                  'No new points will be generated.')
            return []
        
        n_generate = min(n_point-n_pending, n_remaining)

        # generate points
        new_points = generator.ask(n_generate)
        print('INFO: Generated {} new points'.format(n_generate))
        generator.show(new_points)

        return new_points

    def run_generator(self, space, n_point, metric=kDefaultMetric,
                      mode=kDefaultMode, lib=kDefaultGenerator, max_point=None,
                      infile=None, outfile=None, **args):
        
        parsed_data = self.parse_idds_input(infile)
        
        # case no input points
        if parsed_data is None:
            if not space:
                raise ValueError('search space can not be empty')
            with open(space, 'r') as space_input:
                search_space = json.load(space_input)
            new_points = self.generate_points(search_space=search_space, n_point=n_point,
                                             metric=metric, mode=mode,
                                             lib=lib, max_point=max_point, **args)
        # old format
        elif isinstance(parsed_data, tuple):
            points, results, search_space = parsed_data[0], parsed_data[1], parsed_data[2]
            new_points = self.generate_points(search_space=search_space, n_point=n_point,
                                             metric=metric, mode=mode,
                                             lib=lib, max_point=max_point, 
                                             points=points, results=results, **args)
        elif isinstance(parsed_data, dict):
            new_points = []
            for model_id in parsed_data:
                print('Starting point generation for model ID: {}'.format(model_id))
                data = parsed_data[model_id]
                points, results, search_space = data["points"], data["results"], data["search_space"]
                model_specific_new_points = self.generate_points(search_space=search_space, n_point=n_point,
                                                                metric=metric, mode=mode,
                                                                lib=lib, max_point=max_point, 
                                                                points=points, results=results, **args)
                for point in model_specific_new_points:
                    new_points.append(tuple([model_id, point]))

        # save output
        if outfile:
            with open(outfile, 'w') as out:
                json.dump(new_points, out, indent=2, cls=NpEncoder)