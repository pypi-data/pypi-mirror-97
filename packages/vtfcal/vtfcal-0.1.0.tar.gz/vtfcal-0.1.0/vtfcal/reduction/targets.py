"""
Target frame reduction

Average target frames, correct them for darks and flats, and use them to determine alignment
parameters.

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
from os.path import join

import numpy as np
import skimage.feature as skf
import skimage.transform as skt
from skimage.feature import corner_peaks, corner_subpix
from skimage.measure import ransac

import ccdproc

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def average_targets(targetfiles, output_dir):
    """
    Function to reduce VTF target frames

    Loads specified target frames, calculates an average frame per camera channel, corrects these
    for dark and flat effects, then aligns them. Input files should all be for the same line scan.
    Reduced, corrected frames are saved to disk and the corresponding filenames are returned.
    Alignment information is also returned in the form of a rotation matrix.

    \b
    Parameters
    ----------
    targetfiles : list
        List of `pathlib.Path<https://docs.python.org/3/library/pathlib.html#pathlib.Path>`_ objects
        which each point to a FITS file containing a raw VTF flat frame.

    \b
    Returns
    -------
    reduced_flats : list
        List of `pathlib.Path<https://docs.python.org/3/library/pathlib.html#pathlib.Path>`_ objects
        which each point to a FITS file containing a reduced VTF target frame corrected for darks
        and flats.

    rot_matrix : array of floats
        Rotation matrix describing the transformation which aligns each of the narrowband images
        with the broadband channel.

    """

    frames = [ccdproc.CCDData.read(f, format="fits", unit="adu") for f in targetfiles]
    target_fname = join(output_dir, "average_target.FITS")
    target = ccdproc.combine(frames, output_file=target_fname)

    return (target, target_fname)  # latter may not be necessary, can probably get it from metadata


def detect_corners(img):
    return corner_subpix(
        img, corner_peaks(skf.corner_harris(img, 0.2), min_distance=10), window_size=10
    )


def define_alignment_refs(target, extractor):
    points = detect_corners(target)
    extractor.extract(target, points)
    refs = {}
    refs["image"] = target
    refs["points"] = points[extractor.mask]
    refs["descriptors"] = extractor.descriptors

    return points, refs


def align_to_reference(img, extractor, refs):
    # Calculate alignment parameters
    points = detect_corners(img)
    extractor.extract(img, points)
    points = points[extractor.mask]
    descriptors = extractor.descriptors
    matches = skf.match_descriptors(refs["descriptors"], descriptors, cross_check=True)
    transform, inliers = ransac(
        (refs["points"][matches[:, 0]], points[matches[:, 1]]),
        skt.ProjectiveTransform,
        min_samples=5,
        residual_threshold=1,
        max_trials=10000,
    )
    newim = skt.warp(img, transform.inverse, cval=np.nan)
    logger.debug(f"Estimated transform: {transform}")
    logger.debug(f"Estimated transform parameters: {transform.params}")
    logger.debug(f"# inliers: {len(inliers)}")

    return newim, points, matches, transform.params
