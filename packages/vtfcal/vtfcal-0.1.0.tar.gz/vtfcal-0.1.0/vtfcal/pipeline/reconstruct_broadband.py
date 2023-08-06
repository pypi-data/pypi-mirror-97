"""
"""

import logging
from pathlib import Path
import asdf
from vtfcal.reconstruction.broadband import reconstruct

def reconstruct_broadband(data_tree):
    """
    """

    logger = logging.getLogger(__name__)
    asdf_file = asdf.open(data_tree, mode="rw")

    if asdf_file["mode"] != "broadband":
        raise ValueError(
            f'Invalid data mode keyword in asdf tree: {asdf_file["mode"]} '
            'Speckle reconstruction is only applicable to data with "mode": "broadband"')

    asdf_file = reconstruct(asdf_file)

    asdf_file.close()
