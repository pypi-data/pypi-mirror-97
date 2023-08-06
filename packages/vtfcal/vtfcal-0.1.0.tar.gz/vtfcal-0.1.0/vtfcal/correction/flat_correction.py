"""
Short summary

Extended summary

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

import ccdproc

from ..test_constants import TEST_WL_IDX


## This and other new functions in this repo should take and return an asdf tree for consistency
## with existing ones.
def flat_correct(data, flats):
    logger = logging.getLogger(__name__)
    logger.setLevel("INFO")

    corrected_frames = []
    ## OPTIMISE: remove loop
    for i, fileobj in enumerate(data):
        ## REFACTOR: file loading
        dataframe = ccdproc.CCDData.read(fileobj.fileuri, format="fits", unit="adu")
        newpath = fileobj.fileuri.replace("dark_corrected_", "flat_corrected_")
        if isinstance(flats, list):
            flat = flats[i]
        elif isinstance(flats, ccdproc.ccddata.CCDData):
            flat = flats
        logger.debug(f"{np.nanmin(flat.data)}")
        dataframe = ccdproc.flat_correct(dataframe, flat, norm_value=1)
        dataframe.write(newpath)
        corrected_frames.append(newpath)

    return corrected_frames
