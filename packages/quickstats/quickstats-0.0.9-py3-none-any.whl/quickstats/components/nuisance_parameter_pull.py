import os
import time
import json
import fnmatch

import uproot
import numpy as np

from quickstats.components import CLIParser, ExtendedModel, ExtendedMinimizer
from quickstats.utils import root_utils, common_utils

import ROOT

class NuisanceParameterPull(object):
    _CLI_USAGE_          = 'quickstats run_pulls [-h|--help] [<args>]'
    _CLI_DESCRIPTION_    = 'Tool for computing the impact of a given NP to a set of POIs'    
    _CLI_ARG_OPTIONS_    = \
        {
            'input_file': {
                'abbr'        : 'i',
                'description' : 'Path to the input workspace file',
                'required'    : True,
                'type'        : str
            },
            'workspace':{
                'abbr'        : 'w',
                'description' : 'Name of workspace',
                'required'    : False,
                'type'        : str,
                'default'     : 'combWS'
            },
            'model_config':{
                'abbr'        : 'm',
                'description' : 'Name of model config',
                'required'    : False,
                'type'        : str,
                'default'     : 'ModelConfig'
            },  
            'data':{
                'abbr'        : 'd',
                'description' : 'Name of dataset',
                'required'    : False,
                'type'        : str,
                'default'     : 'combData'
            },
            'parameter'  : {
                'abbr'        : 'p',
                'description' : 'Nuisance parameter(s) to run pulls on.' +\
                                'Multiple parameters are separated by commas.' +\
                                'Wildcards are accepted', 
                'required'    : False,
                'type'        : str,
                'default'     : ''
            },   
            'poi': {
                'abbr'        : 'x',
                'description' : 'POIs to measure',
                'required'    : False,
                'type'        : str,
                'default'     : ""
            },
            'profile': {
                'abbr'        : 'r',
                'description' : 'Parameters to profile', 
                'required'    : False,
                'type'        : str,
                'default'     : ""
            },
            'fix': {
                'abbr'        : 'f',
                'description' : 'Parameters to fix', 
                'required'    : False,
                'type'        : str,
                'default'     : ""
            },
            'snapshot': {
                'abbr'        : 's',
                'description' : 'Name of initial snapshot', 
                'required'    : False,
                'type'        : str,
                'default'     : "nominalNuis"
            },
            'outdir': {
                'abbr'        : 'o',
                'description' : 'Output directory', 
                'required'    : False,
                'type'        : str,
                'default'     : "output"
            },
            'minimizer_type'  : {
                'abbr'        : 't',
                'description' : 'Minimizer type', 
                'required'    : False,
                'type'        : str,
                'default'     : "Minuit2"
            },        
            'minimizer_algo'  : {
                'abbr'        : 'a',
                'description' : 'Minimizer algorithm', 
                'required'    : False,
                'type'        : str,
                'default'     : "Migrad"
            },          
            'num_cpu'  : {
                'abbr'        : 'c',
                'description' : 'Number of CPUs to use', 
                'required'    : False,
                'type'        : int,
                'default'     : 1
            },   
            'binned'  : {
                'abbr'        : 'b',
                'description' : 'Binned likelihood', 
                'required'    : False,
                'type'        : int,
                'default'     : 1
            },    
            'precision'  : {
                'abbr'        : 'q',
                'description' : 'Precision for scan', 
                'required'    : False,
                'type'        : float,
                'default'     : 0.001
            },          
            'eps'  : {
                'abbr'        : 'e',
                'description' : 'Convergence criterium', 
                'required'    : False,
                'type'        : float,
                'default'     : 1.0
            },              
            'log_level'  : {
                'abbr'        : 'l',
                'description' : 'Log level', 
                'required'    : False,
                'type'        : str,
                'default'     : "INFO"
            },      
            'eigen'  : {
                'abbr'        : None,
                'description' : 'Compute eigenvalues and vectors', 
                'required'    : False,
                'type'        : int,
                'default'     : 0
            },   
            'strategy'  : {
                'abbr'        : None,
                'description' : 'default strategy', 
                'required'    : False,
                'type'        : int,
                'default'     : 0
            },
            'fix_cache'  : {
                'abbr'        : None,
                'description' : 'Fix StarMomentMorph cache', 
                'required'    : False,
                'type'        : int,
                'default'     : 1
            },    
            'fix_multi'  : {
                'abbr'        : None,
                'description' : 'Fix MultiPdf level 2', 
                'required'    : False,
                'type'        : int,
                'default'     : 1
            },            
            'offset'  : {
                'abbr'        : None,
                'description' : 'Offset likelihood', 
                'required'    : False,
                'type'        : int,
                'default'     : 1
            },  
            'optimize'  : {
                'abbr'        : None,
                'description' : 'Optimize constant terms', 
                'required'    : False,
                'type'        : int,
                'default'     : 2
            },       
            'max_calls'  : {
                'abbr'        : None,
                'description' : 'Maximum number of function calls', 
                'required'    : False,
                'type'        : int,
                'default'     : -1
            }, 
            'max_iters'  : {
                'abbr'        : None,
                'description' : 'Maximum number of Minuit iterations', 
                'required'    : False,
                'type'        : int,
                'default'     : -1
            },       
            'parallel'  : {
                'abbr'        : None,
                'description' : 'Parallelize job across different nuisance parameters using N workers.'+\
                                'Use -1 for N_CPU workers.', 
                'required'    : False,
                'type'        : int,
                'default'     : 0
            },                 
        } 
    
    @property
    def model(self):
        return self._model
    
    @property
    def workspace(self):
        return self._workspace
    @property
    def model_config(self):
        return self._model_config
    @property
    def pdf(self):
        return self._pdf
    @property
    def data(self):
        return self._data
    @property
    def nuisance_parameters(self):
        return self._nuisance_parameters
    @property
    def global_observables(self):
        return self._global_observables
    @property
    def pois(self):
        return self._pois
    @property
    def observables(self):
        return self._observables  
    
    def __init__(self):
        self._model               = None
        self._workspace           = None
        self._model_config        = None
        self._pdf                 = None
        self._data                = None
        self._nuisance_parameters = None
        self._global_observables  = None
        self._pois                = None
        self._observables         = None
    
    def get_parser(self, **kwargs):
        parser = CLIParser(description=self._CLI_DESCRIPTION_,
                           usage=self._CLI_USAGE_)
        parser.load_argument_options(self._CLI_ARG_OPTIONS_)
        return parser
    
    def run_parser(self, args=None):
        parser = self.get_parser()
        kwargs = vars(parser.parse_args(args))
        self.run_pulls(**kwargs)
    
    @staticmethod
    def evaluate_impact(model:ExtendedModel, minimizer:ExtendedMinimizer,
                        nuis, nominal_value, pois, minimizer_options, snapshot=None):
        poi_values = []
        start_time = time.time()
        if snapshot:
            model.workspace.loadSnapshot(snapshot)
        nuis.setVal(nominal_value)
        nuis.setConstant(1)   
        minimizer.minimize(**minimizer_options)
        for poi in pois:
            poi_values.append(poi.getVal())
        elapsed_time = time.time() - start_time
        return poi_values, elapsed_time
    
    @staticmethod
    def _run_pulls(input_file:str, workspace:str, model_config:str, data:str,
                   snapshot:str, nuis_name:str, poi_name:str, 
                   fix_param:str='', profile_param:str='', binned:bool=True,
                   minimizer_type:str='Minuit2', minimizer_algo:str='Migrad', 
                   precision:float=0.001, eps:float=1.0, strategy:int=0, 
                   num_cpu:int=1, offset:int=1, optimize:int=2, eigen:bool=False,
                   fix_cache:bool=True, fix_multi:bool=True, max_calls:int=-1, 
                   max_iters:int=-1, outdir:str='output', **kwargs):
        start_time = time.time()
        snapshot_names = snapshot.split(',')
        # load model
        model = ExtendedModel(model_name="model", fname=input_file, ws_name=workspace,
                              model_config_name=model_config, data_name=data, 
                              snapshot_names=snapshot_names, binned_likelihood=binned,
                              tag_as_measurement="pdf_", fix_cache=fix_cache, fix_multi=fix_multi)
        if fix_param:
            model.fix_parameters(fix_param)
            
        # by default fix all POIs before floating
        model.set_parameter_defaults(model.pois, error=0.15, constant=1, remove_range=True)
        for param in model.pois:
            extra_str = 'Fixing' if param.isConstant() else 'Set'
            print('INFO: {} POI {} at value {}'.format(extra_str, param.GetName(), param.getVal()))
        
        # collect pois
        rank_pois = model.profile_parameters(poi_name)
        model.set_parameter_defaults(rank_pois, error=0.15)     
        
        # profile pois
        if profile_param:
            print('INFO: Profiling POIs')
            profile_pois = model.profile_parameters(profile)
        
        buffer_time = time.time()
    
        nuip = model.workspace.var(nuis_name)
        if not nuip:
            raise ValueError('Nuisance parameter "{}" does not exist'.format(parameter))
        nuip_name = nuip.GetName()
        nuip.setConstant(0)
        print('INFO: Computing error for parameter "{}" at {}'.format(nuip.GetName(), nuip.getVal()))
        
        print("INFO: Making ExtendedMinimizer for unconditional fit")
        minimizer = ExtendedMinimizer("minimizer", model.pdf, model.data)
        print("INFO: Starting minimization")
        nll_commands = [ROOT.RooFit.NumCPU(num_cpu, 3), 
                        ROOT.RooFit.Constrain(model.nuisance_parameters),
                        ROOT.RooFit.GlobalObservables(model.global_observables), 
                        ROOT.RooFit.Offset(offset)]

        minimize_options = {
            'minimizer_type'   : minimizer_type,
            'minimizer_algo'   : minimizer_algo,
            'default_strategy' : strategy,
            'opt_const'        : optimize,
            'precision'        : precision,
            'eps'              : eps,
            'max_calls'        : max_calls,
            'max_iters'        : max_iters,
        }

        minimizer.minimize(nll_commands=nll_commands,
                           scan=1, scan_set=ROOT.RooArgSet(nuip),
                           **minimize_options)
        unconditional_time = time.time() - buffer_time
        print("INFO: Fitting time: {:.3f} s".format(unconditional_time))
        pois_hat = []
        for rank_poi in rank_pois:
            name = rank_poi.GetName()
            value = rank_poi.getVal()
            pois_hat.append(value)
            print('{} {}'.format(name, value))
        
        model.workspace.saveSnapshot('tmp_snapshot', model.pdf.getParameters(model.data))
        print('INFO: Made unconditional snapshot with name tmp_snapshot')
        
        # find prefit variation
        buffer_time = time.time()
        
        nuip_hat = nuip.getVal()
        nuip_errup = nuip.getErrorHi()
        nuip_errdown = nuip.getErrorLo()

        all_constraints = model.get_all_constraints()
        prefit_variation, constraint_type, nuip_nom = model.inspect_constrained_nuisance_parameter(nuip, all_constraints)
        if not constraint_type:
            print('INFO: Not a constrained parameter. No prefit impact can be determined. Use postfit impact instead.')
        prefit_uncertainty_time = time.time() - buffer_time
        print('INFO: Time to find prefit variation: {:.3f} s'.format(prefit_uncertainty_time))
        
        if rank_pois:
            new_minimizer_options = {
                'nll_commands': nll_commands,
                'reuse_nll'   : 1,
                **minimize_options
            }
            # fix theta at the MLE value +/- postfit uncertainty and minimize again to estimate the change in the POI
            print('INFO: Evaluating effect of moving {} up by {} + {}'.format(nuip_name, nuip_hat, nuip_errup))
            pois_up, postfit_up_impact_time = NuisanceParameterPull.evaluate_impact(model, minimizer,
                                                nuip, nuip_hat + abs(nuip_errup), rank_pois,
                                                new_minimizer_options,  'tmp_snapshot')
            print('INFO: Time to find postfit up impact: {:.3f} s'.format(postfit_up_impact_time))
            
            print('INFO: Evaluating effect of moving {} down by {} - {}'.format(nuip_name, nuip_hat, nuip_errup))
            pois_down, postfit_down_impact_time = NuisanceParameterPull.evaluate_impact(model, minimizer,
                                                    nuip, nuip_hat - abs(nuip_errdown), rank_pois,
                                                    new_minimizer_options,  'tmp_snapshot')
            print('INFO: Time to find postfit down impact: {:.3f} s'.format(postfit_down_impact_time))
            
            # fix theta at the MLE value +/- prefit uncertainty and minimize again to estimate the change in the POI
            
            if constraint_type:
                print('Evaluating effect of moving {} up by {} + {}'.format(nuip_name, nuip_hat, prefit_variation))
                pois_nom_up, prefit_up_impact_time = NuisanceParameterPull.evaluate_impact(model, minimizer,
                                                        nuip, nuip_hat + prefit_variation, rank_pois,
                                                        new_minimizer_options,  'tmp_snapshot')
                print('INFO: Time to find prefit up impact: {:.3f} s'.format(prefit_up_impact_time))      
                
                print('Evaluating effect of moving {} down by {} - {}'.format(nuip_name, nuip_hat, prefit_variation))
                pois_nom_down, prefit_down_impact_time = NuisanceParameterPull.evaluate_impact(model, minimizer,
                                                            nuip, nuip_hat - prefit_variation, rank_pois,
                                                            new_minimizer_options,  'tmp_snapshot')
                print('INFO: Time to find prefit down impact: {:.3f} s'.format(prefit_up_impact_time))
            else:
                print('WARNING: Prefit impact not estimated, instead postfit impact is cloned')
                pois_nom_up = [i for i in pois_up]
                pois_nom_down = [i for i in pois_down]
        else:
            pois_up, pois_down, pois_nom_up, pois_nom_down = [], [], [], []
        
        end_time = time.time()
        print('\nINFO: Time to perform all fits: {:.3f} s'.format(end_time-start_time))
        print('INFO: Unconditional minimum of NP {}: {} + {} - {}'.format(nuis_name, nuip_hat, 
              abs(nuip_errup), abs(nuip_errdown)))
        print('INFO: Prefit uncertainy of NP {}: {} +/- {}'.format(nuis_name, nuip_hat, prefit_variation))
        for i, rank_poi in enumerate(rank_pois):
            print('INFO: Unconditional minimum of POI {}: {}'.format(rank_poi.GetName(), pois_hat[i]))
            print('INFO: POI when varying NP up by 1 sigma postfit (prefit): {} ({})'.format(pois_up[i], pois_nom_up[i]))
            print('INFO: POI when varying NP down by 1 sigma postfit (prefit): {} ({})'.format(pois_down[i], pois_nom_down[i]))

        # create output directory if not exists
        pulls_out_dir = os.path.join(outdir, 'pulls')
        if not os.path.exists(outdir):
            os.makedirs(outdir)
            
        # store result in root file
        outname_root = os.path.join(outdir, nuis_name + '.root')
        
        result = {}
        result['nuis'] = {  'nuisance'   : nuis_name,
                            'nuis_nom'   : nuip_nom,
                            'nuis_hat'   : nuip_hat,
                            'nuis_hi'    : nuip_errup,
                            'nuis_lo'    : nuip_errdown,
                            'nuis_prefit': prefit_variation}
        result['pois'] = {}
        for i, rank_poi in enumerate(rank_pois):
            name = rank_poi.GetName()
            result['pois'][name] = { 'hat'     : pois_hat[i],
                                     'up'      : pois_up[i],
                                     'down'    : pois_down[i],
                                     'up_nom'  : pois_nom_up[i],
                                     'down_nom': pois_nom_down[i]}
            
        result_for_root = {}
        result_for_root.update(result['nuis'])
        for k,v in result['pois'].items():
            buffer = {'{}_{}'.format(k, kk): vv for kk,vv in v.items()}
            result_for_root.update(buffer)
        r_file = ROOT.TFile(outname_root, "RECREATE")
        r_tree = ROOT.TTree("result", "result")
        root_utils.fill_branch(r_tree, result_for_root)
        r_file.Write()
        r_file.Close()
        print('INFO: Saved output to {}'.format(outname_root))
        outname_json = os.path.join(outdir, nuis_name + '.json')
        json.dump(result, open(outname_json, 'w'), indent=2)
        

        
    def run_pulls(self, input_file='workspace.root', workspace='combWS', model_config='ModelConfig',
                 data='combData', poi='', snapshot='nominalNuis', outdir='output', profile="",
                 fix='', minimizer_type='Minuit2', minimizer_algo='Migrad', num_cpu=1, binned=1,
                 precision=0.001, eps=1.0, log_level='INFO', eigen=0, strategy=0, fix_cache=1, fix_multi=1,
                 offset=1, optimize=2, parameter="", max_calls=-1, max_iters=-1, parallel=0, **kwargs):
        
        start_time = time.time()
        
        # configure default minimizer options
        ExtendedMinimizer._configure_default_minimizer_options(minimizer_type, minimizer_algo,
            strategy, debug_mode=(log_level=="DEBUG"))
        
        
        nuis_list = ExtendedModel.get_nuisance_parameter_names(input_file, workspace, model_config)
        nuis_patterns = parameter.split(',')
        if parameter:
            nuis_names = []
            for nuis_name in nuis_list:
                # filter out nuisance parameters
                if any(fnmatch.fnmatch(nuis_name, nuis_pattern) for nuis_pattern in nuis_patterns):
                    nuis_names.append(nuis_name)
        else:
            nuis_names = nuis_list
                
        if parallel:
            from itertools import repeat
            arguments = (repeat(input_file), repeat(workspace), repeat(model_config),
                         repeat(data), repeat(snapshot), nuis_names, repeat(poi),
                         repeat(fix), repeat(profile), repeat(binned),
                         repeat(minimizer_type), repeat(minimizer_algo), repeat(precision),
                         repeat(eps), repeat(strategy), repeat(num_cpu), repeat(offset),
                         repeat(optimize), repeat(eigen), repeat(fix_cache), repeat(fix_multi),
                         repeat(max_calls), repeat(max_iters), repeat(outdir))
            max_workers = parallel if parallel != -1 else common_utils.get_cpu_count()
            common_utils.parallel_run(self._run_pulls, *arguments, max_workers=max_workers)
        else:
            for nuis_name in nuis_names:
                self._run_pulls(input_file, workspace, model_config, data, snapshot,
                                nuis_name, poi, fix, profile, binned, minimizer_type, 
                                minimizer_algo, precision, eps, strategy, num_cpu, offset, 
                                optimize, eigen, fix_cache, fix_multi, max_calls, max_iters, outdir)
        end_time = time.time()
        print('INFO: All jobs have finished. Total Time taken: {:.3f} s'.format(end_time-start_time))
        
    @staticmethod
    def parse_root_result(fname):
        with uproot.open(fname) as file:
            result = root_utils.uproot_to_dict(file)
        return result