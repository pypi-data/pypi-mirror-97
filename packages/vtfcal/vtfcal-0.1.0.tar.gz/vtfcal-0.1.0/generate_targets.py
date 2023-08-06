import configparser as cfp

import matplotlib.pyplot as plt
import numpy as np
from skimage.io import imread
from skimage.transform import AffineTransform, warp

from astropy.io import fits

from vtfcal.utils import RAW_DATA, DATA
from vtfcal.test_constants import TEST_DATA_SIZE

# Set up configuration to be saved out
cfg = cfp.ConfigParser()
cfg["camera-rotations"] = {}
cfg["camera-shifts"] = {}

# Load/create image
raw_image = imread("USAF-1951.png")[..., -1].astype("float64")
# Apply a small scaling across the target image
# This will make it easier to match corners from one image to another
raw_image *= np.linspace(0, 1, raw_image.shape[1])

fig, ax = plt.subplots(1, 3, figsize=(16, 4))
# For each image
for i, channel in enumerate(["broadband", "narrowband1", "narrowband2"]):
    # Apply smallish random rotation and shift
    rot = int((np.random.random() * 30) - 15)
    scale = TEST_DATA_SIZE[0] / np.array(raw_image.shape)  # Assumes square images
    c = np.cos(np.deg2rad(rot))
    s = np.sin(np.deg2rad(rot))
    rmatrix = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
    array_centre = np.array(TEST_DATA_SIZE) / 2.0
    displacement = np.dot(rmatrix[:2, :2], array_centre) - array_centre
    rmatrix[:2, 2] = -displacement
    rmatrix[:2, :2] *= scale
    tform = AffineTransform(matrix=rmatrix)
    new_image = warp(raw_image, tform.inverse, output_shape=TEST_DATA_SIZE, cval=-1)
    if channel == "broadband":
        ref_rot = rot

    # Update config and save out
    cfg["camera-rotations"][channel] = f"{rot:+02}"
    cfg["camera-shifts"][channel] = "0"

    # Save file out
    for m in range(4):
        fits.writeto(RAW_DATA / channel / f"modstate{m}" / "target.FITS", new_image, overwrite=True)
    ax[i].imshow(new_image)
    ax[i].set_title(f"Rotation: {rot:+.3f} (diff: {(ref_rot-rot):+.3f})")

# Save config out
# TODO This needs to interact properly with the cwd config file
with open(RAW_DATA / "calibration-config.cfg", "w") as cfgfile:
    cfg.write(cfgfile)

# Display the misaligned target images
plt.suptitle(f"Target images")

plt.savefig(DATA / "targets.png")
plt.close()
