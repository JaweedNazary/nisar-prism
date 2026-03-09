# nisar-prism

Generate **RGB sub-aperture radar images** from NISAR RSLC data with a prism-like visualization.

This tool extracts sub-aperture looks from SAR data and combines them into RGB images. The distinctive rainbow effect in some areas arises from **Bragg scattering conditions**—when the radar wavelength interacts with periodic structures on the surface—allowing polarization-dependent variations to appear as color.

---

## Scientific Background

The **sub-aperture SAR method** used in this package is based on the work of Ferro-Famil et al. (2003) ["Analysis of SAR Response Anisotropic Behavior Using Sub-Aperture Polarimetric Data"](https://ieeexplore.ieee.org/document/1293800), which demonstrates how splitting SAR data into azimuth sub-apertures allows observation of anisotropic scattering behaviors in complex scenes.

---

## Features

* Convert **latitude/longitude** to RSLC pixel indices.
* Extract **sub-aperture looks** along the Doppler axis.
* Combine sub-aperture looks into **RGB images**.
* Works **headless**, suitable for scripting and batch processing.

---

## Installation

Recommended: use a Python virtual environment.

```bash
pip install git+https://github.com/JaweedNazary/nisar-prism.git
```

---

## Usage Example

Generate an RGB sub-aperture image from a NISAR RSLC H5 file:

```bash
# Example: generate RGB sub-aperture images
python -m nisar_prism.cli path\to\your\nisar_file.h5 --lat 24.124 --lon 69.339 --freq frequencyA --pol HH --size 5000
```



### Parameters

* `--input` : Path to the RSLC HDF5 file containing the SAR data.
* `--lat` / `--lon` : Latitude and longitude of the target site. Must be within the RSLC frame.
* `--output` : File path to save the generated RGB image.
* `--subapertures` : Number of azimuth sub-apertures to extract (typically 3 for RGB visualization).
* `--freq` : Frequency band to use. Options: `frequencyA` or `frequencyB`.
* `--pol` : Polarization to use. `HH` or `VV` are recommended for man-made structures.
* `--size` : Tile size to process within the full NISAR scene. NISAR RSLC files are large (tens of GB), so use a value like `5000`–`8000` to avoid running out of memory.



The resulting image visualizes azimuth-dependent backscatter differences as red, green, and blue channels, highlighting anisotropic scattering features in the scene.

### Output

This colorized sub-aperture radar image, derived from L-band RSLC products from the NASA–ISRO Synthetic Aperture Radar, highlights an energy park within the salt-marsh landscape near the Luni River terminus in the Rann of Kutch, India. (lat = 24.124 and lon = 69.339)

<img width="1542" height="1536" alt="image" src="https://github.com/user-attachments/assets/d8135d40-77e0-44e9-be73-74e9a629cda1" />


---
Why the “Rainbow Effect” Appears

The rainbow-like colors in RGB sub-aperture SAR images arise from Bragg scattering conditions. When the radar wavelength interacts with periodic or quasi-periodic structures on the surface—like rows of vegetation, ripples, or man-made patterns—different sub-aperture looks capture slightly different backscatter amplitudes and phases. By mapping these sub-aperture signals to red, green, and blue channels, the anisotropic scattering behavior becomes visible as colorful patterns. Essentially, the color variations encode directional and polarization-dependent differences in the radar return.

### License

This project is developed by Jaweed Nazary in March of 2026 and is released under the MIT License. You are free to use, modify, and distribute the software under the terms of this license.
