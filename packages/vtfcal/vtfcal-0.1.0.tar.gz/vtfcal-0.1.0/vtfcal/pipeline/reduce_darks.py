"""
Dark frame reduction

Average collected dark frames as appropriate to reduce to the smallest number required to calibrate
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

from os.path import join

import asdf

from vtfcal.utils import average_all

PATH = join("/", "home", "drew", "DKIST" "vtfcal", "vtfcal")


## TODO Change this and other functions to take a FOLDER, not a file, and to look there for an appropriate asdf file
## Will mean most functions needing to take a channel keyword also
## Possibly specify default asdf file location in a config file?
## Also most of the content of this function should be moved to one in the vtfcal package
## More generally, these command-line functions should do as little as possible,
## other than calling the appropriate vtfcal function and minor asdf file-handling
def reduce_darks(data_tree):
    """
    Function to reduce VTF dark frames

    Loads all available dark frames from the input directory specified by `data_tree`. These are
    averaged into a single frame, which is saved to the appropriate output directory. A reference to
    the averaged dark file is also added to `data_tree` for use later in the calibration process.

    \b
    Parameters
    ----------
    data_tree : string or :class:`pathlib.Path`
        Path to an :class:`~asdf.AsdfFile` defining the input and output data directories for the
        calibration, and whether the data are broadband or narrowband images. See
        :meth:`commands.init_data_tree` for generating an appropriate file.
    """

    tree = asdf.open(data_tree, mode="rw")

    ## REFACTOR: This will average broadband darks by wavelength as well which I don't want
    average_all(tree, "darks")
