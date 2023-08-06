# Licensed under a 3-clause BSD style license - see LICENSE.rst

# This sub-module is destined for common non-package specific utility
# functions.

import configparser as cfp
from pathlib import Path
from .dark_correction_utils import *  # noqa: F401,F403
from .general import *
from .plotting import *

cfg = cfp.ConfigParser()
cfg.read("vtf-calibration-config.cfg")

home = Path.home()
paths = cfg["paths"]
RAW_DATA = Path(paths["raw_data"]).expanduser() / paths["raw_data_dir_name"]
DKIST = Path(paths["dkist_dir_location"]).expanduser() / "DKIST"
DATA = DKIST / "VTF" / "data"
