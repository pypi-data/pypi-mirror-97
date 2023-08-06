import logging
import logging.config
from os.path import join, split

import numpy as np

import asdf
import astropy.units as u
import ccdproc

from dkist.asdf_maker import headers_from_filenames as heads
from dkist.asdf_maker import references_from_filenames as refs


def correct_darks(asdf_file, category, data_key):
    """
    Corrects averaged flat frames for telescope dark effects.

    Loads specified dark frames and subtracts those data from the corresponding input flat frames.
    Corrected flats are saved to disk and the files and filenames are returned in a dictionary.

    Parameters
    ----------
    asdf_file : string or `Path<https://docs.python.org/3/library/pathlib.html#pathlib.Path>`_
        Path to an `AsdfFile` defining the calibration data structure, including input and output
        data directories and file references to averaged, dark-corrected flat frames. See
        :meth:`vtf-pipeline.commands.init_data_tree` for generating an appropriate file.

    TODO update this docstring
    tree_keys : list of strings
        Keys specifying what frames are to be corrected. `asdf_file` is accessed with each of the
        keys in turn in a nested way. (see examples).

    Returns
    -------
    new_asdf : :class:`asdf.AsdfFile`
        Updated :class:`asdf.AsdfFile` containing the same information as `data_tree` plus a file
        reference to a map of the wavelength shift value calculated for each pixel.

    Examples
    --------

    """
    logger = logging.getLogger(__name__)
    logger.setLevel("INFO")

    # Load dark files
    ## REFACTOR: file loading
    # this is not robust, it'll break silently as soon as there's >1 dark per channel
    darkfiles = asdf_file.tree["support"]["reduced averaged darks"][0].fileuri
    darkframe = ccdproc.CCDData.read(darkfiles, format="fits", unit="adu")

    files = asdf_file[category][data_key]
    logger.debug(f"{data_key}, {files}")

    # Establish dark <--> flat correspondence # no need, 1 flat/channel until I work in exp. t's
    # Subtract darks
    corrected_frames = []
    ## OPTIMISE: remove loop
    for f in files:
        path, fname = split(f.fileuri)
        path = path.replace(asdf_file["raw"]["data_dir"], asdf_file["support"]["data_dir"])
        newpath = join(path, f"dark_corrected_{fname}")
        logger.debug(f"{f.fileuri} ==> {newpath}")
        data = ccdproc.CCDData.read(f.fileuri, format="fits", unit="adu")
        logger.debug(
            "++++ averaged: "
            f"{np.nanmin(data.data)} {np.nanmean(data.data)} {np.nanmax(data.data)}"
        )
        # Exposure times here are clearly placeholders and I need to sort it out
        data = ccdproc.subtract_dark(data, darkframe, dark_exposure=1 * u.s, data_exposure=1 * u.s)
        logger.debug(
            "---- corrected: "
            f"{np.nanmin(data.data)} {np.nanmean(data.data)} {np.nanmax(data.data)}"
        )
        data.write(newpath, overwrite=True)
        corrected_frames.append(newpath)

    headers = np.array(heads(corrected_frames))
    old_keys = data_key.replace("reduced ", "").replace("averaged ", "")
    new_key = "corrected dark-corrected " + old_keys
    logger.debug(f"==== {data_key} ==> {new_key}")

    asdf_file["support"][new_key] = refs(corrected_frames, headers, len(corrected_frames))
    asdf_file.update()

    return asdf_file
