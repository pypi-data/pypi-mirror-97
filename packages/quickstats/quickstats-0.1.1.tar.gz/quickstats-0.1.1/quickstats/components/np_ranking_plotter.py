import os
import time
import glob
import json
import math
from copy import deepcopy
from typing import List, Dict, Optional

import uproot
import numpy as np

from quickstats.components import CLIParser, NuisanceParameterPull
from quickstats.components.root_plots import StandardGraphMaker, set_attrib
from quickstats.components.numerics import array_swap, reorder_arrays, reverse_arrays
from quickstats.utils import root_utils

import ROOT

class NPRankingPlotter(object):
    _BEAM_ENERGY_       = 13
    _LUMINOSITY_        = 36.5
    _BOX_HEIGHT_        = 0.25
    _BOX_HEIGHT_OL_     = 0.125
    _SIGMA_TOT_LO_      = 1.0
    _SIGMA_TOT_HI_      = 1.0
    _CHANNEL_POS_X_     = 0.36
    _CHANNEL_POS_Y_     = 0.19
    _POSITION_LABEL_X_  = 0.36 
    _POSITION_LABEL_DX_ = 0.1225
    _POSITION_LABEL_Y_  = 0.185
    _POSITION_LABEL_DY_ = 0.0275
    _DEFAULT_PLOT_CONFIG_ = {
        'num_param'    : -1,
        'threshold'    : 0.0,
        'scale_poi'    : 1.0,
        'scale_theta'  : 1.0,
        'show_names'   : True,
        'show_prefit'  : True,
        'show_postfit' : True,
        'relative'     : False,
        'correlation'  : True,
        'onesided'     : True,
        'rank'         : True,
        'log_level'    : 'INFO',
        'map_param'    : '',
        'label'        : '',
        'poi'          : 'mu'
    }
    
    _DEFAULT_IMPACT_ = {
        'nuis_val'    : -999,
        'nuis_up'     : 0,
        'nuis_down'   : 0,
        'nuis_prefit' : 1.,
        'poi_hat'     : 0,
        'poi_up'      : 0,
        'poi_down'    : 0,
        'poi_nom_up'  : 0,
        'poi_nom_down': 0
    }
    
    _CLI_USAGE_       = 'quickstats plot_ranking [-h|--help] [<args>]'
    _CLI_DESCRIPTION_ = 'Tool for making NP ranking plots'   
    _CLI_ARG_OPTIONS_ = \
        {
            'input_dir': {
                'abbr'        : 'i',
                'description' : 'Directory containing the NP pulls root files',
                'required'    : True,
                'type'        : str
            },
            'poi': {
                'abbr'        : 'p',
                'description' : 'POI in the ranking',
                'required'    : False,
                'type'        : str,
                'default'     : 'mu'
            },           
            'overlay_dir': {
                'abbr'        : 'v',
                'description' : 'Directory containing the root files for overlay',
                'required'    : False,
                'type'        : str,
                'default'     : ''
            },   
            'num_param': {
                'abbr'        : 'n',
                'description' : 'Top n parameters to show',
                'required'    : False,
                'type'        : int,
                'default'     : -1
            },      
            'threshold': {
                'abbr'        : 't',
                'description' : 'Threshold on impact',
                'required'    : False,
                'type'        : float,
                'default'     : 0.0
            },      
            'scale_poi': {
                'abbr'        : None,
                'description' : 'Scaling of impact axis',
                'required'    : False,
                'type'        : float,
                'default'     : 1.0
            },          
            'scale_theta': {
                'abbr'        : None,
                'description' : 'Scaling of pull axis',
                'required'    : False,
                'type'        : float,
                'default'     : 1.0
            },   
            'show_names': {
                'abbr'        : None,
                'description' : 'Draw nuisance parameter names',
                'required'    : False,
                'type'        : int,
                'default'     : 1
            }, 
            'show_prefit': {
                'abbr'        : None,
                'description' : 'Draw prefit impact',
                'required'    : False,
                'type'        : int,
                'default'     : 1
            },  
            'show_postfit': {
                'abbr'        : None,
                'description' : 'Draw postfit impact',
                'required'    : False,
                'type'        : int,
                'default'     : 1
            },   
            'relative': {
                'abbr'        : None,
                'description' : 'Show relative variation',
                'required'    : False,
                'type'        : int,
                'default'     : 0
            },    
            'correlation': {
                'abbr'        : None,
                'description' : 'Visualize sign of correlation',
                'required'    : False,
                'type'        : int,
                'default'     : 1
            },          
            'onesided': {
                'abbr'        : None,
                'description' : 'Show one sided variations',
                'required'    : False,
                'type'        : int,
                'default'     : 1
            },        
            'rank': {
                'abbr'        : None,
                'description' : 'Order nuisances by impact',
                'required'    : False,
                'type'        : int,
                'default'     : 1
            },  
            'log_level': {
                'abbr'        : None,
                'description' : 'Log level',
                'required'    : False,
                'type'        : str,
                'default'     : "INFO"
            },  
            'map_param': {
                'abbr'        : 'm',
                'description' : 'Map to nicer parameter names',
                'required'    : False,
                'type'        : str,
                'default'     : ""
            },  
            'label': {
                'abbr'        : 'l',
                'description' : 'Label on plot',
                'required'    : False,
                'type'        : str,
                'default'     : ""
            },
            'out_dir': {
                'abbr'        : 'o',
                'description' : 'Directory where the output files are created',
                'required'    : False,
                'type'        : str,
                'default'     : "./"
            },        
        }
    
    @property
    def config(self):
        return self._config
    
    @property
    def color_scheme(self):
        return self._color_scheme

    def __init__(self):   
        self.configure()

    def get_parser(self, **kwargs):
        parser = CLIParser(description=self._CLI_DESCRIPTION_,
                           usage=self._CLI_USAGE_)
        parser.load_argument_options(self._CLI_ARG_OPTIONS_)
        return parser
    
    def run_parser(self, args=None):
        parser = self.get_parser()
        kwargs = vars(parser.parse_args(args))
        self.run_plot(**kwargs)   
        
    def configure(self, **kwargs):
        self._config = self._DEFAULT_PLOT_CONFIG_
        for k,v in kwargs.items():
            if k in self.config:
                self._config[k] = v
            else:
                raise ValueError('unrecognized plot setting: {}'.format(k))                

    def get_plot_options(self):
        anticorr = self.config['correlation']
        kColorStandardBand   = "#ff0000"
        kColorStandardBandOL = "#950098"
        kColorPulls          = "#9d9d9d"
        kColorPrefit         = "#000155"
        kColorPrefitOL       = "#027734"
        kColorPostfit        = "#0094ff"
        kColorPostfitOL      = "#44ff94"
        kColorAntiCorr       = kColorPostfitOL if anticorr else kColorPostfit
        kColorAntiCorrOL     = kColorPostfit if anticorr else kColorPostfitOL
        kColorAntiCorrNom    = kColorPrefitOL if anticorr else kColorPrefit
        kColorAntiCorrNomOL  = kColorPrefit if anticorr else kColorPrefitOL
        plot_options = {
            'nuis_pulls':{
                'LineColor'        : ROOT.kBlack,
                'MarkerColor'      : ROOT.kBlack,
                'MarkerStyle'      : 20,
                'LineStyle'        : 1,
                'LineWidth'        : 1,
                'MarkerSize'       : 1,
                'Xaxis.TitleOffset': 1.2
            },
            'nuis_pulls_ol':{
                'LineColor'        : ROOT.kBlack,
                'MarkerColor'      : ROOT.kBlack,
                'MarkerStyle'      : 24,
                'LineStyle'        : 1,
                'LineWidth'        : 2,
                'MarkerSize'       : 1,
                'Xaxis.TitleOffset': 1.2
            },
            'one_sigma_box':{
                'LineColor'        : ROOT.TColor.GetColor(kColorStandardBand),
                'MarkerColor'      : ROOT.TColor.GetColor(kColorStandardBand),
                'LineStyle'        : 1,
                'LineWidth'        : 1,
                'MarkerSize'       : 1.25,
                'Xaxis.TitleOffset': 1.2
            },  
            'one_sigma_box_ol':{
                'LineColor'        : ROOT.TColor.GetColor(kColorStandardBandOL),
                'MarkerColor'      : ROOT.TColor.GetColor(kColorStandardBandOL),
                'LineStyle'        : 1,
                'LineWidth'        : 3,
                'MarkerSize'       : 1.25,
                'Xaxis.TitleOffset': 1.2
            },
            'line':{
                'LineColor'        : ROOT.TColor.GetColor(kColorPulls),  
                'LineStyle'        : 2,
                'LineWidth'        : 2
            },
            'poi_postfit_corr':{
                'LineColor'        : ROOT.TColor.GetColor(kColorPostfit),
                'FillColor'        : ROOT.TColor.GetColor(kColorPostfit),
                'LineWidth'        : 0,
                'MarkerSize'       : 0,
            },
            'poi_postfit_ol_corr':{
                'LineColor'        : ROOT.TColor.GetColor(kColorPostfitOL),
                'FillColor'        : ROOT.TColor.GetColor(kColorPostfitOL),
                'LineWidth'        : 0,
                'MarkerSize'       : 0,
            },
            'poi_postfit_anticorr':{
                'LineColor'        : ROOT.TColor.GetColor(kColorAntiCorr),
                'FillColor'        : ROOT.TColor.GetColor(kColorAntiCorr),
                'LineWidth'        : 0,
                'MarkerSize'       : 0,
            },
            'poi_postfit_anticorr_ol':{
                'LineColor'        : ROOT.TColor.GetColor(kColorAntiCorrOL),
                'FillColor'        : ROOT.TColor.GetColor(kColorAntiCorrOL),
                'LineWidth'        : 0,
                'MarkerSize'       : 0,
            },            
            'poi_prefit_corr':{
                'LineColor'        : ROOT.TColor.GetColor(kColorPrefit),
                'FillColor'        : ROOT.TColor.GetColor(kColorPrefit),
                'FillStyle'        : 0,
                'LineWidth'        : 1,
                'MarkerSize'       : 0,
            },
            'poi_prefit_ol_corr':{
                'LineColor'        : ROOT.TColor.GetColor(kColorPrefitOL),
                'FillColor'        : ROOT.TColor.GetColor(kColorPrefitOL),
                'FillStyle'        : 0,
                'LineWidth'        : 1,
                'MarkerSize'       : 0,
            },
            'poi_prefit_anticorr':{
                'LineColor'        : ROOT.TColor.GetColor(kColorAntiCorrNom),
                'FillColor'        : ROOT.TColor.GetColor(kColorAntiCorrNom),
                'FillStyle'        : 0,
                'LineWidth'        : 1,
                'MarkerSize'       : 0,
            },
            'poi_prefit_ol_anticorr':{
                'LineColor'        : ROOT.TColor.GetColor(kColorAntiCorrNomOL),
                'FillColor'        : ROOT.TColor.GetColor(kColorAntiCorrNomOL),
                'FillStyle'        : 0,
                'LineWidth'        : 1,
                'MarkerSize'       : 0,
            },
            'shade':{
                'LineColor'        : 18,
                'FillColor'        : 18,
                'FillStyle'        : 3001,
                'LineWidth'        : 1,
                'MarkerSize'       : 0
            },
            'label':{
                'Xaxis.LabelColor' : ROOT.kWhite,
                'Xaxis.AxisColor'  : ROOT.kWhite,
                'Yaxis.LabelColor' : ROOT.kBlack,
                'Yaxis.AxisColor'  : ROOT.kBlack,
                'Yaxis.TickLength' : 0.,
                'Stats'            : 0
            },
            'axis_poi':{
                'Name'             : 'axis_poi',
                'Title'            : "#Delta#hat{#mu}/#Delta#hat{#mu}_{tot}" if self.config['relative'] else \
                                     "#Delta#hat{" + self.config['poi'] + "}",
                'TitleOffset'      : 1.1,
                'LineColor'        : ROOT.kBlack,
                'LabelColor'       : ROOT.kBlack,
                'TitleColor'       : ROOT.kBlack,
                'LabelSize'        : 0.034,
                'TitleSize'        : 0.034
            },
            'axis_theta':{
                'Name'             : 'axis_theta',
                'Title'            : "(#hat{#theta} - #theta_{0})/#Delta#theta",
                'TitleOffset'      : 1.1,
                'LineColor'        : ROOT.kBlack,
                'LabelColor'       : ROOT.kBlack,
                'TitleColor'       : ROOT.kBlack,
                'LabelSize'        : 0.034,
                'TitleSize'        : 0.034
            },        
            'axis_label':{
                'LineColor'        : ROOT.kBlack,
                'TitleColor'       : ROOT.kWhite,
                'LabelSize'        : 0,
                'Ndivisions'       : 0
            },
            'legend':{
                'FillStyle'        : 0,
                'TextSize'         : 0.0225,
                'BorderSize'       : 0,
                'FillColor'        : 0
            },
            'ATLAS_label':{
                'NDC'              : None,
                'TextFont'         : 72,
                'TextColor'        : ROOT.kBlack,
                'TextSize'         : 0.035
            },
            'internal_label':{
                'NDC'              : None,
                'TextFont'         : 42,
                'TextColor'        : 1,
                'TextSize'         : 0.035
            }            
        }
        return plot_options                
        
    def setup_canvas(self):
        
        if not ROOT.gROOT.FindObject("c1"):
            canvas = ROOT.TCanvas("c1", "c1", 1500, 2000)
        else:
            canvas = ROOT.gROOT.FindObject("c1")
        if not ROOT.gROOT.FindObject("pad1"): 
            pad    = ROOT.TPad("pad1", "pad1", 0.0, 0.0, 1.0, 1.0, 0)
        else:
            pad    = ROOT.gROOT.FindObject("pad1")
            
        if self.config['show_names']:
            pad.SetLeftMargin(0.35)
        else:
            pad.SetLeftMargin(0.05)
        pad.SetRightMargin(0.05)
        pad.SetBottomMargin(0.09)
        pad.SetTopMargin(0.09)
        
        pad.Draw()
        pad.cd()
        return canvas, pad
        
    @staticmethod
    def extract_pull_results(input_dir:str, poi:str):
        if not os.path.exists(input_dir):
            raise FileNotFoundError('input directory {} does not exist'.format(input_dir))
        if not os.path.isdir(input_dir):
            raise ValueError('{} is not a directory'.format(input_dir))
        root_files = glob.glob(os.path.join(input_dir, "*.root"))
        pull_results = {
            'nuis_label'  : [],
            'nuis_val'    : [],
            'nuis_up'     : [],
            'nuis_down'   : [],
            'nuis_prefit' : [],
            'poi_hat'     : [],
            'poi_up'      : [],
            'poi_down'    : [],
            'poi_nom_up'  : [],
            'poi_nom_down': []
        }
        for file in root_files:
            raw_result = NuisanceParameterPull.parse_root_result(file)
            content = raw_result.get('result', None)
            if not content:
                raise ValueError('{} is not a valid root file containing NP pulls result'.format(file))
            pull_results['nuis_label'].append(content['nuisance'])
            pull_results['nuis_val'].append(content['nuis_hat'] - content['nuis_nom'])
            pull_results['nuis_up'].append(content['nuis_hi'])
            pull_results['nuis_down'].append(content['nuis_lo'])
            pull_results['nuis_prefit'].append(content['nuis_prefit'])
            pull_results['poi_hat'].append(content['{}_hat'.format(poi)])
            pull_results['poi_up'].append(content['{}_up'.format(poi)])
            pull_results['poi_down'].append(content['{}_down'.format(poi)])
            pull_results['poi_nom_up'].append(content['{}_up_nom'.format(poi)])
            pull_results['poi_nom_down'].append(content['{}_down_nom'.format(poi)])
        # convert to numpy arrays for easier post-processing
        for key in pull_results:
            pull_results[key] = np.array(pull_results[key])
        return pull_results
            
    def run_plot(self, input_dir:str, poi:str, overlay_dir:str='', num_param:int=-1, threshold:float=0.0,
                 scale_poi:float=1.0, scale_theta:float=1.0, show_names:bool=True, show_prefit:bool=True,
                 show_postfit:bool=True, relative:bool=False, correlation:bool=True, onesided:bool=True,
                 rank:bool=True, log_level:str="INFO", map_param:str="", label:str="", out_dir:str="./"):
        
        data = self.extract_pull_results(input_dir, poi)
        data_overlay = None
        if overlay_dir:
            data_overlay = self.extract_pull_results(overlay_dir, poi)
        
        param_dict = None
        if map_param:
            if os.path.exists(map_param):
                with open(map_param) as f:
                    param_dict = json.load(f)
            else:
                raise FileNotFoundError("map file {} does not exist".format(map_param))
        
        self.configure(num_param=num_param, threshold=threshold, scale_poi=scale_poi, rank=rank,
                       scale_theta=scale_theta, show_names=show_names, relative=relative,
                       correlation=correlation, onesided=onesided, label=label,
                       show_prefit=show_prefit, show_postfit=show_postfit, 
                       log_level=log_level, map_param=map_param, poi=poi)
        
        if data_overlay:
            all_nuis_labels = set(data['nuis_label']).union(set(data_overlay['nuis_label']))
        else:
            all_nuis_labels = None
        
        data = self.process_data(data, **self.config, pad_labels=all_nuis_labels)
        labels_to_keep = data['nuis_label']
        
        if data_overlay:
            overlay_config = deepcopy(self.config)
            overlay_config['threshold'] = 0.0
            overlay_config['num_param'] = -1
            data_overlay = self.process_data(data_overlay, **overlay_config,
                                             pad_labels=all_nuis_labels)
            # remove extra labels not present in data
            keep_indices = np.in1d(data_overlay['nuis_label'], labels_to_keep)
            for key in data_overlay:
                data_overlay[key] = data_overlay[key][keep_indices]
        #return data, data_overlay
        self.create_ranking_plot(data, data_overlay, param_dict, out_dir=out_dir)
    
    @staticmethod
    def pad_default_impact(source, pad_labels:Optional[List]=None, 
                           default_impact:Optional[Dict]=None):
        # no extra impacts for padding, just exit
        if not pad_labels:
            return None
        if default_impact is None:
            default_impact = NPRankingPlotter._DEFAULT_IMPACT_        
        extra_labels = np.array(list(set(pad_labels) - set(source['nuis_label'])))
        n_extra = len(extra_labels)
        if n_extra == 0:
            return None
        new_impact = {'nuis_label': extra_labels}
        new_impact.update({key: np.array([default_impact[key]]*n_extra) for key in default_impact})
        for key in source:
            if key not in new_impact:
                raise ValueError('missing default value for the attribute {}'.format(key))
            source[key] = np.concatenate((source[key], new_impact[key]))
            
    @staticmethod
    def remove_impact_data(data, threshold:float=0.0, num_param:int=-1):
        # remove impacts below threshold
        sigma_tol = NPRankingPlotter._SIGMA_TOT_LO_ + NPRankingPlotter._SIGMA_TOT_HI_
        below_threshold = np.where(((data['poi_up'] + data['poi_down']) / sigma_tol) < threshold)
        for i in below_threshold[0]:
            print('WARNING: Removing "{}" (impact up:{}, impact down:{}) below threshold {}.'.format(
                  data['nuis_label'][i], data['poi_up'][i], data['poi_down'][i], threshold))
        for key in data:
            data[key] = np.delete(data[key], below_threshold)
        # retain only top num_param impacts
        if num_param > 0:
            for key in data:
                data[key] = data[key][:num_param]
    
    @staticmethod
    def process_impact(impact_up:np.ndarray, impact_down:np.ndarray, 
                       correlation:bool=True, onesided:bool=True):
        if correlation:
            array_swap(impact_up, impact_down, (impact_up < 0) & (impact_down > 0))

        if (not correlation) or (not onesided):
            array_swap(impact_up, impact_down, impact_up < 0)
        # secondary rows for one-sided impacts
        impact_up_sec = deepcopy(impact_up)
        impact_down_sec = deepcopy(impact_down)
        if onesided:
            indices = (impact_up > 0) & (impact_down > 0)
            impact_up[indices] = impact_down_sec[indices]
            impact_down[indices] = 0
            impact_down_sec[indices] = 0
            indices = (impact_up < 0) & (impact_down < 0)
            impact_down_sec[indices] = impact_up[indices]
            impact_up[indices] = 0
            impact_up_sec[indices] = 0
        impact_up[:], impact_down[:] = abs(impact_up), abs(impact_down)
        impact_up_sec[:], impact_down_sec[:] = abs(impact_up_sec), abs(impact_down_sec)
        return impact_up_sec, impact_down_sec
    
    @staticmethod
    def process_data(data, scale_theta:float=1.0, scale_poi:float=1.0, correlation:bool=True,
                     onesided:bool=True, ranking:bool=True, relative:bool=False, threshold:float=0.0,
                     num_param:int=-1, pad_labels:Optional[List]=None, **kwargs):
        source = deepcopy(data)
        # subtract poi_hat offset from impacts
        for key in ['poi_up', 'poi_down', 'poi_nom_up', 'poi_nom_down']:
            source[key] -= source['poi_hat']   
        anticorrelated     = source['nuis_label'][(source['poi_up'] < 0) & (source['poi_down'] > 0)]
        anticorrelated_nom = source['nuis_label'][(source['poi_nom_up'] < 0) & (source['poi_nom_down'] > 0)]
        poi_up_sec, poi_down_sec = NPRankingPlotter.process_impact(
            source['poi_up'], source['poi_down'], correlation, onesided)
        source['poi_up_sec'] = poi_up_sec
        source['poi_down_sec'] = poi_down_sec
        poi_nom_up_sec, poi_nom_down_sec = NPRankingPlotter.process_impact(
            source['poi_nom_up'], source['poi_nom_down'], correlation, onesided)
        source['poi_nom_up_sec'] = poi_nom_up_sec
        source['poi_nom_down_sec'] = poi_nom_down_sec        
        max_poi = max(max(source['poi_up']), max(source['poi_down']),
                      max(source['poi_up_sec']), max(source['poi_down_sec']))
        NPRankingPlotter.pad_default_impact(source, pad_labels)
        if ranking:
            impact = (source['poi_up'] + source['poi_down'] +
                     source['poi_up_sec'] + source['poi_down_sec'])
            impact /= (1*(source['poi_up'] != 0) + 1*(source['poi_down'] != 0) +
                       1*(source['poi_up_sec'] != 0) + 1*(source['poi_down_sec'] != 0))
            # order by impact, from largest to smallest
            reorder_arrays(impact, *source.values())
        else:
            # order by NP names
            reorder_arrays(source['nuis_label'], *source.values(), descending=False)

        NPRankingPlotter.remove_impact_data(source, threshold, num_param)
        
        # rescaling impacts and pulls
        for key in ['poi_up', 'poi_down', 'poi_nom_up', 'poi_nom_down',
                    'poi_up_sec', 'poi_down_sec', 'poi_nom_up_sec', 'poi_nom_down_sec']:
            source[key] *= (scale_poi / max_poi)
            if relative:
                source[key] /= source['poi_hat']
        source['nuis_val'] *= scale_theta
        for key in ['nuis_up', 'nuis_down']:
            source[key] /= source['nuis_prefit']   
            source[key] = abs(source[key])*scale_theta
    
        source['poi_corr']     = ~np.in1d(source['nuis_label'], anticorrelated)
        source['poi_nom_corr'] = ~np.in1d(source['nuis_label'], anticorrelated_nom)
        # dirty fix for carrying max_poi inside source
        source['max_poi'] = np.array([max_poi]*len(source['nuis_label']))
        if ranking:
            # order by impact, from smallest to largest
            reverse_arrays(*source.values())
        return source
    
    @staticmethod
    def split_impact_by_correlation(impact_up, impact_down, correlated_indices):
        impacts = {
            'up_corr'       : impact_up.copy(),
            'up_anticorr'   : impact_up.copy(),
            'down_corr'     : impact_down.copy(),
            'down_anticorr' : impact_down.copy(),
        }
        impacts['up_corr'][~correlated_indices]      = 0.0
        impacts['up_anticorr'][correlated_indices]   = 0.0
        impacts['down_corr'][~correlated_indices]    = 0.0
        impacts['down_anticorr'][correlated_indices] = 0.0
        #for key in impacts:
        #    impacts[key] = np.vstack((impacts[key], impacts[key])).ravel('F')
        return impacts
    
    @staticmethod
    def _combine_impacts(primary, secondary):
        impacts = {}
        for key in ['up_corr', 'up_anticorr', 'down_corr', 'down_anticorr']:
            impacts[key] = np.vstack((primary[key], secondary[key])).ravel('F')
        return impacts
    
    def get_plot_data(self, data, data_overlay=None):
        
        n_nuis = len(data['nuis_label'])
        if data_overlay:
            n_nuis_ol = len(data['data_overlay'])
            assert n_nuis == n_nuis_ol
            
        box_up      = np.array([self.config['scale_theta']]*n_nuis)
        box_down    = np.array([self.config['scale_theta']]*n_nuis)
        box_up_ol   = data['nuis_prefit']*self.config['scale_theta']
        box_down_ol = data['nuis_prefit']*self.config['scale_theta']
        cen_up      = np.array([self._BOX_HEIGHT_]*2*n_nuis)
        cen_down    = np.array([self._BOX_HEIGHT_]*2*n_nuis)
        cen_up_ol   = np.array([self._BOX_HEIGHT_OL_]*2*n_nuis)
        cen_down_ol = np.array([self._BOX_HEIGHT_OL_]*2*n_nuis)        
             
        primary     = self.split_impact_by_correlation(data['poi_up'], 
                                                       data['poi_down'],
                                                       data['poi_corr'])
        
        secondary   = self.split_impact_by_correlation(data['poi_up_sec'], 
                                                       data['poi_down_sec'],
                                                       data['poi_corr'])        
        poi_impacts = self._combine_impacts(primary, secondary)
        
        nom_primary = self.split_impact_by_correlation(data['poi_nom_up'],
                                                       data['poi_nom_down'],
                                                       data['poi_nom_corr'])
        
        nom_secondary = self.split_impact_by_correlation(data['poi_nom_up_sec'], 
                                                         data['poi_nom_down_sec'],
                                                         data['poi_nom_corr'])   
        poi_nom_impacts = self._combine_impacts(nom_primary, nom_secondary)
        #from pdb import set_trace
        #set_trace()
        if data_overlay:
            nuis_y = np.array(range(n_nuis)) + 0.75
            poi_y  = np.array([0.625, 0.875] * n_nuis) + np.vstack((range(n_nuis), range(n_nuis))).ravel('F')
        else:
            nuis_y = np.array(range(n_nuis)) + 0.5
            poi_y  = np.array([0.25, 0.75] * n_nuis) + np.vstack((range(n_nuis), range(n_nuis))).ravel('F')

        #  make plot of pulls for nuisance parameters
        plot_data = {}
        plot_data['nuis_pulls'] = {
            'n'      : n_nuis,
            'x'      : data['nuis_val'],
            'y'      : nuis_y,
            'xerr_lo': data['nuis_down'],
            'xerr_hi': data['nuis_up']
        }
        plot_data['one_sigma_box'] = {
            'n'      : n_nuis,
            'x'      : data['nuis_val'],
            'y'      : nuis_y,
            'xerr_lo': box_down,
            'xerr_hi': box_up
        }
        plot_data['poi_prefit_corr'] = {
            'n'      : 2*n_nuis,
            'x'      : np.zeros(2*n_nuis),
            'y'      : poi_y,
            'xerr_lo': poi_nom_impacts['down_corr'],
            'xerr_hi': poi_nom_impacts['up_corr'],
            'yerr_lo': cen_down,
            'yerr_hi': cen_up,
        }
        plot_data['poi_prefit_anticorr'] = {
            'n'      : 2*n_nuis,
            'x'      : np.zeros(2*n_nuis),
            'y'      : poi_y,
            'xerr_lo': poi_nom_impacts['down_anticorr'],
            'xerr_hi': poi_nom_impacts['up_anticorr'],
            'yerr_lo': cen_down,
            'yerr_hi': cen_up,        
        }    
        plot_data['poi_postfit_corr'] = {
            'n'      : 2*n_nuis,
            'x'      : np.zeros(2*n_nuis),
            'y'      : poi_y,
            'xerr_lo': poi_impacts['down_corr'],
            'xerr_hi': poi_impacts['up_corr'],
            'yerr_lo': cen_down,
            'yerr_hi': cen_up,             
        }
        plot_data['poi_postfit_anticorr'] = {
            'n'      : 2*n_nuis,
            'x'      : np.zeros(2*n_nuis),
            'y'      : poi_y,
            'xerr_lo': poi_impacts['down_anticorr'],
            'xerr_hi': poi_impacts['up_anticorr'],
            'yerr_lo': cen_down,
            'yerr_hi': cen_up,          
        }

        if data_overlay:
            poi_overlay_impacts     = self.split_impact_by_correlation(data_overlay['poi_up'], 
                                                                       data_overlay['poi_down'], 
                                                                       data_overlay['poi_corr'])
            poi_overlay_nom_impacts = self.split_impact_by_correlation(data_overlay['poi_nom_up'],
                                                                       data_overlay['poi_nom_down'],
                                                                       data_overlay['poi_nomcorr']) 
            nuis_y        = np.array(range(n_nuis)) + 0.25
            poi_y_overlay = np.array([0.125, 0.375]*n_nuis) + np.vstack((range(n_nuis), range(n_nuis))).ravel('F')
            plot_data['nuis_pulls_ol'] = {
                'n'      : n_nuis,
                'x'      : data_overlay['nuis_val'],
                'y'      : nuis_y,
                'xerr_lo': data_overlay['nuis_down'],
                'xerr_hi': data_overlay['nuis_up']
            }
            plot_data['one_sigma_box_ol'] = {
                'n'      : n_nuis,
                'x'      : source['nuis_val'],
                'y'      : nuis_y,
                'xerr_lo': box_down_ol,
                'xerr_hi': box_up_ol
            }
            plot_data['poi_prefit_ol_corr'] = {
                'n'      : 2*n_nuis,
                'x'      : np.zeros(2*n_nuis),
                'y'      : poi_y_overlay,
                'xerr_lo': poi_overlay_nom_impacts['down_corr'],
                'xerr_hi': poi_overlay_nom_impacts['up_corr'],
                'yerr_lo': cen_down_ol,
                'yerr_hi': cen_up_ol,
            }
            plot_data['poi_prefit_ol_anticorr'] = {
                'n'      : 2*n_nuis,
                'x'      : np.zeros(2*n_nuis),
                'y'      : poi_y_overlay,
                'xerr_lo': poi_overlay_nom_impacts['down_anticorr'],
                'xerr_hi': poi_overlay_nom_impacts['up_anticorr'],
                'yerr_lo': cen_down_ol,
                'yerr_hi': cen_up_ol,        
            }    
            plot_data['poi_postfit_ol_corr'] = {
                'n'      : 2*n_nuis,
                'x'      : np.zeros(2*n_nuis),
                'y'      : poi_y_overlay,
                'xerr_lo': poi_overlay_impacts['down_corr'],
                'xerr_hi': poi_overlay_impacts['up_corr'],
                'yerr_lo': cen_down_ol,
                'yerr_hi': cen_up_ol,             
            }
            plot_data['poi_postfit_ol_anticorr'] = {
                'n'      : 2*n_nuis,
                'x'      : np.zeros(2*n_nuis),
                'y'      : poi_y_overlay,
                'xerr_lo': poi_overlay_impacts['down_anticorr'],
                'xerr_hi': poi_overlay_impacts['up_anticorr'],
                'yerr_lo': cen_down_ol,
                'yerr_hi': cen_up_ol,          
            }           
        else:
            plot_data['nuis_pulls_ol']           = None
            plot_data['one_sigma_box_ol']        = None
            plot_data['poi_prefit_ol_corr']      = None
            plot_data['poi_prefit_ol_anticorr']  = None
            plot_data['poi_postfit_ol_corr']     = None
            plot_data['poi_postfit_ol_anticorr'] = None
        n_shade = (n_nuis + 1)//2
        plot_data['shade'] = {
            'n'      : n_shade,
            'x'      : np.zeros(n_shade),
            'y'      : np.array(range(n_shade))*2 + 0.5,
            'xerr_lo': np.array([100.]*n_shade),
            'xerr_hi': np.array([100.]*n_shade),
            'yerr_lo': np.array([0.5]*n_shade),
            'yerr_hi': np.array([0.5]*n_shade)
        }
        max_poi   = data['max_poi'][0]
        offset    = math.ceil(2 * n_nuis / 10)
        border_lo = -self._SIGMA_TOT_LO_ / max_poi
        border_hi = self._SIGMA_TOT_HI_ / max_poi
        plot_data['label'] = {
            "n_x"  : 1,
            "x_lo" : border_lo,
            "x_hi" : border_hi,
            "n_y"  : n_nuis + offset + 1,
            "y_lo" : -offset,
            "y_hi" : n_nuis + 1
        }      
        plot_data['axis_poi'] = {
            "x_min" : border_lo,
            "y_min" : n_nuis + 1,
            "x_max" : border_hi,
            "y_max" : n_nuis + 1,
            "w_min" : -self._SIGMA_TOT_LO_ / self.config['scale_poi'],
            "w_max" : self._SIGMA_TOT_HI_ / self.config['scale_poi'],
            "n_div" : 510,
            "chopt" : "-L"
        }    
        plot_data['axis_theta'] = {
            "x_min" : border_lo,
            "y_min" : -offset,
            "x_max" : border_hi,
            "y_max" : -offset,
            "w_min" : (-self._SIGMA_TOT_LO_ / max_poi) / self.config['scale_theta'],
            "w_max" : (self._SIGMA_TOT_HI_ / max_poi) / self.config['scale_theta'],
            "n_div" : 510,
            "chopt" : "+R"
        }  
        plot_data['axis_label'] = {
            "x_min" : border_lo,
            "y_min" : 0,
            "x_max" : border_lo,
            "y_max" : n_nuis + 1,
            "w_min" : 0,
            "w_max" : n_nuis + 1,
            "n_div" : 0,
            "chopt" : "-R"
        }     
        plot_data['legend'] = {
            'x1'     : self._CHANNEL_POS_X_ + 0.28,
            'y1'     : self._CHANNEL_POS_Y_ - 0.0775,
            'x2'     : self._CHANNEL_POS_X_ + 0.68,
            'y2'     : self._CHANNEL_POS_Y_ + 0.02,
            "header" : "",
            "option" : "NDC"
        }
        return plot_data

    def create_ranking_plot(self, data, data_overlay=None, param_dict=None, out_dir="./"):
        
        canvas, pad = self.setup_canvas()
        n_nuis = len(data['nuis_label'])
        plot_data = self.get_plot_data(data, data_overlay)  
        plot_options = self.get_plot_options()
        
        # format histogram for labels
        hist = StandardGraphMaker.TH2F("h_ranking", "", **plot_data['label'])
        labels = data['nuis_label'] if self.config['show_names'] else np.array([""]*n_nuis)
        if param_dict is not None:
            labels = np.array([param_dict[label] for label in labels])
        offset = math.ceil(2 * n_nuis / 10)
        for i, label in enumerate(labels):
            hist.GetYaxis().SetBinLabel(i + offset + 1, label)
        label_size = (1.0 / n_nuis) if (1.0 / n_nuis) < 0.02 else 0.02
        hist.SetLabelSize(label_size, "Y")
        set_attrib(hist, **plot_options['label'])
        hist.Draw("h")
        
        # format axis for poi
        axis_poi = StandardGraphMaker.TGaxis(**plot_data['axis_poi'])
        axis_poi.ImportAxisAttributes(hist.GetXaxis())
        set_attrib(axis_poi, **plot_options['axis_poi'])
        
        # format axis for theta
        axis_theta = StandardGraphMaker.TGaxis(**plot_data['axis_theta'])
        axis_theta.ImportAxisAttributes(hist.GetXaxis())
        set_attrib(axis_theta, **plot_options['axis_theta'])
        
        # format axis for labels
        axis_label = StandardGraphMaker.TGaxis(**plot_data['axis_label'], options=plot_options['axis_label'])
        
        # format line
        line = StandardGraphMaker.TLine(options=plot_options['line'])  
        
        graphs_to_draw = ['shade']
        if self.config['show_postfit']:
            graphs_to_draw.append('poi_postfit_corr')
            graphs_to_draw.append('poi_postfit_anticorr')
            if data_overlay:
                graphs_to_draw.append('poi_postfit_ol_corr')
                graphs_to_draw.append('poi_postfit_ol_anticorr')
        if self.config['show_prefit']:
            graphs_to_draw.append('poi_prefit_corr')
            graphs_to_draw.append('poi_prefit_anticorr')
            if data_overlay:
                graphs_to_draw.append('poi_prefit_ol_corr')
                graphs_to_draw.append('poi_prefit_ol_anticorr')
        # draw graphs
        graphs = {}
        for name in graphs_to_draw:
            graphs[name] = StandardGraphMaker.GraphAsymErrors(**plot_data[name], options=plot_options[name])
            graphs[name].Draw("p2")
            
        # draw axis
        if self.config['show_postfit'] or self.config['show_prefit']:
            axis_poi.Draw()
        axis_theta.Draw()
        axis_label.Draw()
        
        # draw +-1 and 0 sigma lines for pulls
        line.DrawLine(0., 0., 0., n_nuis);
        line.DrawLine(1. * self.config['scale_theta'], 0., 1. * self.config['scale_theta'], n_nuis);
        line.DrawLine(-1. * self.config['scale_theta'], 0., -1. * self.config['scale_theta'], n_nuis);

        ROOT.gStyle.SetEndErrorSize(5.0)
        if data_overlay:
            graphs_to_draw = ['one_sigma_box', 'one_sigma_box_ol', 'nuis_pulls', 'nuis_pulls_ol']
        else:
            graphs_to_draw = ['one_sigma_box', 'nuis_pulls']
            
        for name in graphs_to_draw:
            graphs[name] = StandardGraphMaker.GraphAsymErrors(**plot_data[name], options=plot_options[name])
            graphs[name].Draw("p")
        
        canvas.SetLogy(0)
        
        # draw legends
        legend = StandardGraphMaker.TLegend(**plot_data['legend'], options=plot_options['legend'])
        legend.AddEntry(graphs['nuis_pulls'], "Pull", "lp")
        if data_overlay:
            legend.AddEntry(graphs['nuis_pulls_ol'], "Alt pull", "lp")
        legend.AddEntry(graphs['one_sigma_box'], "1 standard deviation", "l")
        if data_overlay:
            legend.AddEntry(graphs['one_sigma_box_ol'], "Alt 1 standard deviation", "l")    
        if self.config['show_prefit']:
            legend.AddEntry(graphs['poi_prefit_corr'], 
                            "Prefit Impact on #hat{" + self.config['poi'] + "}", "f")
            if data_overlay:
                legend.AddEntry(graphs['poi_prefit_corr_ol'], 
                                "Alt Prefit Impact on #hat{" + self.config['poi'] + "}", "f")
        if self.config['show_postfit']:
            legend.AddEntry(graphs['poi_postfit_corr'], 
                            "Postfit Impact on #hat{" + self.config['poi'] + "}", "f")
            if data_overlay:
                legend.AddEntry(graphs['poi_postfit_corr_ol'], 
                                "Alt Postfit Impact on #hat{" + self.config['poi'] + "}", "f")
        legend.Draw()
        
        label_1 = StandardGraphMaker.TLatex(options=plot_options['ATLAS_label'])
        label_2 = StandardGraphMaker.TLatex(options=plot_options['internal_label'])
        
        label_1.DrawLatex(self._POSITION_LABEL_X_, self._POSITION_LABEL_Y_, "ATLAS")
        label_2.DrawLatex(self._POSITION_LABEL_X_ + self._POSITION_LABEL_DX_,
                              self._POSITION_LABEL_Y_, "Internal")
        label_2.DrawLatex(self._POSITION_LABEL_X_,
                              self._POSITION_LABEL_Y_ - 1 * self._POSITION_LABEL_DY_,
                              self.config['label'])  
        label_2.DrawLatex(self._POSITION_LABEL_X_,
                              self._POSITION_LABEL_Y_ - 2 * self._POSITION_LABEL_DY_,
                              "Rank 1 to {}".format(n_nuis))         
        
        save_name = "ranking_{}_rank_{:04d}_to_{:04d}".format(self.config['poi'], 1, n_nuis)
        save_path = os.path.join(out_dir, save_name)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        for extension in ['eps', 'pdf', 'png', 'C']:
            canvas.SaveAs("{}.{}".format(save_path, extension))