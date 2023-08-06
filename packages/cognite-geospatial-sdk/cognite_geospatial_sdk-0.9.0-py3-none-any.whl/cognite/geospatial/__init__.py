# Copyright 2020 Cognite AS
# flake8: noqa

__docformat__ = "restructuredtext"
from cognite.geospatial._geospatial_client import CogniteGeospatialClient
from cognite.geospatial.error import GeospatialError
from cognite.geospatial.types import (
    DataExtractor,
    Geometry,
    SpatialItem,
    SpatialList,
    SpatialRelationship,
    UpdateSpatialItem,
)

from ._console import in_ipython_frontend
from ._version import get_version

__version__ = get_version()

del get_version


# Print banner
if in_ipython_frontend():
    from IPython.display import HTML, display

    display(HTML("Cognite Geospatial SDK <strong>%s</strong>" % __version__))

    del in_ipython_frontend, display, HTML

# module level doc-string
__doc__ = """
cognite-geospatial-sdk - a geospatial SDK to work with Cognite DatA Fusion (CDF) for Python
=====================================================================
**geospatial** is a Python package providing flexible access to spatial data.
Main Features
-------------
Here are just a few of the things that geospatial does well:
  - Create geospatial object
  - Search geospatial object on the space
  - Extra functionality to work with one spatial object
"""
