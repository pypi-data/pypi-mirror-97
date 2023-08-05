# Copyright 2020 Cognite AS

from .index import Index2, Position2


class GeometryDefinition:
    def __init__(self):
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

        # affine transformation
        self._affine = None

    # Real word properties
    @property
    def origin(self) -> Position2:
        return self._origin

    @origin.setter
    def origin(self, origin):
        self._origin = origin

    @property
    def space_xy(self) -> Position2:
        return self._space_xy

    @space_xy.setter
    def space_xy(self, space_xy: Position2):
        self._space_xy = space_xy

    @property
    def top_left(self) -> Position2:
        return self._top_left

    @top_left.setter
    def top_left(self, top_left: Position2):
        self._top_left = top_left

    @property
    def top_right(self) -> Position2:
        return self._top_right

    @top_right.setter
    def top_right(self, top_right: Position2):
        self._top_right = top_right

    @property
    def bottom_right(self) -> Position2:
        return self._bottom_right

    @bottom_right.setter
    def bottom_right(self, bottom_right: Position2):
        self._bottom_right = bottom_right

    @property
    def bottom_left(self) -> Position2:
        return self._bottom_left

    @bottom_left.setter
    def bottom_left(self, bottom_left: Position2):
        self._bottom_left = bottom_left

    # Grid properties
    @property
    def space_ij(self) -> Index2:
        return self.space_ij

    @space_ij.setter
    def space_ij(self, space_ij: Index2):
        self._space_ij = space_ij

    @property
    def grid_top_left(self) -> Index2:
        return self.grid_top_left

    @grid_top_left.setter
    def grid_top_left(self, grid_top_left: Index2):
        self._grid_top_left = grid_top_left

    @property
    def grid_bottom_right(self) -> Index2:
        return self._grid_bottom_right

    @grid_bottom_right.setter
    def grid_bottom_right(self, grid_bottom_right: Index2):
        self._grid_bottom_right = grid_bottom_right

    @property
    def affine(self):
        return self._affine

    @affine.setter
    def affine(self, affine):
        self._affine = affine

    def __str__(self):
        return ""
