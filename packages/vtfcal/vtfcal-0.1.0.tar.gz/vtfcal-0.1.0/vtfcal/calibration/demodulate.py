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
from pathlib import Path

import dask.array as da
import numpy as np

from astropy.io import fits

from dkist.asdf_maker import headers_from_filenames as heads
from dkist.asdf_maker import references_from_filenames as refs
from dkist.io import DaskFITSArrayContainer as DFAC
from dkist.io.fits import AstropyFITSLoader as Loader


def demod(asdf_file):
    """
    Apply demodulation matrix to reconstructed data frames.
    """

    logger = logging.getLogger(__name__)
    logger.setLevel("INFO")

    outdir = asdf_file["support"]["data_dir"]

    modstates = ["modstate0", "modstate1", "modstate2", "modstate3"]
    data_by_modstate = {
        m: asdf_file["support"]["calibrated aligned data " + m] for m in modstates
    }
    demod_by_modstate = {m: [] for m in modstates}

    # for each wavelength
    for l in range(18):
        # load frame for each mod state (x, y, 4)
        allstates = DFAC(
            [data_by_modstate[m][l] for m in modstates], loader=Loader
        ).array
        ## Moving the axis in this way _shouldn't_ make anything wrong, but make sure of that at some point
        allstates = da.moveaxis(allstates, 0, -1)
        logger.debug(
            f"{allstates.shape}, {type(allstates)}, {allstates.mean().compute()}"
        )
        logger.debug(asdf_file["polcal-demod-matrices"])
        # This isn't right at the moment because Athur's code makes a 4x8 matrix
        # demod_mat = fits.open(asdf_file["polcal-demod-matrices"])[1]
        # TODO Double check that this array is a) the right way round and b) in the right order
        rt34 = np.sqrt(3) / 4
        demod_mat = np.array(
            [
                [1 / 4, 1 / 4, 1 / 4, 1 / 4],
                [rt34, rt34, -rt34, -rt34],
                [rt34, -rt34, -rt34, rt34],
                [rt34, -rt34, rt34, -rt34],
            ]
        )
        logger.debug(f"{demod_mat.shape}")
        newdata = np.matmul(allstates, demod_mat)  # .data)
        logger.debug(f"{newdata.shape}, {type(newdata)}")

        for m, mod in enumerate(modstates):
            # get/define output name
            outfile = data_by_modstate[mod][l].fileuri.replace("aligned", "demodulated")
            logger.debug(f"{outfile}")
            # save file
            # This will want a defined header
            fits.writeto(outfile, np.array(newdata[..., m]), overwrite=True)
            # put filname in list
            demod_by_modstate[mod].append(outfile)

    for mod, files in demod_by_modstate.items():
        asdf_file["support"]["calibrated demodulated data " + mod] = refs(
            files, np.array(heads(files)), len(files)
        )

    asdf_file.update()

    return asdf_file
