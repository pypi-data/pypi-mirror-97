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

from pathlib import Path

import PAC_Pipeline as pacp

import asdf
from astropy.time import Time

db_file = pacp.generic.get_default_telescope_db()


def fit_parameters(asdf_file):
    """"""
    # get directory of polcal frames and filename for parameter fits from data tree
    tree = asdf_file.tree
    poldir = asdf_file["polarization"]["data_dir"]
    outdir = Path(asdf_file["support"]["data_dir"])
    paramsfile = str(outdir / "polcal-fit-params.FITS")

    # call pa&c fit function
    pacp.FitCUParams.main(poldir, paramsfile, telescope_db=db_file)

    tree["polcal-fit-params"] = paramsfile
    new_asdf = asdf.AsdfFile(tree=tree, uri=asdf_file.uri)
    new_asdf.write_to(asdf_file.uri)


def gen_demod_matrix(asdf_file):
    """"""
    tree = asdf_file.tree
    poldir = Path(asdf_file["polarization"]["data_dir"])
    outdir = Path(asdf_file["support"]["data_dir"])
    paramsfile = asdf_file["polcal-fit-params"]
    demodfile = str(outdir / "polcal-demod-matrix.FITS")

    pacp.GenerateDemodMatrices.main(poldir, paramsfile, demodfile, telescope_db=db_file)

    tree["polcal-demod-matrices"] = demodfile
    new_asdf = asdf.AsdfFile(tree=tree, uri=asdf_file.uri)
    new_asdf.write_to(asdf_file.uri)


def gen_mueller_matrix(asdf_tree):
    """"""
    telescope = pacp.TelescopeModel.TelescopeModel(
        0, 0, 0
    )  ## obviously change these numbers to take from the headers
    obstime = Time("2020-01-31").mjd  # happy unification day
    obswave = 396.86  # nm
    telescope.load_from_database(db_file, obstime, obswave)

    mueller_matrix = telescope.generate_inverse_telescope_model()
