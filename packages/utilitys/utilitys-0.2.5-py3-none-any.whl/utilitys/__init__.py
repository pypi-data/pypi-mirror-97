import pyqtgraph as _pg
_pg.setConfigOption('imageAxisOrder', 'row-major')
# Be sure to register pgparams
from .params.prjparam import PrjParam
from .params import pgregistered as _
from .processing import *
from .params import *
from .misc import *
from . import fns, widgets