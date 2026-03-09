import argparse
import h5py
import matplotlib.pyplot as plt

from .io import read_complex_tile, apply_scale_factor
from .subaperture import doppler_partition_looks, combine_looks_complex
from .rgb import looks_to_rgb
from .geocode import find_az0_rg0_from_latlon


def main():

    parser = argparse.ArgumentParser(
        description="Generate RGB sub-aperture radar image from NISAR RSLC data."
    )

    parser.add_argument("h5", help="Path to NISAR RSLC HDF5 file")

    parser.add_argument("--lat", type=float, required=True)
    parser.add_argument("--lon", type=float, required=True)

    parser.add_argument("--freq", default="frequencyA")
    parser.add_argument("--pol", default="HH")

    parser.add_argument("--size", type=int, default=5000)
    parser.add_argument("--looks", type=int, default=12)

    parser.add_argument("--out", default="nisar_rgb.png")

    args = parser.parse_args()

    img_path = f"science/LSAR/RSLC/swaths/{args.freq}/{args.pol}"

    print("Finding radar coordinates...")

    az0, rg0, info = find_az0_rg0_from_latlon(
        args.h5,
        img_path,
        args.lat,
        args.lon,
        layer=2,
    )

    with h5py.File(args.h5) as h5:

        dset = h5[img_path]

        slc = read_complex_tile(
            dset,
            tile_az=args.size,
            tile_rg=args.size,
            az0=az0 - args.size // 2,
            rg0=rg0 - args.size // 2,
        )

        slc = apply_scale_factor(h5, args.freq, args.pol, slc)

        looks = doppler_partition_looks(
            slc,
            looks=args.looks,
            az_axis=1,
        )

        groups = [
            range(0, args.looks // 3),
            range(args.looks // 3, 2 * args.looks // 3),
            range(2 * args.looks // 3, args.looks),
        ]

        looks3 = combine_looks_complex(looks, groups)

        rgb = looks_to_rgb(looks3, gamma=0.3)

    plt.figure(figsize=(10, 10))
    plt.imshow(rgb, origin="lower")
    plt.axis("off")

    plt.savefig(args.out, dpi=200)

    print(f"RGB image saved to {args.out}")
