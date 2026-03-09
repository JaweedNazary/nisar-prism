import numpy as np

def doppler_partition_looks(slc, looks=9, az_axis=0):

    S = np.fft.fftshift(np.fft.fft(slc, axis=az_axis), axes=az_axis)

    n_az = slc.shape[az_axis]
    edges = np.linspace(0, n_az, looks + 1, dtype=int)

    output = []

    for i in range(looks):
        lo, hi = edges[i], edges[i+1]

        mask = np.zeros(n_az)
        mask[lo:hi] = 1

        shape = [1]*slc.ndim
        shape[az_axis] = n_az
        mask = mask.reshape(shape)

        Sb = S * mask
        Sb = np.fft.ifftshift(Sb, axes=az_axis)

        look = np.fft.ifft(Sb, axis=az_axis)

        output.append(look)

    return output


def combine_looks_complex(looks, groups):

    combined = []

    for g in groups:
        stack = np.stack([looks[i] for i in g])
        combined.append(np.mean(stack, axis=0))

    return combined
