"""
Polarisation calibration preprocessing

Tools to prepare the polarisation calibration data for processing by DKIST.

"""

import click


@click.command()
def preprocess_polcal(polcal_frames):
    """
    Function to preprocess polarisation calibration data.

    Loads specified polarisation calibration frames, corrects them for darks, and averages over
    accumulations.

    \b
    Parameters
    ----------
    polcal_frames : list
        List of `pathlib.Path<https://docs.python.org/3/library/pathlib.html#pathlib.Path>`_ objects
        which each point to a FITS file containing a raw VTF polarisation calibration frame.

    \b
    Returns
    -------
    reduced_polcal_frames : list
        List of `pathlib.Path<https://docs.python.org/3/library/pathlib.html#pathlib.Path>`_ objects
        which each point to a FITS file containing a preprocessed VTF polarisation calibration frame
        corrected for darks and averaged over accumulations.

    """


# If this script is invoked from the command line, run reduced_prefilter()
# Command line arguments are passed automatically by click
if __name__ == "__main__":
    preprocess_polcal()
