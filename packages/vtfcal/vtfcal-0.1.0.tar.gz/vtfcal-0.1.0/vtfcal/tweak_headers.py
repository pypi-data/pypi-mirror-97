import glob

from astropy.io import fits

from dkist_data_model.generator import VTF

vtf = VTF(end_condition="1s")
h, c = list(vtf.generate_metadata("mode1"))[0]

for fname in glob.iglob("data/test_input/**/*.FITS", recursive=True):
    f = fits.open(fname)[0]
    for k, v in h.items():
        f.header[k] = v
        if k in list(c.keys()):
            f.header.comments[k] = c[k]
    # f.header.set('DNAXIS', 3)
    # f.header.set('DNAXIS1', 512)
    # f.header.set('DNAXIS2', 512)
    # f.header.set('DNAXIS3', 18)
    # f.header.set('DAAXES', 2)
    # f.header.set('DTYPE1', h['CTYPE1'])
    # f.header.set('DTYPE2', h['CTYPE2'])
    # f.header.set('DTYPE3', 'SPECTRAL')
    # f.header.set('DUNIT1', h['CUNIT1'])
    # f.header.set('DUNIT2', h['CUNIT2'])
    # f.header.set('DUNIT3', 'nm')
    # f.header.set('DPNAME1', 'spatial x')
    # f.header.set('DPNAME2', 'spatial y')
    # f.header.set('DPNAME3', 'lambda')
    # f.header.set('DWNAME1', 'helioprojetive latitude')
    # f.header.set('DWNAME2', 'helioprojective longitude')
    # f.header.set('DWNAME3', 'wavelength')
    # f.header.set('DINDEX3', 0)

    f.writeto(fname, overwrite=True)
