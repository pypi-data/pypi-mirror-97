# Copyright 2020 Cognite AS

import copy

import numpy as np
from cognite.geospatial.visualization import Plot
from scipy.interpolate import griddata

from .geometry_definition import GeometryDefinition
from .index import Index2, Position2


class Surface(Plot):
    def __init__(self, data, grid=None, geometry: GeometryDefinition = None, name: str = None):
        self.name = name
        self.data = data
        self.grid = grid
        self.is_gridded = grid is not None
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

    @property
    def points(self):
        return self.data

    @property
    def extent(self):
        return self.geometry.extent

    def window(self, row_range, column_range):
        """Window (crop) out part of the surface.

        Args:
            row_range (array): A window for row (min,max)
            column_range (array): A window for column (min,max)

        Returns:
            Surface within a window
        """
        if not self.is_gridded:
            raise Exception("Surface not grided! Grid the surface before using this function.")

        row_ind = Index2(row_range)
        col_ind = Index2(column_range)
        indexes = np.argwhere(
            (self.grid[:, 0] >= row_ind.i)
            & (self.grid[:, 0] < row_ind.j)
            & (self.grid[:, 1] >= col_ind.i)
            & (self.grid[:, 1] < col_ind.j)
        )
        indexes = indexes.reshape(len(indexes))
        filtered_grid = np.array(self.grid[indexes], copy=True)
        filtered_data = np.array(self.data[indexes], copy=True)

        filtered_geometry = copy.deepcopy(self.geometry)
        filtered_geometry.grid_top_left = Index2(row_ind.i, col_ind.i)
        filtered_geometry.grid_bottom_right = Index2(row_ind.j - 1, col_ind.j - 1)

        min_coord = np.min(filtered_data, axis=0)
        max_coord = np.max(filtered_data, axis=0)

        filtered_geometry._top_left = Position2(min_coord[0], max_coord[1])
        filtered_geometry._top_right = Position2(max_coord[0:2])
        filtered_geometry._bottom_right = Position2(max_coord[0], min_coord[1])
        filtered_geometry._bottom_left = Position2(min_coord[0:2])

        return Surface(data=filtered_data, grid=filtered_grid, geometry=filtered_geometry, name=self.name)

    def sample(self, data_sampling):
        """Downsample surface

        Args:
            data_sampling (int): take each N point
        """
        data = np.array(self.data[::data_sampling, :], copy=True)
        sample_geometry = copy.deepcopy(self.geometry)

        min_coord = np.min(data, axis=0)
        max_coord = np.max(data, axis=0)

        sample_geometry._top_left = Position2(min_coord[0], max_coord[1])
        sample_geometry._top_right = Position2(max_coord[0:2])
        sample_geometry._bottom_right = Position2(max_coord[0], min_coord[1])
        sample_geometry._bottom_left = Position2(min_coord[0:2])

        grid = None
        if self.grid is not None:
            grid = np.array(self.grid[::data_sampling, :], copy=True)
            min_grid = np.min(grid, axis=0)
            max_grid = np.max(grid, axis=0)

            sample_geometry._grid_top_left = Index2(min_grid[0:2])
            sample_geometry._grid_bottom_right = Index2(max_grid[0:2])

        return Surface(data=data, grid=grid, geometry=sample_geometry, name=self.name)

    def interpolate_to_grid(self, method="cubic", fill_value=np.nan):
        X, Y = self.geometry.xy_grid_mesh()
        data_on_grid = griddata(self.data[:, :2], self.data[:, 2], (X, Y), method=method, fill_value=fill_value)
        data = np.stack((X.flatten(), Y.flatten(), data_on_grid.flatten()), axis=-1)
        row, column = self.geometry.row_column_grid_mesh()
        grid = np.stack((row.flatten(), column.flatten()), axis=-1)
        return Surface(data=data, grid=grid, geometry=copy.deepcopy(self.geometry), name=self.name)

    def _apply_transformation(self, transformation):
        points = transformation.transform(self.data[:, :2])
        return np.stack((points[:, 0], points[:, 1], self.data[:, 2]), axis=-1)

    def _update_geometry(self, transformation):
        new_geometry = copy.deepcopy(self.geometry)
        extent = [
            self.geometry.top_left,
            self.geometry.top_right,
            self.geometry.bottom_right,
            self.geometry.bottom_left,
            self.geometry.origin,
        ]
        new_extent = transformation.transform(extent)

        new_geometry.top_left = new_extent[0]
        new_geometry.top_right = new_extent[1]
        new_geometry.bottom_right = new_extent[2]
        new_geometry.bottom_left = new_extent[3]
        new_geometry.origin = new_extent[4]
        return new_geometry

    def translate(self, origin):
        """Translate surface to X, Y

        Args:
            origin (array): X, Y to translate points
        Returns:
            Translated Surface
        """
        transformation = self.geometry.affine.get_translation(origin)
        return self._apply_full(transformation)

    def rotate(self, theta):
        """Rotate surface

        Args:
            theta (float): angle
        Returns:
            Rotated Surface
        """
        transformation = self.geometry.affine.get_rotation(theta)
        return self._apply_full(transformation)

    def scale(self, scale):
        """Scale surface

        Args:
            scale (array): X, Y scale directions
        Returns:
            Scaled Surface
        """
        transformation = self.geometry.affine.get_scale(scale)
        return self._apply_full(transformation)

    def to_compute_grid(self, to_grid=False):
        """To compute grid
        """
        transformation = self.geometry.to_compute_grid_transformation(to_grid=to_grid)
        return self._apply_full(transformation)

    def _apply_full(self, transformation):
        new_data = self._apply_transformation(transformation)
        new_geometry = self._update_geometry(transformation)

        return Surface(data=new_data, grid=self.grid, geometry=new_geometry, name=self.name)

    def move_to_geometry(self, geometry, to_grid=False):
        """Move to geometry

        Args:
            geometry (GeometryDefinition): Move to geometry
        Returns:
            Moved Surface
        """
        transformation = geometry.to_compute_grid_transformation(to_grid=to_grid)
        return self._apply_full(transformation)

    def __str__(self):
        return f"Surface: {self.name}\nGeometry\n{self.geometry}"

    def __repr__(self):
        return self.__str__()
