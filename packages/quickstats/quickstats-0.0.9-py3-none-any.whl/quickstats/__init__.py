from quickstats._version import __version__

import os
import sys
import pathlib

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
macro_path = pathlib.Path(__file__).parent.absolute()
ROOT.gSystem.Load(os.path.join(macro_path, 'macros', 'RooTwoSidedCBShape_cc'))
from ROOT import RooTwoSidedCBShape