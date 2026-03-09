import h5py
import matplotlib.pyplot as plt

from nisar_prism.io import read_complex_tile, apply_scale_factor
from nisar_prism.subaperture import doppler_partition_looks, combine_looks_complex
from nisar_prism.rgb import looks_to_rgb
from nisar_prism.geocode import find_az0_rg0_from_latlon

#############################################################
###  Replace the path with your NISAR file path            ##
#############################################################

H5_PATH = "NISAR_Missouri_20260117.h5"


#############################################################
###  replace the lat and lon  with the site of interest    ##
#############################################################

lat = 38.973889
lon = -91.957968




freq = "frequencyA"
pol = "HH"

img_path = f"science/LSAR/RSLC/swaths/{freq}/{pol}"


az0, rg0, _ = find_az0_rg0_from_latlon(
    H5_PATH,
    img_path,
    lat,
    lon,
    layer=2
)


with h5py.File(H5_PATH) as h5:

    dset = h5[img_path]

    slc = read_complex_tile(
        dset,
        tile_az=5000,
        tile_rg=5000,
        az0=az0-2500,
        rg0=rg0-2500
    )

    slc = apply_scale_factor(h5, freq, pol, slc)

    looks = doppler_partition_looks(slc, looks=12, az_axis=1)

    groups = [(0,1,2,3),(4,5,6,7),(8,9,10,11)]

    looks3 = combine_looks_complex(looks, groups)

    rgb = looks_to_rgb(looks3, gamma=0.3)


plt.figure(figsize=(10,10))
plt.imshow(rgb, origin="lower")
plt.title("NISAR Sub-aperture RGB")
plt.show()
