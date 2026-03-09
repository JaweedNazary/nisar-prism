"""
nisar-prism

Developed by Jaweed Nazary
University of Missouri-Columbia

A lightweight toolkit for generating RGB sub-aperture radar images
from NISAR RSLC data.

Main capabilities
-----------------
• Lat/Lon → RSLC pixel mapping
• Doppler sub-aperture decomposition
• RGB composite generation
"""

__version__ = "0.1.0"

from .io import read_complex_tile, apply_scale_factor
from .subaperture import doppler_partition_looks, combine_looks_complex
from .rgb import looks_to_rgb
from .geocode import find_az0_rg0_from_latlon

__all__ = [
    "read_complex_tile",
    "apply_scale_factor",
    "doppler_partition_looks",
    "combine_looks_complex",
    "looks_to_rgb",
    "find_az0_rg0_from_latlon",
]
