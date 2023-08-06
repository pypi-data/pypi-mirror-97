# Copyright 2020 Cognite AS
import pprint


class TextBasedGeometry:
    def __init__(self, geojson=None, crs: str = None, wkt: str = None):
        self.geojson = geojson
        self.crs = crs
        self.wkt = wkt

    def __repr__(self):
        return pprint.pformat(vars(self))


class SpatialItemId:
    def __init__(self, id: int = None, external_id: str = None):
        self.id = id
        self.external_id = external_id

    def __repr__(self):
        return pprint.pformat(vars(self))


class Geometry(SpatialItemId, TextBasedGeometry):
    def __init__(
        self, id: int = None, external_id: str = None, wkt: str = None, crs: str = None, geojson: object = None
    ):
        self.id = id
        self.external_id = external_id
        self.geojson = geojson
        self.crs = crs
        self.wkt = wkt

    def __repr__(self):
        return pprint.pformat(vars(self))
