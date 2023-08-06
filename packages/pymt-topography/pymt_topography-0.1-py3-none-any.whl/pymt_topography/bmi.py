from __future__ import absolute_import

import pkg_resources
from bmi_topography import BmiTopography as Topography

Topography.__name__ = "Topography"
Topography.METADATA = pkg_resources.resource_filename(__name__, "data/Topography")

__all__ = [
    "Topography",
]
