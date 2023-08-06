##################################################################################################
# Based on https://gitlab.cern.ch/atlas-physics/stat/tools/StatisticsTools by Stefan Gadatsch
# Author: Alkaid Cheng
# Email: chi.lung.cheng@cern.ch
##################################################################################################
import os
import math
from typing import List, Optional

import ROOT

from quickstats.components.numerics import is_integer

class ExtendedModel(object):
    def __init__(self, model_name:str, fname:str, ws_name:str,
                 model_config_name:str, data_name:str, snapshot_names:List[str],
                 binned_likelihood:bool=True, tag_as_measurement:str="pdf_",
                 fix_cache:bool=True, fix_multi:bool=True,
                 interpolation_code:int=-1):
        self.fname = fname
        self.name = model_name
        self.ws_name = ws_name
        self.model_config_name = model_config_name
        self.data_name = data_name
        self.snapshot_names = snapshot_names
        self.binned_likelihood = binned_likelihood
        self.tag_as_measurement = tag_as_measurement
        self.fix_cache = fix_cache
        self.fix_multi = fix_multi
        self.interpolation_code = interpolation_code
        
        self.initialize()
  
    @property
    def file(self):
        return self._file
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
        
    @staticmethod
    def modify_interp_codes(ws, interp_code, classes=None):
        if classes is None:
            classes = [ROOT.RooStats.HistFactory.FlexibleInterpVar, ROOT.PiecewiseInterpolation]
        for component in ws.components():
            for cls in classes:
                if (component.IsA() == cls.Class()):
                    component.setAllInterpCodes(interp_code)
                    class_name = cls.Class_Name().split('::')[-1]
                    print('INFO: {} {} interpolation code set to {}'.format(component.GetName(),
                                                                            class_name,
                                                                            interp_code))
        return None

    @staticmethod
    def activate_binned_likelihood(ws):
        print('INFO: Activating binned likelihood evaluation')
        for component in ws.components():
            if (component.IsA() == ROOT.RooRealSumPdf.Class()):
                component.setAttribute('BinnedLikelihood')
                print('INFO: Activated binned likelihood attribute for {}'.format(component.GetName()))
        return None
                          
    @staticmethod
    def set_measurement(ws, condition):
        print('INFO: Activating measurements to reduce memory consumption')
        for component in ws.components():
            name = component.GetName()
            if ((component.IsA() == ROOT.RooAddPdf.Class()) and condition(name)):
                component.setAttribute('MAIN_MEASUREMENT')
                print('INFO: Activated main measurement attribute for {}'.format(name))
        return None
    
    @staticmethod
    def deactivate_lv2_const_optimization(ws, condition):
        print('INFO: Deactivating level 2 constant term optimization for specified pdfs')
        for component in ws.components():
            name = component.GetName()
            if (component.InheritsFrom(ROOT.RooAbsPdf.Class()) and condition(name)):
                component.setAttribute("NOCacheAndTrack")
                print('INFO: Deactivated level 2 constant term optimizatio for {}'.format(name))
    
    @staticmethod
    def get_nuisance_parameter_names(fname:str, ws_name:str, model_config_name:str):
        if not os.path.exists(fname):
            raise FileNotFoundError('workspace file {} does not exist'.format(fname))
        file = ROOT.TFile(fname) 
        if (not file):
            raise RuntimeError("Something went wrong while loading the root file: {}".format(fname))
        ws = file.Get(ws_name)
        if not ws:
            raise RuntimeError("Something went wrong while loading the workspace: {}".format(ws_name))
        model_config = ws.obj(model_config_name)
        if not model_config:
            raise RuntimeError('ERROR: Failed to load model config {}'.format(model_config_name))
        nuisance_parameters = model_config.GetNuisanceParameters()
        if not nuisance_parameters:
            raise RuntimeError('ERROR: Failed to load nuisance parameters')
        return [nuis.GetName() for nuis in nuisance_parameters]
            
    def initialize(self):
        if not os.path.exists(self.fname):
            raise FileNotFoundError('workspace file {} does not exist'.format(self.fname))
        print('Opening file: {}'.format(self.fname))
        file = ROOT.TFile(self.fname) 
        if (not file):
            raise RuntimeError("Something went wrong while loading the root file: {}".format(self.fname))
        print('Loading workspace: {}'.format(self.ws_name))
        ws = file.Get(self.ws_name)
        if not ws:
            raise RuntimeError("Something went wrong while loading the workspace: {}".format(self.ws_name))
        
        # modify interpolation code
        if self.interpolation_code != -1:
            self.modify_interp_codes(ws, self.interpolation_code,
                                     classes=[ROOT.RooStats.HistFactory.FlexibleInterpVar, ROOT.PiecewiseInterpolation])
        
        # activate binned likelihood
        if self.binned_likelihood:
            self.activate_binned_likelihood(ws)
        
        # set main measurement
        if self.tag_as_measurement:
            self.set_measurement(ws, condition=lambda name: name.startswith(self.tag_as_measurement))
                          
        # deactivate level 2 constant term optimization
            self.deactivate_lv2_const_optimization(ws, 
                condition=lambda name: (name.endswith('_mm') and 'mumu_atlas' in name))
                          
        # load model config
        model_config = ws.obj(self.model_config_name)
        if not model_config:
            raise RuntimeError('ERROR: Failed to load model config {}'.format(self.model_config_name))
        print('INFO: Loaded model config "{}" from workspace'.format(self.model_config_name))

        # load pdf
        pdf = model_config.GetPdf()
        if not pdf:
            raise RuntimeError('Failed to load pdf')
        print('INFO: Loaded model pdf "{}" from model config'.format(pdf.GetName()))
             
        # load dataset
        data = ws.data(self.data_name)
        if not data:
            raise RuntimeError('ERROR: Failed to load dataset')
        print('INFO: Loaded dataset "{}" from workspace'.format(data.GetName()))
                
        # load nuisance parameters
        nuisance_parameters = model_config.GetNuisanceParameters()
        if not nuisance_parameters:
            raise RuntimeError('ERROR: Failed to load nuisance parameters')
        print('INFO: Loaded nuisance parameters from model config')
                
        # Load global observables
        global_observables = model_config.GetGlobalObservables()
        if not global_observables:
            raise RuntimeError('ERROR: Failed to load global observables')          
        print('INFO: Loaded global observables from model config')                  
    
        # Load POIs
        pois = model_config.GetParametersOfInterest()
        if not pois:
            raise RuntimeError('ERROR: Failed to load parameters of interest')
        print('INFO: Loaded parameters of interest from model config')
                                  
        # Load observables
        observables = model_config.GetObservables()
        if not observables:
            raise RuntimeError('ERROR: Failed to load observables')     
        print('INFO: Loaded observables from model config')
        
        self._file                = file
        self._workspace           = ws
        self._model_config        = model_config
        self._pdf                 = pdf
        self._data                = data
        self._nuisance_parameters = nuisance_parameters
        self._global_observables  = global_observables
        self._pois                = pois
        self._observables         = observables
                          
        # Load snapshots
        if self.snapshot_names:
            for snapshot_name in self.snapshot_names:
                self._workspace.loadSnapshot(snapshot_name)
                print('INFO: Loaded snapshot "{}"'.format(snapshot_name))
        
        return None
                
    @staticmethod
    def _fix_parameters(source:"ROOT.RooArgSet", param_expr=None, param_str='parameter'):
        '''
            source: parameters instance
            param_expr: 
        '''            
        param_dict = ExtendedModel.parse_param_expr(param_expr)
        return ExtendedModel._set_parameters(source, param_dict, mode='fix', param_str=param_str)           
    
    @staticmethod
    def _profile_parameters(source:"ROOT.RooArgSet", param_expr=None, param_str='parameter'):
        '''
            source: parameters instance
            param_expr: 
        '''                          
        param_dict = ExtendedModel.parse_param_expr(param_expr)
        return ExtendedModel._set_parameters(source, param_dict, mode='free', param_str=param_str)   
    
    def fix_parameters(self, param_expr=None):
        return self._fix_parameters(self.workspace.allVars(), param_expr=param_expr,
                                    param_str='parameter')
    
    def profile_parameters(self, param_expr=None):
        profiled_parameters = self._profile_parameters(self.workspace.allVars(), param_expr=param_expr,
                                                       param_str='parameter') 
        if not profiled_parameters:
            print('Info: No parameters are profiled.')
        return profiled_parameters 
    
    def fix_nuisance_parameters(self, param_expr=None):
        return self._fix_parameters(self.nuisance_parameters, param_expr=param_expr,
                                    param_str='nuisance parameter')
                          
    def fix_parameters_of_interest(self, param_expr=None):
        return self._fix_parameters(self.pois, param_expr=param_expr, param_str='parameter of interest')

    def profile_parameters_of_interest(self, param_expr=None):
        return self._profile_parameters(self.pois, param_expr=param_expr, param_str='parameter of interest')
    
    @staticmethod
    def _set_parameters(source:"ROOT.RooArgSet", param_dict, mode=None, param_str='parameter'):
        set_parameters = []
        available_parameters = [param.GetName() for param in source]
        for name in param_dict:
            if name in available_parameters:
                ExtendedModel._set_parameter(source[name], param_dict[name], mode=mode, param_str=param_str)
                set_parameters.append(source[name])
            else:
                print('WARNING: Parameter "{}" does not exist. No modification will be made.'.format(name))
        return set_parameters
    
    @staticmethod
    def _set_parameter(param, value, mode=None, param_str='parameter'):
        name = param.GetName()
        old_value = param.getVal()
        new_value = old_value
        if isinstance(value, (float, int)):
            new_value = value
        elif isinstance(value, (list, tuple)):
            if len(value) == 3:
                new_value = value[0]
                v_min, v_max = value[1], value[2]
            elif len(value) == 2:
                v_min, v_max = value[0], value[1]
            else:
                raise ValueError('invalid expression for profiling parameter: {}'.format(value))
            # set range
            if (v_min is not None) and (v_max is not None):
                if (new_value < v_min) or (new_value > v_max):
                    new_value = (v_min + v_max)/2
                param.setRange(v_min, v_max)
                print('INFO: Set {} "{}" range to ({},{})'.format(param_str, name, v_min, v_max))
            elif (v_min is not None):
                if (new_value < v_min):
                    new_value = v_min
                # lower bound is zero, if original value is negative, will flip to positive value
                if (v_min == 0) and (old_value < 0):
                    new_value = abs(old_value)
                param.setMin(v_min)
                print('INFO: Set {} "{}" min value to ({},{})'.format(param_str, name, v_min))
            elif (v_max is not None):
                if (new_value > v_max):
                    new_value = v_max
                # upper bound is zero, if original value is positive, will flip to negative value
                if (v_max == 0) and (old_value > 0):
                    new_value = -abs(old_value)                    
                param.setMax(v_max)
                print('INFO: Set {} "{}" max value to ({},{})'.format(param_str, name, v_max))
        if new_value != old_value:
            param.setVal(new_Val)              
            print('INFO: Set {} "{}" value to {}'.format(param_str, name, new_value))
        if mode=='fix':
            param.setConstant(1)
            print('INFO: Fixed {} "{}" at value {}'.format(param_str, name, param.getVal()))
        elif mode=='free':
            param.setConstant(0)
            print('INFO: "{}" = [{}, {}]'.format(name, param.getMin(), param.getMax()))
        return None

    @staticmethod
    def set_parameter_defaults(source:"ROOT.RooArgSet", value=None, error=None, constant=None,
                               remove_range=None, target:List[str]=None):

        for param in source:
            if (not target) or (param.GetName() in target):
                if remove_range:
                    param.removeRange()            
                if value is not None:
                    param.setVal(value)
                if error is not None:
                    param.setError(error)
                if constant is not None:
                    param.setConstant(constant)
        return None
    
    @staticmethod
    def parse_param_expr(param_expr):
        param_dict = {}
        # if parameter expression is not empty string or None
        if param_expr: 
            if isinstance(param_expr, str):
                param_dict = ExtendedModel.parse_param_str(param_expr)
            elif isinstance(param_expr, dict):
                param_dict = param_dict
            else:
                raise ValueError('invalid format for parameter expression: {}'.format(param_expr))
        elif param_expr is None:
        # if param_expr is None, all parameters will be parsed as None by default
            param_dict = {param.GetName():None for param in source}
        return param_dict
                          
    @staticmethod
    def parse_param_str(param_str):
        '''
        Example: "param_1,param_2=0.5,param_3=-1,param_4=1,param_5=0:100,param_6=:100,param_7=0:"
        '''
        param_str = param_str.replace(' ', '')
        param_list = param_str.split(',')
        param_dict = {}
        for param_expr in param_list:
            expr = param_expr.split('=')
            # case only parameter name is given
            if len(expr) == 1:
                param_dict[expr[0]] = None
            # case both parameter name and value is given
            elif len(expr) == 2:
                param_name = expr[0]
                param_value = expr[1]
                # range like expression
                if ':' in param_value:
                    param_range = param_value.split(':')
                    if len(param_range) != 2:
                        raise ValueError('invalid parameter range: {}'.format(param_value))
                    param_min = float(param_range[0]) if param_range[0].isnumeric() else None
                    param_max = float(param_range[1]) if param_range[1].isnumeric() else None
                    param_dict[param_name] = [param_min, param_max]
                elif is_integer(param_value):
                    param_dict[param_name] = int(param_value)
                else:
                    param_dict[param_name] = float(param_value)
            else:
                raise ValueError('invalid parameter expression: {}'.format(param))
        return param_dict
    
    @staticmethod
    def find_unique_prod_components(root_pdf, components, recursion_count=0):
        if (recursion_count > 50):
            raise RuntimeError('find_unique_prod_components detected infinite loop')
        pdf_list = root_pdf.pdfList()
        if pdf_list.getSize() == 1:
            components.add(pdf_list)
            #print('ProdPdf {} is fundamental'.format(pdf_list.at(0).GetName()))
        else:
            for pdf in pdf_list:
                if pdf.ClassName() != 'RooProdPdf':
                    #print('Pdf {} is no RooProdPdf. Adding it.')
                    components.add(pdf)
                    continue
                find_unique_prod_components(pdf, components, recursion_count+1)
    
    def get_all_constraints(self):
        all_constraints = ROOT.RooArgSet()
        cache_name = "CACHE_CONSTR_OF_PDF_{}_FOR_OBS_{}".format(self.pdf.GetName(), 
                     ROOT.RooNameSet(self.data.get()).content())                 
        constr = self.workspace.set(cache_name)
        if constr:
            # retrieve constrains from cache     
            all_constraints.add(constr)
        else:
            # load information needed to determine attributes from ModelConfig 
            obs = deepcopy(self.observables)
            nuis = deepcopy(self.nuisance_parameters)
            all_constraints = self.pdf.getAllConstraints(obs, nuis, ROOT.kFALSE)
            
        # take care of the case where we have a product of constraint terms
        temp_all_constraints = ROOT.RooArgSet(all_constraints.GetName())
        for constraint in all_constraints:
            if constraint.IsA() == ROOT.RooProdPdf.Class():
                buffer = ROOT.RooArgSet()
                ExtendedModel.find_unique_prod_components(constraint, buffer)
                temp_all_constraints.add(buffer)
            else:
                temp_all_constraints.add(constraint)
        return temp_all_constraints
    
    def inspect_constrained_nuisance_parameter(self, nuis, constraints):
        nuis_name = nuis.GetName()
        print('INFO: On nuisance parameter {}'.format(nuis_name))
        nuip_nom = 0.0
        prefit_variation = 1.0
        found_constraint = ROOT.kFALSE
        found_gaussian_constraint = ROOT.kFALSE
        constraint_type = None
        for constraint in constraints:
            constr_name = constraint.GetName()
            if constraint.dependsOn(nuis):
                found_constraint = ROOT.kTRUE
                constraint_type = 'unknown'
                # Loop over global observables to match nuisance parameter and
                # global observable in case of a constrained nuisance parameter
                found_global_observable = ROOT.kFALSE
                for glob_obs in self.global_observables:
                    if constraint.dependsOn(glob_obs):
                        found_global_observable = ROOT.kTRUE
                        # find constraint width in case of a Gaussian
                        if constraint.IsA() == ROOT.RooGaussian.Class():
                            found_gaussian_constraint = ROOT.kTRUE
                            constraint_type = 'gaus'
                            old_sigma_value = 1.0
                            found_sigma = ROOT.kFALSE
                            for server in constraint.servers():
                                if (server != glob_obs) and (server != nuis):
                                    old_sigma_value = server.getVal()
                                    found_sigma = ROOT.kTRUE
                            if math.isclose(old_sigma_value, 1.0, abs_tol=0.001):
                                old_sigma_value = 1.0
                            if not found_sigma:
                                print('INFO: Sigma for pdf {} not found. Uisng 1.0.'.format(constr_name))
                            else:
                                print('INFO: Uisng {} for sigma of pdf {}'.format(old_sigma_value, constr_name))

                            prefit_variation = old_sigma_value
                        elif constraint.IsA() == ROOT.RooPoisson.Class():
                            constraint_type = 'pois'
                            tau = glob_obs.getVal()
                            print('INFO: Found tau {} of pdf'.format(constr_name))
                            prefit_variation = 1. / math.sqrt(tau)
                            print('INFO: Prefit variation is {}'.format(prefit_variation))
                            nuip_nom = 1.0
                            print("INFO: Assume that {} is nominal value of the nuisance parameter".format(nuip_nom))
        return prefit_variation, constraint_type, nuip_nom
        
    def set_initial_errors(self, source:Optional["ROOT.RooArgSet"]=None):
        if not source:
            source = self.nuisance_parameters
    
        all_constraints = self.get_all_constraints()
        for nuis in source:
            nuis_name = nuis.GetName()
            prefit_variation, constraint_type, _ = self.inspect_constrained_nuisance_parameter(nuis, all_constraints)
            if constraint_type=='gaus':
                print('INFO: Changing error of {} from {} to {}'.format(nuis_name, nuis.getError(), prefit_variation))
                nuis.setError(prefit_variation)
                nuis.removeRange()    
        return None
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                