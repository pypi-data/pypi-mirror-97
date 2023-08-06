#! /usr/bin/env python
import pkg_resources

__version__ = pkg_resources.get_distribution("pymt_topography").version


from .bmi import Topography

__all__ = [
    "Topography",
]
