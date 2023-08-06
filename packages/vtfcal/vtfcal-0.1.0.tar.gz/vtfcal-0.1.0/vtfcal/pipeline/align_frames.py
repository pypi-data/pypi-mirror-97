"""
Frame alignment

Functions to align frames based on coalignment parameters calculated by target reduction

See Also
--------

Notes
-----

References
----------

Examples
--------

"""

import re
import logging
from os.path import join

import matplotlib.pyplot as plt
import numpy as np
from skimage.transform import AffineTransform, warp

import asdf
from astropy.io import fits

from dkist.asdf_maker import headers_from_filenames as heads
from dkist.asdf_maker import references_from_filenames as refs
from vtfcal.test_constants import TEST_PIXEL, TEST_WL_IDX
from vtfcal.utils import plotframes


def align_frames(data_tree):
    """
    """
    logger = logging.getLogger(__name__)

    asdf_file = asdf.open(data_tree, mode="rw")

    tform = AffineTransform(matrix=asdf_file["coalignment-matrix"])

    for modstate in ["modstate0", "modstate1", "modstate2", "modstate3"]:
        aligned_frames = []
        datafiles = asdf_file["support"]["corrected flat-corrected data " + modstate]
        for f in datafiles:
            logger.debug(f.fileuri)
            hdu = fits.open(f.fileuri)[0]
            img = hdu.data
            new_img = warp(img, tform.inverse, output_shape=img.shape, cval=img.mean())
            hdu.data = new_img
            # TODO also update the rotation in the header because that will obviously be important
            new_fname = f.fileuri.replace("flat_corrected", "aligned")
            fits.writeto(new_fname, hdu.data, header=hdu.header)
            aligned_frames.append(new_fname)

        headers = np.array(heads(aligned_frames))
        asdf_file["support"]["calibrated aligned data " + modstate] = refs(
            aligned_frames, headers, len(aligned_frames)
        )

        plotframes(
            asdf_file,
            [
                (f"corrected flat-corrected data {modstate}", "Flat-corrected frame"),
                (
                    f"calibrated aligned data {modstate}",
                    "Derotated flat-corrected frame",
                ),
            ],
            f"04a-aligned-data-{modstate}",
        )

    asdf_file.update()
