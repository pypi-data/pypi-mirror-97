from vtfcal.reconstruction.speckle import calc_fried_param, run_speckle
from pathlib import Path
from astropy.io import fits


def reconstruct(asdf_file):
    # Not sure if I should be doing this one per modstate or not?
    r0 = calc_fried_param()
    specframe = run_speckle(
        width=1024,
        height=1024,
        burst_directory="vtfTestImages",
        burst_prefix="cssSim_1024x1024",
        burst_suffix=".raw",
        burst_size=99,
        fixed_width=3,
        gpus=0,
        fried_parameter=r0,
    )

    outdir = asdf_file["support"]["data_dir"]
    fname = Path(outdir) / f"speckle-output.FITS"
    fits.writeto(fname, specframe, overwrite=True)

    return asdf_file
