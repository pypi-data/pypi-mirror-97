import dask.array as da
import dask.bytes
import matplotlib.pyplot as plt
import numpy as np
from dask_kubernetes import KubeCluster

from astropy.io import fits
from astropy.io.fits.hdu.base import BITPIX2DTYPE


def get_info(f):
    with f as fi:
        head = fits.getheader(fi, hdu=1)
    naxes = head["NAXIS"]
    dtype = BITPIX2DTYPE[head["BITPIX"]]
    shape = [head[f"NAXIS{n}"] for n in range(naxes, 0, -1)]
    return dtype, shape


class DelayedFits:
    def __init__(self, file, shape, dtype):
        self.shape = shape
        self.dtype = dtype
        self.file = file
        self.hdu = 0

    def __getitem__(self, item):
        with self.file as f:
            with self.file as f:
                with fits.open(f) as hdul:
                    hdul.verify("fix")
                    return hdul[self.hdu].data[item]


files = dask.bytes.open_files(
    "/home/drew/vtfcal/vtfcal/data/test_input/narrowband_t/modstate0/flat_*.fits.gz"
)
a = list(map(get_info, files))
for f in files:
    print(f.path)
n = np.array(a, dtype="object")
assert all([n[0, 0] == a for a in n[:, 0]])
assert all([n[0, 1] == a for a in n[:, 1]])
dtype = n[0, 0]
shape = n[0, 1]
arrs = [da.from_array(DelayedFits(fn, shape=shape, dtype=dtype), chunks=shape) for fn in files]
arr = da.stack(arrs)
print(arr)
plt.plot(arr[:, 512, 512].compute())
plt.show()
