# Copyright 2020 Cognite AS

import numpy as np

from .geometry_definition import GeometryDefinition


class Surface:
    def __init__(self, data, geometry: GeometryDefinition = None, name: str = None, gridded: bool = False):
        self.name = name
        self.data = data
        self.is_gridded = gridded
        self.geometry = geometry

    @property
    def mean_x(self) -> float:
        return np.mean(self.data[:, 0])

    @property
    def mean_y(self) -> float:
        return np.mean(self.data[:, 1])

    @property
    def mean_z(self) -> float:
        return np.mean(self.data[:, 2])
