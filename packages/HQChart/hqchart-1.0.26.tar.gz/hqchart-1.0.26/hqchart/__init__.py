import sys
import os
import json
from os.path import dirname

with open(dirname(__file__) + '/pkg_info.json') as fp:
    _info = json.load(fp)

__version__ = _info['version']

from hqchart.HQChartPy2 import LoadAuthorizeInfo, Run, GetAuthorizeInfo, GetVersion

from hqchart.hqchartpy2_fast import PERIOD_ID, IHQData, FastHQChart

from hqchart.hqchartpy2_pandas import HQChartPy2Helper

from hqchart.tushare.hqchartpy2_tushare import TushareHQChartData, TushareKLocalHQChartData, HQResultTest
from hqchart.tushare.hqchartpy2_tushare_config import TushareConfig


