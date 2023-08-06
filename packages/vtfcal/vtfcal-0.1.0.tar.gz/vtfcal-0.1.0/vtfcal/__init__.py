# Licensed under a 3-clause BSD style license - see LICENSE.rst

# Packages may add whatever they like to this file, but
# should keep this content at the top.
# ----------------------------------------------------------------------------
from ._dkist_init import *  # noqa: F403
# ----------------------------------------------------------------------------

if not _ASTROPY_SETUP_:  # noqa: F405
    # For egg_info test builds to pass, put package imports here.
    from .example_mod import *  # noqa: F401,F403

import logging
import logging.config


logging.basicConfig(level=logging.WARNING)
logging.config.dictConfig(
    {
        "version": 1,
        "loggers": {"astropy.nddata.ccddata": {"level": "WARNING"}},
        "disable_existing_loggers": True,
    }
)
