"""
Target frame reduction

Functions to average, dark-correct, flat-correct and align target frames.

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

import matplotlib.pyplot as plt
import numpy as np
import skimage.feature as skf
from skimage.feature import BRIEF

import asdf

from dkist.asdf_maker import headers_from_filenames as heads
from dkist.asdf_maker import references_from_filenames as refs
from vtfcal.reduction import targets
from vtfcal.utils import correct_darks


def reduce_targets(data_trees):
    """
    Reduce and correct target frames

    Loads target frames from the input directory specified by `data_tree`, then averages them,
    corrects for dark and flat frames, and determines the parameters required to coalign the images.

    Parameters
    ----------
    data_trees : list of strings or :class:`pathlib.Path`s
        Paths to :class:`~asdf.AsdfFile`s defining the calibration data structure, including input
        and output data directories, for each telescope channel. See :meth:`commands.init_data_tree`
        for generating appropriate files.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    extractor = BRIEF()
    ## Plotting helpers
    fig, ax = plt.subplots(2, 3, figsize=(16, 10))
    ax = ax.flatten()
    for i, fname in enumerate(data_trees):
        for m in range(4):
            modstate = f"modstate{m}"
            channel_tree = asdf.open(fname, mode="rw")
            data_dir = Path(channel_tree["raw"]["data_dir"]) / modstate
            targetfiles = list(data_dir.rglob("target.FITS"))
            headers = np.array(heads(targetfiles))
            channel_tree["raw"]["target {modstate}"] = refs(targetfiles, headers, len(targetfiles))
            channel_tree.update()
            target, target_fname = targets.average_targets(
                targetfiles, Path(channel_tree["support"]["data_dir"]) / modstate
            )

            # existing_reduced = channel_tree.tree.get("reduced", {}).get("averaged", {})
            header = np.array(heads([target_fname]))
            channel_tree["support"][f"reduced averaged target {modstate}"] = refs(target_fname, header, 1)
            channel_tree.update()
            channel_tree = correct_darks(channel_tree, "support", f"reduced averaged target {modstate}")

            # # This isn't plotting dark-corrected targets but that's probably fine for now I guess
            img = target.data
            plt.sca(ax[i])
            plt.imshow(img)
            if channel_tree["mode"] == "broadband":
                points, img_refs = targets.define_alignment_refs(img, extractor)
                ax[i].scatter(
                    points.T[1], points.T[0], marker="x", cmap="Reds", c=range(len(points.T[0]))
                )
            elif channel_tree["mode"] == "narrowband":
                newim, points, matches, matrix = targets.align_to_reference(img, extractor, img_refs)
                ax[i].scatter(
                    points.T[1], points.T[0], marker="x", cmap="Reds", c=range(len(points.T[0]))
                )
                skf.plot_matches(ax[3], img_refs["image"], img, img_refs["points"], points, matches)

                channel_tree["coalignment-matrix"] = matrix
                channel_tree.write_to(channel_tree.uri)
                resid = img_refs["image"] - newim
                logger.debug(f"{resid.max()}")
                ax[i + 3].imshow(resid)
            else:
                raise ValueError(
                    "Unrecognised data mode." "Should be either 'broadband' or 'narrowband'."
                )

    plt.savefig(Path(channel_tree["plots"]).parent / "target-alignment")
