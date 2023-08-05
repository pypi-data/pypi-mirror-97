# Copyright 2020 Cognite AS


def _split(line: str, size: int):
    if line is None:
        return None
    result = [x.strip() for x in line.split(",")]
    missing = size - len(result)
    if missing > 0:
        result.extend([None] * missing)
    return tuple(result)


class LayerMetadata:
    AXES = "AXES"
    ACTIVE = "ACTIVE"
    EXTENT = "EXTENT"
    GRID = "GRID"
    GRID_BOX = "GRID_BOX"
    GRID_STEP = "GRID_STEP"
    ROW_COLUMN = "ROW_COLUMN"
    WIDTH_HEIGHT = "WIDTH_HEIGHT"
    AFFINE_TRANSFORMATION = "AFFINE_TRANSFORMATION"

    def __init__(self, metadata: dict):
        self.metadata = metadata

    def axes(self):
        axes = self.metadata.get(LayerMetadata.AXES)
        return _split(axes, 3)

    def x(self):
        axes = self.axes()
        if axes is None:
            return None
        return axes[0]

    def y(self):
        axes = self.axes()
        if axes is None:
            return None
        return axes[1]

    def z(self):
        axes = self.axes()
        if axes is None:
            return None
        return axes[2]

    def active(self):
        return self.metadata.get(LayerMetadata.ACTIVE)

    def row_column(self):
        row_column = self.metadata.get(LayerMetadata.ROW_COLUMN)
        return _split(row_column, 2)

    def row(self):
        row_column = self.row_column()
        if row_column is None:
            return None
        return row_column[0]

    def column(self):
        row_column = self.row_column()
        if row_column is None:
            return None
        return row_column[1]

    def width_height(self):
        width_height = self.metadata.get(LayerMetadata.WIDTH_HEIGHT)
        return _split(width_height, 2)

    def width(self):
        width_height = self.width_height()
        if width_height is None:
            return None
        return width_height[0]

    def height(self):
        width_height = self.width_height()
        if width_height is None:
            return None
        return width_height[1]

    def extent(self):
        extent = self.metadata.get(LayerMetadata.EXTENT)
        return _split(extent, 8)

    def extent_top_left_x(self):
        extent = self.extent()
        if extent is None:
            return None
        return extent[0]

    def extent_top_left_y(self):
        extent = self.extent()
        if extent is None:
            return None
        return extent[1]

    def extent_top_right_x(self):
        extent = self.extent()
        if extent is None:
            return None
        return extent[2]

    def extent_top_right_y(self):
        extent = self.extent()
        if extent is None:
            return None
        return extent[3]

    def extent_bottom_right_x(self):
        extent = self.extent()
        if extent is None:
            return None
        return extent[4]

    def extent_bottom_right_y(self):
        extent = self.extent()
        if extent is None:
            return None
        return extent[5]

    def extent_bottom_left_x(self):
        extent = self.extent()
        if extent is None:
            return None
        return extent[6]

    def extent_bottom_left_y(self):
        extent = self.extent()
        if extent is None:
            return None
        return extent[7]

    def grid_box(self):
        grid = self.metadata.get(LayerMetadata.GRID_BOX)
        return _split(grid, 4)

    def grid_box_min_i(self):
        grid_box = self.grid_box()
        if grid_box is None:
            return None
        return grid_box[0]

    def grid_box_min_j(self):
        grid_box = self.grid_box()
        if grid_box is None:
            return None
        return grid_box[1]

    def grid_box_max_i(self):
        grid_box = self.grid_box()
        if grid_box is None:
            return None
        return grid_box[2]

    def grid_box_max_j(self):
        grid_box = self.grid_box()
        if grid_box is None:
            return None
        return grid_box[3]

    def grid_step(self):
        grid_step = self.metadata.get(LayerMetadata.GRID_STEP)
        return _split(grid_step, 2)

    def grid_step_i(self):
        grid_step = self.grid_step()
        if grid_step is None:
            return None
        return grid_step[0]

    def grid_step_j(self):
        grid_step = self.grid_step()
        if grid_step is None:
            return None
        return grid_step[1]

    def affine_transformation(self):
        affine_transformation = self.metadata.get(LayerMetadata.AFFINE_TRANSFORMATION)
        return _split(affine_transformation, 6)
