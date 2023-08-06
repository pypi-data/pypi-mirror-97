import logging
import subprocess as subp

import numpy as np

from astropy.io import fits


def run_speckle(
    width=2048,
    height=2048,
    tile_size=128,
    burst_directory="/home/dkistdev/data",
    burst_prefix="bbso",
    burst_suffix=".pnm",
    burst_size=80,
    fixed_width=0,
    gpus=0,
    master_gpu=0,
    L1=0.949999988,
    L2=0.0900000036,
    iterations=10,
    out_prefix="byproducts",
    fried_parameter=0.100000001,
    wavelength=656.281982,
    pixel_scale=0.0170000009,
    diameter=4,
    dark=None,
    gain=None,
    npsd=None,
    init_with_mean=False,
    floats=False,
):

    logger = logging.getLogger(__name__)
    logger.setLevel("DEBUG")

    # Define bispectrum indices?
    # call spectral ratio library?
    # construct speckle class
    # read darks
    # read flats
    # read 'burst' image files
    # correct for darks and flats
    # sum images?
    # call reconstruction

    if not isinstance(gpus, int):
        gpus = {gpus}

    speckle_command = [
        "./testSpeckle",
        "-w",
        f"{width}",
        "-h",
        f"{height}",
        "-t",
        f"{tile_size}",
        "-d",
        f"{burst_directory}",
        "-p",
        f"{burst_prefix}",
        "-s",
        f"{burst_suffix}",
        "-n",
        f"{burst_size}",
        f"--fixed-width={fixed_width}",
        f"--gpus={gpus}",
        f"--master-gpu={master_gpu}",
        f"--L1={L1}",
        f"--L2={L2}",
        f"--iterations={iterations}",
        f"--fried-parameter={fried_parameter}",
        f"--wavelength={wavelength}",
        f"--pixel-scale={pixel_scale}",
        f"--diameter={diameter}",
    ]
    if dark:
        speckle_command.append(f"--dark={dark}")
    if gain:
        speckle_command.append(f"--gain={gain}")
    if npsd:
        speckle_command.append(f"--npsd={npsd}")
    if init_with_mean:
        speckle_command.append(f"--init-with-mean={init_with_mean}")
    if floats:
        speckle_command.append(f"--floats={floats}")

    subp.run(speckle_command)

    recon = np.fromfile("byproducts-reconstruction.raw", dtype="float32").reshape(
        (1024, 1024)
    )

    return recon


def calc_fried_param(
    dmActs2KlModes="./aotelem/dmActs2KlModes-default-f32.data",
    reconMatrixPrefix="./aotelem/RECON_MAT-",
    reconMatrixSuffix="Modes.data",
    klVariances="./aotelem/klVariances-default-f64.data",
    actCommands="./aotelem/actCommands.data",
    actErrors="./aotelem/actErrors.data",
    shifts="./aotelem/shifts.data",
    mode="1049Modes",
):

    logger = logging.getLogger(__name__)
    logger.setLevel("DEBUG")

    aotelem_command = [
        "./testAOTelemetry",
        f"--dmActs2KlModes={dmActs2KlModes}",
        f"--reconMatrixPrefix={reconMatrixPrefix}",
        f"--reconMatrixSuffix={reconMatrixSuffix}",
        f"--klVariances={klVariances}",
        f"--actCommands={actCommands}",
        f"--actErrors={actErrors}",
        f"--shifts={shifts}",
        f"--mode={mode}",
    ]

    out = subp.run(aotelem_command, capture_output=True, check=True, text=True)

    if "FriedParameter" in out.stdout:
        # This really wants to be somewhat more robust
        result = out.stdout.split("\n")[-2]
        r0 = result.split(" ")[-1]
    else:
        r0 = None

    return r0
