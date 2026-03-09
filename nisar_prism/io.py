import numpy as np
import h5py

def read_complex_tile(dset, tile_az=1000, tile_rg=1000, az0=None, rg0=None):
    n_az, n_rg = dset.shape

    tile_az = min(tile_az, n_az)
    tile_rg = min(tile_rg, n_rg)

    if az0 is None:
        az0 = (n_az - tile_az) // 2
    if rg0 is None:
        rg0 = (n_rg - tile_rg) // 2

    az1 = min(n_az, az0 + tile_az)
    rg1 = min(n_rg, rg0 + tile_rg)

    return np.asarray(dset[az0:az1, rg0:rg1])


def apply_scale_factor(h5, freq, pol, slc):
    path = f"science/LSAR/RSLC/metadata/calibrationInformation/{freq}/{pol}/scaleFactor"

    if path in h5:
        sf = float(h5[path][()])
        return slc * sf

    return slc
