# Copyright 2020 Cognite AS
from shapely.geometry import LineString

from ._util import plot_geometry, plot_grid_point


class Plot:
    @property
    def points(self):
        pass

    @property
    def extent(self):
        pass

    def plot_shape(self, label="Grid", title="Grid", xlabel="x", ylabel="y"):
        """ Plot raster grid using holoview.

        Note:
            holoview and datashader should be installed separately.

        Args:
            label (str): label of the geometry
            title (str): title of the plot
            xlabel (str): x axis label (default: x)
            ylabel (str): y axis label (default: y)
        Returns:
            holoview plot
        """
        points_array = self.points
        return plot_grid_point(points_array, label, title, xlabel, ylabel)

    def plot_extent(self):
        """ Plot extent box of spatial object

        Note:
            holoview should be installed separately.

        Returns:
            holoview plot
        """
        extent = self.extent
        return self._plot_line(
            points=extent, label="Extent", title="Extent in UTM-coordinates", xlabel="UTM-X", ylabel="UTM-Y"
        )

    def _plot_line(self, points, label=None, title=None, xlabel="x", ylabel="y"):
        line = points.tolist()
        line.append(line[0])
        geometry = LineString(line)
        return plot_geometry(
            geometry, label=label or "Attributes", title=title or "Attributes", xlabel=xlabel, ylabel=ylabel
        )
