"""
Flat frame reduction

Average collected flat frames as appropriate to reduce to the smallest number required to calibrate
the science data.

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
from pathlib import Path
from multiprocessing.pool import ThreadPool

import dask
import dask.array as da
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
from dask.distributed import Client

import asdf
from astropy.io import fits

from dkist.asdf_maker import headers_from_filenames as heads
from dkist.asdf_maker import references_from_filenames as refs
from dkist.io import DaskFITSArrayContainer as DFAC
from dkist.io.fits import AstropyFITSLoader as Loader
from vtfcal.reduction.flats import average_flats, calculate_wl_shift, correct_wl_shift
from vtfcal.test_constants import TEST_PIXEL, TEST_WL_IDX
from vtfcal.utils import correct_darks, plotframes

# Set up dask for threading of intensive tasks.
# Need this here because Client doesn't like being instantiated not in __main__.
if __name__ == "__main__":
    client = Client()
    dask.config.set(pool=ThreadPool())


def reduce_flats(data_tree, correction=True, fourier=True):
    """
    Function to reduce VTF flat frames

    Loads flat frames from the input directory specified by `data_tree` and reduces them by applying
    the following steps:

    \b
    - Group frames by wavelength position and average them
    - Correct for darks
    - Calculate and correct for wavelength shift
    - Normalise images by scaling each frame by its average value [still needs implementing]

    Reduced flats are saved to the output directory specified by `data_tree` and references to the
    files are added to the tree for use later in the calibration process.

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
    logger.setLevel("INFO")

    asdf_file = asdf.open(data_tree, mode="rw")
    outdir = asdf_file["support"]["data_dir"]

    asdf_file = average_flats(asdf_file)
    if asdf_file["mode"] not in ["broadband", "narrowband"]:
        raise ValueError(
            f'Unrecognised data mode in asdf tree: {asdf_file["mode"]} '
            '- "mode" keyword should be either "broadband" or "narrowband".'
        )
    for modstate in ["modstate0", "modstate1", "modstate2", "modstate3"]:
        averaged_frames = asdf_file["support"][
            "reduced averaged flats " + modstate
        ]  # list of reference
        logger.debug(f"{modstate}, {averaged_frames[0]}")
        averaged_profile = [
            fits.open(f.fileuri)[0].data[TEST_PIXEL[0], TEST_PIXEL[1]]
            for f in averaged_frames
        ]

        asdf_file = correct_darks(
            asdf_file, "support", f"reduced averaged flats {modstate}"
        )
        corrected_frames = asdf_file["support"][
            f"corrected dark-corrected flats {modstate}"
        ]
        corrected_profile = [
            fits.open(f.fileuri)[0].data[TEST_PIXEL[0], TEST_PIXEL[1]]
            for f in corrected_frames
        ]

        plotframes(
            asdf_file,
            [
                (f"reduced averaged flats {modstate}", "Averaged flat frames"),
                (f"reduced averaged darks", "Averaged dark frame"),
                (
                    f"corrected dark-corrected flats {modstate}",
                    "Dark-corrected flat frame",
                ),
            ],
            "01aii-flat-correction",
        )

        ## REFACTOR: plotting helpers
        fig = plt.figure(figsize=(10, 7))
        plt.plot(
            averaged_profile,
            color="red",
            linestyle=":",
            label=f"Averaged profile for pixel {TEST_PIXEL}",
        )
        plt.plot(
            corrected_profile,
            color="blue",
            linestyle="--",
            label=f"Dark-corrected profile for pixel {TEST_PIXEL}",
        )
        plt.xlabel(r"$\lambda$ index")
        plt.ylabel(r"$I$")
        plt.legend()
        plt.savefig(
            join(asdf_file["plots"], f"01bii-averaged-vs-corrected-profiles"),
            bbox_inches="tight",
        )

        plt.close()

        if asdf_file["mode"] == "broadband":
            continue

        if not correction:
            arr = DFAC(corrected_frames, loader=Loader).array
            norm_frames = arr / arr.mean(axis=0)
            norm_fnames = []
            for wl, frame in enumerate(norm_frames):
                fname = Path(outdir) / modstate / f"normalised_flat_l{wl:02}a0.FITS"
                fits.writeto(fname, frame.compute(), overwrite=True)
                norm_fnames.append(fname)
            asdf_file["support"]["corrected normalised flats " + modstate] = refs(
                norm_fnames, np.array(heads(norm_fnames)), len(norm_fnames)
            )
            asdf_file.update()
            continue

        asdf_file, daskarr, mean_profile = calculate_wl_shift(asdf_file, modstate, fourier=fourier)

        wl_shift_map = fits.open(
            asdf_file["support"]["calibration wl-shift-map " + modstate][0].fileuri
        )[0].data
        shifted_frames = correct_wl_shift(
            daskarr, wl_shift_map, mean_profile, asdf_file["plots"], modstate=modstate, fourier=fourier
        )

        shifted_fnames = []
        for wl, frame in enumerate(shifted_frames):
            fname = Path(outdir) / modstate / f"wl_shifted_flat_l{wl:02}a0.FITS"
            fits.writeto(fname, frame.compute(), overwrite=True)
            shifted_fnames.append(fname)
        asdf_file["support"]["corrected wl-shifted flats " + modstate] = refs(
            shifted_fnames, np.array(heads(shifted_fnames)), len(shifted_fnames)
        )

        plotframes(
            asdf_file,
            [
                (f"corrected dark-corrected flats {modstate}", "Dark-corrected flat frame"),
                (f"calibration wl-shift-map {modstate}", r"$\lambda$-shift map"),
                (
                    f"corrected wl-shifted flats {modstate}",
                    r"$\lambda$-shifted flat frame",
                ),
            ],
            f"01g-wl-shift-comparison",
        )

        logger.debug(shifted_frames.shape)

        norm_frames = shifted_frames / shifted_frames.mean(axis=0)
        norm_fnames = []
        for wl, frame in enumerate(norm_frames):
            fname = Path(outdir) / modstate / f"normalised_flat_l{wl:02}a0.FITS"
            fits.writeto(fname, frame.compute(), overwrite=True)
            norm_fnames.append(fname)
        asdf_file["support"]["corrected normalised flats " + modstate] = refs(
            norm_fnames, np.array(heads(norm_fnames)), len(norm_fnames)
        )
        asdf_file.update()

        plotframes(
            asdf_file,
            [
                (
                    f"corrected wl-shifted flats {modstate}",
                    r"$\lambda$-shifted flat frame",
                ),
                (
                    f"corrected normalised flats {modstate}",
                    "Normalised shifted flat frame",
                ),
            ],
            "01h-normalisation-comparison",
        )
