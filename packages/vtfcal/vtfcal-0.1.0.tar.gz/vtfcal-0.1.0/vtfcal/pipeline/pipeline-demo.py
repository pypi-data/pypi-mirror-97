import warnings

from vtfcal.utils import RAW_DATA
from vtfcal.utils.preprocess_data import process

from vtfcal.pipeline import (align_frames, correct_darks, correct_flats, demodulate,
                             init_data_tree, reconstruct, reconstruct_broadband, reduce_darks,
                             reduce_flats, reduce_polcal, reduce_targets)

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)

dsid = "00000000"

# Perform initial pre-processing of simulated data
# Provides the proper folder structure, offsets frame alignment, and scales for reasonable run time
print("Preprocessing simulation data...", end="")
dataset_dir = process(raw_data_dir=RAW_DATA)
print("Done")

# Initiate data tree which tracks filenames and types of data frames
print("Initiating data tree...", end="")
init_data_tree(dataset_dir)
print("Done")
bb_data_tree = dataset_dir / "bb_data_tree"
nb1_data_tree = dataset_dir / "nb1_data_tree"
nb2_data_tree = dataset_dir / "nb2_data_tree"

# Reduce darks
print("Reducing dark frames...", end="")
reduce_darks(bb_data_tree)
reduce_darks(nb1_data_tree)
reduce_darks(nb2_data_tree)
print("Done")

# Reduce flats
print("Reducing flat frames...", end="")
reduce_flats(bb_data_tree)
reduce_flats(nb1_data_tree, correction=True, fourier=True)
reduce_flats(nb2_data_tree, correction=True, fourier=True)
print("Done")

# Reduce targets
print("Reducing target frames...", end="")
reduce_targets([bb_data_tree, nb1_data_tree, nb2_data_tree])
print("Done")

# Reduce prefilter not implemented

# Polarimetric calibration
print("Reducing polarimetric calibration frames...", end="")
reduce_polcal(nb1_data_tree)
reduce_polcal(nb2_data_tree)
print("Done")

# Dark correction
print("Dark-correcting science frames...", end="")
correct_darks(bb_data_tree)
correct_darks(nb1_data_tree)
correct_darks(nb2_data_tree)
print("Done")

# Flat correction
print("Flat-correcting science frames...", end="")
correct_flats(bb_data_tree)
correct_flats(nb1_data_tree)
correct_flats(nb2_data_tree)
print("Done")

# Data alignment
print("Aligning narrowband frames to broadband...", end="")
align_frames(nb1_data_tree)
align_frames(nb2_data_tree)
print("Done")

# Broadband reconstruction
# reconstruct_broadband(bb_data_tree)

# Narrowband reconstruction dependent on broadband reconstruction
reconstruct(nb1_data_tree, bb_tree=bb_data_tree)
reconstruct(nb2_data_tree, bb_tree=bb_data_tree)

# Demodulate reconstructed images
print("Demodulating narrowband frames...", end="")
demodulate(nb1_data_tree)
demodulate(nb2_data_tree)
print("Done")
