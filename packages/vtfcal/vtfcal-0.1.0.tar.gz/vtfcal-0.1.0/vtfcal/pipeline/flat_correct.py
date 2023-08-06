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

import logging

import numpy as np

import asdf
import ccdproc

from dkist.asdf_maker import headers_from_filenames as heads
from dkist.asdf_maker import references_from_filenames as refs
from dkist.io import DaskFITSArrayContainer as DFAC
from dkist.io.fits import AstropyFITSLoader as Loader
from vtfcal.correction.flat_correction import flat_correct
from vtfcal.test_constants import TEST_PIXEL, TEST_WL_IDX
from vtfcal.utils import plotframes


def correct_flats(data_tree):
    """
    Apply flat correction to data frames.

    Loads dark-corrected data frames specified by `data_tree` and corrects them for flat-field
    effects using the reduced flats calculated using :meth:`commands.reduce_flats`. Corrected frames
    are saved to the output directory specified by `data_tree` and references to the files are added
    to the tree for use later in the calibration process.

    \b
    Parameters
    ----------
    data_tree : string or :class:`pathlib.Path`
        Path to an :class:`~asdf.AsdfFile` defining the calibration data structure, including input
        and output data directories, and file references to reduced flats. See
        :meth:`commands.init_data_tree` for generating an appropriate file.

    Examples
    --------

    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    asdf_file = asdf.open(data_tree, mode="rw")
    for modstate in ["modstate0", "modstate1", "modstate2", "modstate3"]:
        datafiles = asdf_file["support"]["corrected dark-corrected data " + modstate]
        outdir = asdf_file["support"]["data_dir"]

        if asdf_file["mode"] == "broadband":
            allflats = asdf_file["support"][
                "corrected dark-corrected flats " + modstate
            ]
            flats = [
                ccdproc.CCDData.read(f.fileuri, format="fits", unit="adu")
                for f in allflats
            ]
        else:
            ## REFACTOR: rewrite whatever saves the stack to do it as fits files and as part of the asdf
            flat_data = DFAC(asdf_file["support"][f"corrected normalised flats {modstate}"], loader=Loader).array
            flats = [
                ccdproc.CCDData(frame.compute(), unit="adu") for frame in flat_data
            ]
        corrected_frames = flat_correct(datafiles, flats)
        headers = np.array(heads(corrected_frames))
        asdf_file["support"]["corrected flat-corrected data " + modstate] = refs(
            corrected_frames, headers, len(corrected_frames)
        )

        plotframes(
            asdf_file,
            [
                (
                    f"corrected flat-corrected data {modstate}",
                    "Flat-corrected data frame",
                )
            ],
            "02b-flat-corrected-data",
        )

    asdf_file.update()
