import numpy as np


def robust_unit_scale(x, low=1, high=99):

    lo = np.percentile(x, low)
    hi = np.percentile(x, high)

    y = (x - lo) / (hi - lo + 1e-12)

    return np.clip(y, 0, 1)


def looks_to_rgb(looks, gamma=0.9):

    channels = []

    for lk in looks:

        inten = np.abs(lk)**2
        inten = np.log10(inten + 1e-12)

        inten = robust_unit_scale(inten)

        inten = inten ** (1/gamma)

        channels.append(inten)

    rgb = np.stack(channels, axis=-1)

    return (rgb*255).astype(np.uint8)
