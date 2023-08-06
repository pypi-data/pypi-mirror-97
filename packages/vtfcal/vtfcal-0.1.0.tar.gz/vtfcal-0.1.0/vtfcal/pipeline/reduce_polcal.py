"""
Polarisation calibration reduction

...

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

import asdf

from vtfcal.reduction.polcal import fit_parameters, gen_demod_matrix, gen_mueller_matrix
from vtfcal.utils import correct_darks


def reduce_polcal(data_tree):
    """
    Function to reduce VTF polarisation calibration frames

    Loads polcal frames from the input directory specified by `data_tree` and reduces them by
    applying the following steps:

    - Correct for darks
    - Average accumulations
    - Run reduced polcal frames through DKIST's PA&C pipeline to produce demodulation and telescope
    matrices

    Reduced frames and matrices are saved to the output directory specified by `data_tree` and
    references to the files are added to the tree for use later in the calibration process.

    Parameters
    ----------
    data_tree : string or :class:`pathlib.Path`
        Path to an :class:`~asdf.AsdfFile` defining the calibration data structure, including input
        and output data directories, and file references to polcal frames. See
        :meth:`commands.init_data_tree` for generating an appropriate file.

    Examples
    --------

    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    asdf_file = asdf.open(data_tree)
    outdir = asdf_file["support"]["data_dir"]

    # Reduce darks
    # Depends on dark averaging
    # asdf_file = correct_darks(asdf_file, "raw", "polcal")

    # Average accumulations

    # Run through PA&C pipeline
    ## wrapper func around fitcuparams.main()
    fit_parameters(asdf_file)
    ## wrapper func around generatedmodmatrices.main()
    gen_demod_matrix(asdf_file)
    ## wrapper func around telescopemodel.telescopemodel.generate_inverse.telescope_model
    gen_mueller_matrix(asdf_file)
