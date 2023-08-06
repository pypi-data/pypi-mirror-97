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

import dask.array as da
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage.interpolation import shift

from astropy.io import fits
from astropy.io.fits.hdu.base import BITPIX2DTYPE
from astropy.modeling import fitting, models

from dkist.asdf_maker import headers_from_filenames as heads
from dkist.asdf_maker import references_from_filenames as refs
from dkist.io import DaskFITSArrayContainer as DFAC
from dkist.io.fits import AstropyFITSLoader as Loader
from vtfcal.test_constants import TEST_PIXEL, TEST_WL_IDX
from vtfcal.utils import average_by_wavelength

# from dask.distributed import get_client  # Client


def get_dtype_and_size(f):
    with f as fi:
        head = fits.getheader(fi, hdu=1)
    naxes = head["NAXIS"]
    dtype = BITPIX2DTYPE[head["BITPIX"]]
    shape = [head[f"NAXIS{n}"] for n in range(naxes, 0, -1)]
    return dtype, shape


class DelayedFits:
    def __init__(self, file, shape, dtype):
        self.shape = shape
        self.dtype = dtype
        self.file = file
        self.hdu = 0

    def __getitem__(self, item):
        with self.file as f:
            with self.file as f:
                with fits.open(f) as hdul:
                    hdul.verify("fix")
                    return hdul[self.hdu].data[item]


def average_flats(asdf_file):
    return average_by_wavelength(asdf_file, "flats")


def calculate_wl_shift(asdf_file, modstate, fourier=True):
    """
    Calculate the wavelength shift of each pixel from the image mean profile

    Extract a wavelength profile and determine its minimum, both for each individual pixel position
    and for the average across all pixels in each image. The wavelength shift for each pixel is
    calculated as the difference between these two values.

    Parameters
    ----------
    asdf_file : string or `Path<https://docs.python.org/3/library/pathlib.html#pathlib.Path>`_
        Path to an `AsdfFile` defining the calibration data structure, including input and output
        data directories and file references to averaged, dark-corrected flat frames. See
        :meth:`vtf-pipeline.commands.init_data_tree` for generating an appropriate file.

    Returns
    -------
    new_asdf : :class:`asdf.AsdfFile`
        Updated :class:`asdf.AsdfFile` containing the same information as `data_tree` plus a file
        reference to a map of the wavelength shift value calculated for each pixel.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel("INFO")

    # client = get_client()

    outdir = Path(asdf_file["support"]["data_dir"])

    ## REFACTOR: file loading
    flatfiles = asdf_file["support"]["corrected dark-corrected flats " + modstate]
    arr = DFAC(flatfiles, loader=Loader).array
    arr = arr.rechunk((-1, 8, 8))
    mean_profile = da.nanmean(arr, axis=(1, 2)).compute()
    profile = arr[:, TEST_PIXEL[0], TEST_PIXEL[1]].compute()

    if fourier:
        flats = np.array(arr)
        flats[np.isnan(flats)] = 0
        l = flats.shape[0]
        flats_fft = np.fft.fftn(flats, axes=[0])
        lp = -np.arctan(flats_fft[1].imag / flats_fft[1].real) / (2 * np.pi)
        wl_shift_map = -(lp * l)
    else:
        # cropped_profile = profile[profile.argmin()-5:profile.argmin()+6]
        model = models.Polynomial1D(degree=2)
        fitter = fitting.LinearLSQFitter()
        # xp = range(profile.argmin()-5, profile.argmin()+6)
        # fit_profile = fitter(model, xp, cropped_profile)
        fit_profile = fitter(model, range(len(profile)), profile)
        c, b, a = fit_profile.parameters
        minx = -b / (2 * a)
        miny = c - ((b ** 2) / (4 * a))
        logger.debug(f"\n{fit_profile}\n{c, b, a}\n{minx, miny}")

        minmap = da.from_array(np.zeros((arr.shape[1], arr.shape[2])), chunks=(8, 8))
        minmap = da.map_blocks(
            _calcshift, minmap, arr, dtype=minmap.dtype, chunks=(1, 8, 8)
        )
        minmap = minmap.reshape((arr.shape[1], arr.shape[2]))

        wl_shift_map = da.nanmean(minmap) - minmap

    if fourier:
        final_map = wl_shift_map
    else:
        final_map = wl_shift_map.compute()
    fname = outdir / "wl_shift_map.FITS"
    fits.writeto(fname, final_map, overwrite=True)
    asdf_file["support"]["calibration wl-shift-map " + modstate] = refs(
        [fname], np.array(heads([fname])), 1
    )
    asdf_file.update()

    return asdf_file, arr, mean_profile


# TODO Consider moving this function and _shift_pixels into .utils somewhere
def _calcshift(wl_shift_map, flatfiles):
    """
    Wavelength-shift calculation

    Fits a second-order polynomial to the wavelength profile of each pixel in `flatfiles`, and
    stores the minima of the polynomials in `wl_shift_map`. Only uses a small range around the
    minimum value of the wavelength profile, since including the wings can produce inaccurate fits.

    Parameters
    ----------
    wl_shift_map : :class:`dask.array.Array`
        Empty array with the same shape as flat frames.

    flatfiles : :class:`dask.array.Array`
        3D array containing flat frame values for each wavelength step

    Returns
    -------
    wl_shift_map : :class:`dask.array.Array`
        Array of calculated profile minima for each pixel
    """
    logger = logging.getLogger(__name__)

    l, xx, yy = flatfiles.shape

    ## OPTIMISE: remove loops if possible
    fitter = fitting.LinearLSQFitter()
    for x in range(xx):
        for y in range(yy):
            profile = flatfiles[:, x, y]
            xc = profile.argmin()
            model = models.Polynomial1D(degree=2)
            try:
                ## Hard-coded indices assume wl range of scan will be small
                ## Double check this and see if header info can be used instead
                fit_profile = fitter(
                    model, range(xc - 5, xc + 6), profile[xc - 5 : xc + 6]
                )
                c, b, a = fit_profile.parameters
                minx = -b / (2 * a)
            ## OPTIMISE: find a way to exclude these pixels without try/except
            except Exception as e:
                logger.debug(
                    (
                        x,
                        y,
                        xc,
                        len(range(xc - 5, xc + 6)),
                        len(profile[xc - 5 : xc + 6]),
                        len(range(xc - 5, xc + 6)) == len(profile[xc - 5 : xc + 6]),
                    )
                )
                logger.debug(f"Failed to fit pixel {x}, {y} of chunk with error: {e}")
                minx = np.nan
            wl_shift_map[x, y] = minx

    return wl_shift_map


def _shift_pixels(flatfiles, wl_shift_map):
    """
    Shift wavelength profiles

    Interpolates the wavelength profile of each pixel along the wavelength axis to align the minimum
    of the profile with the minimum of the average profile.

    Parameters
    ----------
    flatfiles : :class:`dask.array.Array`
        3D array containing flat frame values for each wavelength step

    wl_shift_map : :class:`dask.array.Array`
        Wavelength shifts calculated by :meth:`_calcshift`
    """
    logger = logging.getLogger(__name__)

    xx, yy = wl_shift_map.shape

    ## OPTIMISE: remove loop
    for x in range(xx):
        for y in range(yy):
            if np.isnan(wl_shift_map[x, y]):
                logger.debug(f"No valid shift value for pixel {x}, {y}, skipping.")
                flatfiles[:, x, y] = np.nan
            else:
                flatfiles[:, x, y] = shift(
                    flatfiles[:, x, y], wl_shift_map[x, y], mode="nearest"
                )
            ## This wants to be something more accurate than nearest once i've optimised a bit

    return flatfiles


def correct_wl_shift(flatfiles, wl_shift_map, mean_profile, outdir, modstate, fourier=True):
    """
    Correct flat-field images by adjusting for wavelength shift

    Interpolate the given flat-field images such that the value in each pixel position is adjusted
    by an amount specified by the wavelength shift map. This aligns the centre of the wavelength
    profile of each pixel.

    Parameters
    ----------
    flatfiles : array-like
        Dask array of per-wavelength-position
        dark-corrected flats. For the broadband channel this dictionary should contain a single
        frame.

    wl_shift_map : array of floats
        Array containing the wavelength shift value calculated for each pixel.

    mean_profile : array
        Wavelength profile averaged over all pixels. Used only for plotting.

    outdir : string
        Output directory in which to save plots

    Returns
    -------
    corrected_flats : array-like
        Dask array of per-wavelength-position flats corrected for wavelength shift.

    Raises
    ------

    See Also
    --------
    calculate_wl_shift

    Notes
    -----

    References
    ----------
    Optional, use if references are cited in Notes

    Examples
    --------

    """
    if fourier:
        wl_shift_map[np.isnan(wl_shift_map)] = 0
        flats = np.array(flatfiles)
        nanidx = np.isnan(flats)
        flats[nanidx] = 0
        flats_fft = np.fft.fftn(flats, axes=[0])
        l = flats_fft.shape[0]
        midpoint = l // 2
        k = np.roll(-(np.arange(l) - midpoint), midpoint)
        d = 2 * np.pi * (k / l) * wl_shift_map.reshape(*wl_shift_map.shape, 1)
        d = np.rollaxis(d, 2)
        d1 = np.cos(d) + (np.sin(d) * 1j)
        corrected_flats = np.fft.ifftn(flats_fft * d1, axes=[0]).real
        corrected_flats[nanidx] = np.nan
        corrected_flats = da.from_array(corrected_flats)
    else:
        wl_shift_map = da.from_array(wl_shift_map, chunks=(8, 8))
        corrected_flats = da.map_blocks(
            _shift_pixels, flatfiles, wl_shift_map, dtype=flatfiles.dtype
        )

    profile = flatfiles[:, TEST_PIXEL[0], TEST_PIXEL[1]]
    shifted_profile = corrected_flats[:, TEST_PIXEL[0], TEST_PIXEL[1]]

    ## REFACTOR: plotting helpers
    fig, ax = plt.subplots(figsize=(10, 7))
    plt.plot(profile, label=f"Unshifted profile for pixel {TEST_PIXEL}")
    plt.axhline(profile.min(), linestyle=":")
    if not fourier:
        plt.plot(mean_profile, linestyle="--", color="red", label="Mean profile")
        plt.plot(mean_profile.argmin(), mean_profile.min(), "x", color="red")
        target = mean_profile.argmin()
    else:
        target = midpoint
    plt.axvline(target, linestyle="--", color="red")
    plt.plot(
        shifted_profile,
        linestyle=":",
        color="green",
        label=f"Shifted profile for pixel {TEST_PIXEL}",
    )
    plt.axvline(shifted_profile.argmin(), linestyle=":", color="green")
    plt.xlabel(r"$\lambda$ index")
    plt.ylabel(r"$I$")
    plt.legend()
    testshift = wl_shift_map[TEST_PIXEL[0], TEST_PIXEL[1]]
    if not fourier:
        testshift = testshift.compute()
    plt.title(f"Profile minimum shifted from {profile.argmin().compute()} to {shifted_profile.argmin().compute()}\n(Target = {target}, calculated shift = {testshift})")
    plt.savefig(join(outdir, f"01e-wl-shifted-profile-{modstate}"), bbox_tight="tight")
    plt.close()

    return corrected_flats
