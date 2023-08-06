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

from vtfcal.utils import add_files_by_keywords


def init_data_tree(indir):
    """
    Initiate a set of data trees for describing the calibration data structure.

    Creates and saves an :class:`~asdf.AsdfFile` for each VTF camera and initialises them with
    `inidir` and `outdir` as input and output directories, respectively. Also defines for each file
    whether the data are broadband or narrowband images.

    \b
    Parameters
    ----------
    indir : str or :class:`pathlib.Path`
        Directory in which raw input is stored.

    \b
    outdir : str or :class:`pathlib.Path`
        Directory to which intermediate and final output files will be saved.
    """

    channels = [("bb", "broadband"), ("nb1", "narrowband1"), ("nb2", "narrowband2")]

    for short, long_ in channels:
        tree = {
            # Would use pathlib for these but asdf can't represent it
            "raw": {"data_dir": join(indir, "raw", long_)},
            "support": {"data_dir": join(indir, "support", long_)},
            "processed": {"data_dir": join(indir, "processed", long_)},
            "polarization": {"data_dir": join(indir, "raw", "polarization")},
            "plots": join(indir, "plots", long_),
            "mode": "broadband" if short == "bb" else "narrowband",
            "speckle": {"data_dir": join(indir, "raw", "speckle")},
        }

        f = join(indir, f"{short}_data_tree")
        asdf_file = asdf.AsdfFile(tree, uri=f)
        asdf_file = add_files_by_keywords(asdf_file, "darks", {"DKIST003": "dark"}, raw=True)
        # Header key indicating channel isn't in the format I'm using for tracking files
        chankey = short.upper().replace("1", "+").replace("2", "-")
        for dkey, head_kw in zip(["flats", "data"], ["gain", "observe"]):
            for m in range(4):
                asdf_file = add_files_by_keywords(
                    asdf_file,
                    f"{dkey} modstate{m}",
                    {"VTF__002": chankey, "VTF__031": m, "DKIST003": head_kw},
                    raw=True,
                )
