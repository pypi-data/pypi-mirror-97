"""
Prefilter frame reduction

Reduce prefilter frames to curve coefficients which approximate the instrumental effects of the
etalon.

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

import click


@click.command()
def reduce_prefilter(prefilterfiles):
    """
    Function to reduce, correct and process VTF prefilter frames

    Loads specified prefilter frames and determines the parameters of the prefilter curve. This is
    achieved by performing the following operations:

    - Apply dark-correction to frames
    - Average over accumulations
    - Correct for wavelength shifts using the wavelength-shift map calculated during flat-frame
      reduction
    - Average each frame to produce an average spectrum
    - Determine wavelength offset between VTF spectrum and FTS atlas spectrum and adjust for it
    - Determine ratio between VTF and FTS spectra
    - Fit a curve to the ratio of spectra using a double-Gaussian or Lorentzian profile

    \b
    Parameters
    ----------
        List of `pathlib.Path<https://docs.python.org/3/library/pathlib.html#pathlib.Path>`_ objects
        which each point to a FITS file containing a raw VTF prefilter frame.

    \b
    Returns
    -------
    prefilter_params : dict
        Dictionary of parameters describing the profile fitted to the prefilter spectrum.

    """


# If this script is invoked from the command line, run reduced_prefilter()
# Command line arguments are passed automatically by click
if __name__ == "__main__":
    reduce_prefilter()
