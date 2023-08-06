# Copyright 2020 Cognite AS

import copy

import numpy as np

from .affine import AffineTransformation
from .index import Index2, Position2


class GeometryDefinition:
    def __init__(self):
        """Geometry definition of the grid
        """
        # real world
        self._origin = Position2(0.0, 0.0)
        # top_left_x, top_left_y
        self._top_left = Position2(0.0, 0.0)
        # top_right_x,top_right_y
        self._top_right = Position2(0.0, 0.0)
        # bottom_right_x,bottom_right_y
        self._bottom_right = Position2(0.0, 0.0)
        #  bottom_left_x,bottom_left_y
        self._bottom_left = Position2(0.0, 0.0)
        self._space_xy = Position2(1.0, 1.0)

        # grid
        # row_step,column_step
        self._space_ij = Index2(1, 1)
        # row_min,column_min
        self._grid_top_left = Index2(0, 0)
        # row_max,column_max
        self._grid_bottom_right = Index2(0, 0)
        self._grid_origin = Index2(0, 0)

        self._rotation_ij = Position2(0.0, 0.0)

        # affine transformation (identity)
        self._affine = AffineTransformation()

    # Real word properties
    @property
    def origin(self) -> Position2:
        """Get origin of the geometry

        Returns:
            Position2 - X, Y origin
        """
        return self._origin

    @origin.setter
    def origin(self, origin):
        """Set the origin of geometry

        Args:
            origin (array|Position2): Origin X, Y
        """
        self._origin = Position2(origin)

        # update tranformation
        self._affine = self.affine.get_translation(self._origin)

    @property
    def space_xy(self) -> Position2:
        """Get space in 2D cartesian plane between near points.

        Returns:
            Position2 - X, Y space
        """
        return self._space_xy

    @space_xy.setter
    def space_xy(self, space_xy):
        """Set space in 2D cartesian plane between near points.

        Args:
            space_xy (array|Position2): Space X, Y direction
        """
        self._space_xy = Position2(space_xy)

        # update tranformation
        self._affine = self.affine.get_scale(self._space_xy)

    @property
    def top_left(self) -> Position2:
        """Get top left corner coordinates

        Returns:
            Position2 - X, Y top left position
        """
        return self._top_left

    @top_left.setter
    def top_left(self, top_left):
        """Set top left corner coordinates

        Args:
            top_left (array, Position2): X, Y top left position
        """
        self._top_left = Position2(top_left)

    @property
    def top_right(self) -> Position2:
        """Get top right corner coordinates

        Returns:
            Position2 - X, Y top right position
        """
        return self._top_right

    @top_right.setter
    def top_right(self, top_right):
        """Set top right corner coordinates

        Args:
            top_right (array, Position2): X, Y top right position
        """
        self._top_right = Position2(top_right)

    @property
    def bottom_right(self) -> Position2:
        """Get bottom right corner coordinates

        Returns:
            Position2 - X, Y bottom right position
        """
        return self._bottom_right

    @bottom_right.setter
    def bottom_right(self, bottom_right):
        """Set bottom right corner coordinates

        Args:
            bottom_right (array, Position2): X, Y bottom right position
        """
        self._bottom_right = Position2(bottom_right)

    @property
    def bottom_left(self) -> Position2:
        """Get bottom left corner coordinates

        Returns:
            Position2 - X, Y bottom left position
        """
        return self._bottom_left

    @bottom_left.setter
    def bottom_left(self, bottom_left):
        """Set bottom left corner coordinates

        Args:
            bottom_left (array, Position2): X, Y bottom left position
        """
        self._bottom_left = Position2(bottom_left)

    @property
    def extent(self):
        """Extend in 2D cartesian plane

        Returns:
            array 4 coordinates
        """
        return np.array([self.top_left, self.top_right, self.bottom_right, self.bottom_left])

    @extent.setter
    def extent(self, extent):
        """Set extend in 2D cartesian plane

        Args:
            extent (array): 4 coordinates (top left, top rigth, bottom left, bottom right)
        """
        ext = np.array(extent)
        min_x = ext[0::2].min()
        max_x = ext[0::2].max()
        min_y = ext[1::2].min()
        max_y = ext[1::2].min()
        self.top_left = [min_x, max_y]
        self.top_right = [max_x, max_y]
        self.bottom_left = [min_x, min_y]
        self.bottom_right = [max_x, min_y]

    @property
    def min_x(self):
        """Get min X coordinate of extend

        Returns:
            min X position
        """
        return np.min([self.top_left.i, self.top_right.i, self.bottom_left.i, self.bottom_right.i])

    @property
    def max_x(self):
        """Get max X coordinate of extend

        Returns:
            max X position
        """
        return np.max([self.top_left.i, self.top_right.i, self.bottom_left.i, self.bottom_right.i])

    @property
    def min_y(self):
        """Get min Y coordinate of extend

        Returns:
            min Y position
        """
        return np.min([self.top_left.j, self.top_right.j, self.bottom_left.j, self.bottom_right.j])

    @property
    def max_y(self):
        """Get max Y coordinate of extend

        Returns:
            max Y position
        """
        return np.max([self.top_left.j, self.top_right.j, self.bottom_left.j, self.bottom_right.j])

    # Grid properties
    @property
    def space_ij(self) -> Index2:
        """Get space between two nearest points in a grid

        Returns:
            array space in I and J direction
        """
        return self._space_ij

    @space_ij.setter
    def space_ij(self, space_ij):
        """Set space between two nearest points in a grid

        Args:
            space_ij (array|Index2): space in I and J direction
        """
        self._space_ij = Index2(space_ij)

    @property
    def grid_top_left(self) -> Index2:
        """Get top left grid index

        Returns:
            array top left I and J
        """
        return self._grid_top_left

    @grid_top_left.setter
    def grid_top_left(self, grid_top_left):
        """Set top left grid index

        Args:
            grid_top_left (array|Index2): top left I and J
        """
        self._grid_top_left = Index2(grid_top_left)

    @property
    def grid_bottom_right(self) -> Index2:
        """Get bottom right grid index

        Returns:
            array bottom right I and J
        """
        return self._grid_bottom_right

    @grid_bottom_right.setter
    def grid_bottom_right(self, grid_bottom_right):
        """Set bottom right grid index

        Args:
            grid_bottom_right (array|Index2): bottom right I and J
        """
        self._grid_bottom_right = Index2(grid_bottom_right)

    @property
    def grid_min_i(self):
        return self.grid_top_left.i

    @property
    def grid_max_i(self):
        return self.grid_bottom_right.i

    @property
    def grid_min_j(self):
        return self.grid_top_left.j

    @property
    def grid_max_j(self):
        return self.grid_bottom_right.j

    @property
    def grid_height(self):
        """Grid height

        Returns:
            int - height of the grid
        """
        return self.grid_max_i - self.grid_min_i + 1

    @property
    def grid_width(self):
        """Grid width

        Returns:
            int - width of the grid
        """
        return self.grid_max_j - self.grid_min_j + 1

    @property
    def grid_origin(self):
        """Get grid origin I, J

        Returns:
            array - origin of the grid I, J
        """
        return self._grid_origin

    @grid_origin.setter
    def grid_origin(self, grid_origin):
        """Set grid origin I, J

        Arga:
            grid_origin (array|Index2): origin of the grid I, J
        """
        self._grid_origin = Index2(grid_origin)

    @property
    def rotation_ij(self):
        """Rotation of I, J axis

        Returns:
            array - rotation in I, J
        """
        return self._rotation_ij

    @property
    def rotation_i(self):
        """Get rotation for I

        Returns:
            angle of I
        """
        return self._rotation_ij.i

    @property
    def rotation_j(self):
        """Get rotation for J

        Returns:
            angle of J
        """
        return self._rotation_ij.j

    @rotation_ij.setter
    def rotation_ij(self, rotations):
        """Set rotation of I, J axis

        Args:
            rotations (array): rotation in I, J
        """
        self._rotation_ij = Position2(rotations)
        # todo update transformation
        # self._affine = self._get_rotate(angle)

    @rotation_i.setter
    def rotation_i(self, theta):
        """Set rotation for I

        Args:
            angle (float): of I
        """
        self.rotation_ij = Position2(theta, -theta)

    @rotation_j.setter
    def rotation_j(self, theta):
        """Set rotation for J

        Args:
            angle (float): of J
        """
        self.rotation_ij = Position2(-theta, theta)

    @property
    def affine(self):
        """Affine transformation

        Returns:
            affine transformation of the grid
        """
        return self._affine

    @affine.setter
    def affine(self, affine):
        """Set affine transformation of the grid.

        Args:
            affine (array|AffineTransformation) - transformation
        """
        self._affine = AffineTransformation(affine)

        matrix = self._affine.matrix

        # this method update origin, rotation and space
        self._origin = Position2(matrix[2], matrix[5])
        self._space_xy = Position2(np.linalg.norm(matrix[[1, 4]]), np.linalg.norm(matrix[[0, 3]]))
        self._rotation_ij = Position2(
            np.arctan2(matrix[3], matrix[0]) - np.pi / 2.0, np.arctan2(matrix[1], matrix[4]) - np.pi / 2.0
        )

    def rotate(self, theta):
        """Rotate geometry

        Args:
            theta (float): angle
        """
        rotation = self.get_rotate(theta)
        rotated_geometry = copy.deepcopy(self)
        rotated_geometry.affine(rotation)
        return rotated_geometry

    def translate(self, origin):
        """Translate geometry

        Args:
            origin (array): X, Y
        """
        translation = self.affine.get_translation(origin)
        translated_geometry = copy.deepcopy(self)
        translated_geometry.affine(translation)
        return translated_geometry

    def scale(self, scale):
        """Scale geometry

        Args:
            scale (array): X, Y direction
        """
        scale = self.affine.get_scale(scale)
        scaled_geometry = copy.deepcopy(self)
        scaled_geometry.affine(scale)
        return scaled_geometry

    def xy_grid_mesh(self):
        """Get the meshgrid 2D

        Returns:
           (x, y) : 2D meshgrid array
        """
        xvec = np.linspace(self.min_x, self.max_x, self.grid_width)
        yvec = np.linspace(self.min_y, self.max_y, self.grid_height)
        return np.meshgrid(xvec, yvec)

    def row_column_grid_mesh(self):
        """Get the meshgrid 2D

        Returns:
           (r, c) : 2D meshgrid array
        """
        xvec = np.linspace(self.grid_min_j, self.grid_max_j, self.grid_width)
        yvec = np.linspace(self.grid_min_i, self.grid_max_i, self.grid_height)
        return np.meshgrid(xvec, yvec)

    def to_compute_grid_transformation(self, to_grid=False):
        """Translate grid points to origin and rotate them.
        """
        transformation = AffineTransformation()
        transformation = transformation.translate(-self.origin)
        transformation = transformation.rotate(self.rotation_i)

        if to_grid:
            transformation = transformation.scale(self.space_xy)
            transformation = transformation.translate(self.grid_origin)
        return transformation

    def __str__(self):
        return (
            f"Origin: {self.origin}\n"
            + f"Extent: {self.extent}\n"
            + f"AngleI: {self.rotation_ij.i} (rad), {np.rad2deg(self.rotation_ij.i)} (deg)\n"
            + f"AngleJ: {self.rotation_ij.j} (rad), {np.rad2deg(self.rotation_ij.j)} (deg)\n"
            + f"Grid: {self.grid_top_left}, {self.grid_bottom_right}\n"
            + f"SpaceI: {self.space_ij.i}  SpaceJ: {self.space_ij.j}\n"
            + f"SpaceX: {self.space_xy.x}  SpaceY: {self.space_xy.y}"
        )

    def __repr__(self):
        return self.__str__()
