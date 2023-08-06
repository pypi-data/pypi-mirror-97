"""
Dark frame reduction

Average collected dark frames as appropriate to reduce to the smallest number required to calibrate
the science data.
"""

import ccdproc


def average_darks(darkfiles, outfile):
    # I feel like there should be a way of loading these all at once.
    # TODO Try just passing multiple filenames and see what it does
    frames = [ccdproc.CCDData.read(f.fileuri, format="fits", unit="adu") for f in darkfiles]

    # Obviously at the moment this just makes one averaged dark
    # Need to code in the unique exposure times part of it
    ## META: exposure times
    ccdproc.combine(frames, output_file=outfile)
