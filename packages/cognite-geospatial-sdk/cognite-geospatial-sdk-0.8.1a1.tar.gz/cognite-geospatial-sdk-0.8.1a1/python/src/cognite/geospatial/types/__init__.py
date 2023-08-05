# Copyright 2020 Cognite AS
# flake8: noqa
from enum import Enum
from typing import Dict, List, NamedTuple

from cognite.geospatial._client import SpatialRelationshipNameDTO

from ._basic import Geometry, SpatialItemId, TextBasedGeometry
from ._layer import Layer
from ._layer_metadata import LayerMetadata
from ._spatial_item import SpatialItem, SpatialList, UpdateSpatialItem


class SpatialRelationship(Enum):
    within = SpatialRelationshipNameDTO.WITHIN
    within_distance = SpatialRelationshipNameDTO.WITHINDISTANCE
    within_completely = SpatialRelationshipNameDTO.WITHINCOMPLETELY
    intersect = SpatialRelationshipNameDTO.INTERSECT
    within_3d = SpatialRelationshipNameDTO.WITHIN3D
    within_distance_3d = SpatialRelationshipNameDTO.WITHINDISTANCE3D
    within_completely_3d = SpatialRelationshipNameDTO.WITHINCOMPLETELY3D
    intersect_3d = SpatialRelationshipNameDTO.INTERSECT3D


class DataExtractor(NamedTuple):
    attribute: str
    min_val: str
    max_val: str


class GridCoverage:
    """Map from a line to list of cross points
    """

    def __init__(self, cross_points_map: Dict[int, List[int]]):
        self.cross_points_map = cross_points_map

    def get_cross_points(self, line: int):
        """

        Args:
            line (int): the line number

        Returns:
            List[int]: a list of cross points on this line
        """
        return self.cross_points_map.get(line, [])

    def __str__(self):
        return "\n".join(["line {} -> {}".format(key, value) for key, value in self.cross_points_map.items()])
