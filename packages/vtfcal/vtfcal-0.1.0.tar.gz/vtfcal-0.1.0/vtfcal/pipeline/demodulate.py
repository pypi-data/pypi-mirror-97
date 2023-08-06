import re
import logging
from os.path import join

import matplotlib.pyplot as plt

import asdf
from astropy.io import fits

from vtfcal.calibration.demodulate import demod
from vtfcal.test_constants import TEST_WL_IDX
from vtfcal.utils import plotframes


def demodulate(data_tree):
    """
    """

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    asdf_file = asdf.open(data_tree, mode="rw")
    outdir = asdf_file["support"]["data_dir"]

    asdf_file = demod(asdf_file)
    asdf_file.update()

    titles = [r"$I_0$", r"$I_1$", r"$I_2$", r"$I_3$", r"$I$", r"$Q$", r"$U$", r"$V$"]
    keys = [f"calibrated aligned data modstate{m}" for m in range(4)] + [f"calibrated demodulated data modstate{m}" for m in range(4)]
    plotframes(asdf_file, list(zip(keys, titles)), "05-demodulated-data")
