import logging
from os.path import join

import matplotlib.pyplot as plt
import numpy as np

from astropy.io import fits

from vtfcal.test_constants import TEST_PIXEL, TEST_WL_IDX


def plotframes(data_tree, frames, outname, raw=False):
    logger = logging.getLogger(__name__)
    logger.setLevel("INFO")

    nframes = len(frames)
    nrows = np.int(np.ceil(nframes / 4))
    ncols = min(nframes, 4)
    plotshape = (nrows, ncols)
    figsize = (8 * (ncols + 1), 8 * nrows)  # Same for this

    fig, ax = plt.subplots(*plotshape, figsize=figsize)
    try:
        ax = ax.flatten()
    except AttributeError:
        ax = [ax]

    for i, (dkey, title) in enumerate(frames):
        keybase = "raw" if raw else "support"
        logger.debug(f"{keybase} {dkey}")
        files = data_tree[keybase][dkey]
        if len(files) == 1:
            imgfile = files[0].fileuri
        else:
            imgfile = [f.fileuri for f in files if f"l{TEST_WL_IDX:02}" in f.fileuri][
                0
            ]
        logger.debug(imgfile)

        dat = np.array(fits.open(imgfile)[0].data)
        # vmin = 0 if not (dat < 0).any() else np.nanpercentile(dat, 1)
        vmin = np.nanpercentile(dat, 1)
        vmax = np.nanpercentile(dat, 99)
        if ((dat < 0).any() and (dat > 0).any()):
            cmap = "coolwarm"
            vext = max(abs(vmax), abs(vmin))
            vmin, vmax = -vext, vext
        else:
            cmap = "magma" if "data" in dkey else "viridis"

        plt.sca(ax[i])
        plt.imshow(dat, cmap=cmap, vmin=vmin, vmax=vmax)
        plt.title(title)
        plt.plot(TEST_PIXEL[0], TEST_PIXEL[1], "x", color="black")

        plt.colorbar()

    plt.savefig(join(data_tree["plots"], outname), bbox_inches="tight")
    plt.close()
