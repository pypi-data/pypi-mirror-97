# Copyright 2020 Cognite AS
from typing import List

from cognite.geospatial._client import FeatureLayerDTO

from ._layer_metadata import LayerMetadata


class Layer(FeatureLayerDTO):
    def __init__(self, client, layer=None):
        self.client = client
        self.__dict__.update(layer.__dict__)
        self.items = None
        self._meta = None
        if layer is not None:
            self._meta = LayerMetadata(layer.metadata)

    def get_all_items(self, attributes: List[str] = None, output_crs: str = None, geometry_format: str = None):
        return self.client.get_layer_items(
            layer=self.name, attributes=attributes, output_crs=output_crs, geometry_format=geometry_format
        )
