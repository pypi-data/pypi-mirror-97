"""
Science data preparation

Functions to perform dark corrections on raw science data as part of the preparation for more
rigourous image reconstruction using those data.

See Also
--------
Optional

Notes
-----
Optional

References
----------
Optional, use if references are cited in Notes

Examples
--------
Optional
"""

import glob
import logging
from os.path import join
from pathlib import Path
from itertools import groupby

import matplotlib.pyplot as plt
import numpy as np

import asdf
from astropy.io import fits

from dkist.asdf_maker import headers_from_filenames as heads
from dkist.asdf_maker import references_from_filenames as refs
from vtfcal import utils
from vtfcal.test_constants import TEST_PIXEL, TEST_WL_IDX


def correct_darks(data_tree):
    """
    Apply dark correction to raw data frames.

    Loads data frames from the input directory specified by `data_tree` and corrects them for dark
    effects using the average dark calculated using :meth:`commands.reduce_darks`. Corrected frames
    are saved to the output directory specified by `data_tree` and references to the files are added
    to the tree for use later in the calibration process.

    \b
    Parameters
    ----------
    data_tree : string or :class:`pathlib.Path`
        Path to an :class:`~asdf.AsdfFile` defining the calibration data structure, including input
        and output data directories, and file references to averaged darks. See
        :meth:`commands.init_data_tree` for generating an appropriate file.

    Examples
    --------

    """
    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.DEBUG)

    asdf_file = asdf.open(data_tree, mode="rw")
    # datafiles = sorted(
    #     glob.glob(join(asdf_file["raw"]["data_dir"], "data*.FITS"), recursive=True)
    # )
    datafiles = sorted(
        list(Path(asdf_file["raw"]["data_dir"]).rglob("data*.FITS")),
        key=utils.get_modstate,
    )
    filegroups = groupby(datafiles, key=utils.get_modstate)
    files_by_modstate = {}
    for modstate, files in filegroups:
        filelist = list(files)
        files_by_modstate[modstate] = refs(
            filelist, np.array(heads(filelist)), len(filelist)
        )
    # iterate over groups
    for modstate in ["modstate0", "modstate1", "modstate2", "modstate3"]:
        datafiles = files_by_modstate[modstate]
        asdf_file["raw"]["data " + modstate] = datafiles
        logger.debug(datafiles)

        asdf_file = utils.correct_darks(asdf_file, "raw", "data " + modstate)
        corrected_frames = asdf_file["support"][
            "corrected dark-corrected data " + modstate
        ]
        logger.info(f"Demo plots created with wavelength index {TEST_WL_IDX}")
        logger.debug(corrected_frames)
        # This surely isn't necessary with ExternalArrayReferences ?
        testframe = fits.open(
            [f.fileuri for f in corrected_frames if f"_l{TEST_WL_IDX:02}" in f.fileuri][
                0
            ]
        )[0]

        utils.plotframes(
            asdf_file,
            [
                (
                    f"corrected dark-corrected data {modstate}",
                    "Dark-corrected data frame",
                )
            ],
            "02a-dark-corrected-data",
        )
