# Copyright 2020 Cognite AS
import json
from functools import lru_cache
from typing import List

import numpy as np
from cognite.geospatial.error import GeospatialError
from cognite.geospatial.shape import GeometryDefinition, Index2, Position2, Surface
from cognite.geospatial.vizualization._util import plot_geometry, plot_grid_point
from shapely import wkt
from shapely.geometry import LineString

from ._basic import Geometry

try:
    from collections.abc import Mapping  # noqa
    from collections.abc import MutableMapping  # noqa
except ImportError:
    from collections import Mapping  # noqa
    from collections import MutableMapping  # noqa


def _attributes_map(layer):
    if layer is None or layer.attributes is None:
        return {}
    attribute_map = {}
    for attribute in layer.attributes:
        attribute_map[attribute.name] = attribute
    return attribute_map


GEOMETRY_TYPES = [
    "point",
    "line",
    "polygon",
    "multipoint",
    "multiline",
    "multipolygon",
    "pointz",
    "linez",
    "polygonz",
    "multipointz",
    "multilinez",
    "multipolygonz",
    "surface",
]


def _is_geometry(layer_attribute):
    return layer_attribute.type in GEOMETRY_TYPES


def _is_number(layer_attribute):
    return layer_attribute.type in ["int", "long", "float", "double"]


class UpdateSpatialItem:

    visible_types = ["id", "external_id", "name", "description", "metadata", "asset_ids", "attributes", "source"]

    def __init__(
        self,
        name: str = None,
        id: int = None,
        external_id: str = None,
        description: str = None,
        metadata: dict = None,
        asset_ids: List[int] = None,
        source: str = None,
        attributes: dict = None,
    ):
        """Update Spatial item

            Args:
                name (str): spatial item name
                id (int): the id
                external_id (str): external_id reference
                description (str): the description
                metadata (dict): metadata of the object
                asset_ids (List[int]): a list of associated asset ids
                source (str): the source of the object
                attributes (dict): a map of attribute's name and value
        """
        self._name = name
        self._id = id
        self._external_id = external_id
        self._description = description
        self._metadata = metadata
        self._asset_ids = asset_ids
        self._source = source
        self._attributes = attributes

    @property
    def name(self) -> str:
        """Gets the name of spatial item.  # noqa: E501

        The name of the spatial item  # noqa: E501

        :return: The name of this spatial item.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of spatial item.

        The name of the spatial item  # noqa: E501

        :param name: The name of this spatial item.  # noqa: E501
        :type name: str
        """
        self._name = name

    @property
    def external_id(self) -> str:
        """Gets the external_id of spatial item.  # noqa: E501

        External Id provided by client. Should be unique within a given project/resource combination.  # noqa: E501

        :return: The external_id of this spatial item.  # noqa: E501
        :rtype: str
        """
        return self._external_id

    @external_id.setter
    def external_id(self, external_id: str):
        """Sets the external_id of spatial item.

        External Id provided by client. Should be unique within a given project/resource combination.  # noqa: E501

        :param external_id: The external_id of this spatial item.  # noqa: E501
        :type external_id: str
        """
        self._external_id = external_id

    @property
    def description(self) -> str:
        """Gets the description of spatial item.  # noqa: E501

        Textual description of the spatial item.  # noqa: E501

        :return: The description of this spatial item.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description: str) -> str:
        """Sets the description of spatial item.

        Textual description of the spatial item.  # noqa: E501

        :param description: The description of this spatial item.  # noqa: E501
        :type description: str
        """
        self._description = description

    @property
    def metadata(self) -> dict:
        """Gets the metadata of spatial item.  # noqa: E501

        Custom, application specific metadata. String key -> String value.  # noqa: E501

        :return: The metadata of this spatial item.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata: dict):
        """Sets the metadata of spatial item.

        Custom, application specific metadata. String key -> String value.  # noqa: E501

        :param metadata: The metadata of this spatial item.  # noqa: E501
        :type metadata: dict(str, str)
        """
        self._metadata = metadata

    @property
    def asset_ids(self) -> List[int]:
        """Gets the asset_ids of spatial item.  # noqa: E501

        Asset IDs of related asset resource item that this spatial item relates to.  # noqa: E501

        :return: The asset_ids of this spatial item.  # noqa: E501
        :rtype: list[int]
        """
        return self._asset_ids

    @asset_ids.setter
    def asset_ids(self, asset_ids: List[int]):
        """Sets the asset_ids of spatial item.

        Asset IDs of related asset resource item that this spatial item relates to.  # noqa: E501

        :param asset_ids: The asset_ids of this spatial item.  # noqa: E501
        :type asset_ids: list[int]
        """
        self._asset_ids = asset_ids

    @property
    def source(self) -> str:
        """Gets the source of spatial item.  # noqa: E501

        The source of this spatial item  # noqa: E501

        :return: The source of this spatial item.  # noqa: E501
        :rtype: str
        """
        return self._source

    @source.setter
    def source(self, source: str):
        """Sets the source of spatial item.

        The source of this spatial item  # noqa: E501

        :param source: The source of this spatial item.  # noqa: E501
        :type source: str
        """
        self._source = source

    @property
    def id(self) -> int:
        """Gets the id of  spatial item.  # noqa: E501

        A server-generated ID for the object.  # noqa: E501

        :return: The id of this spatial item.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id: int):
        """Sets the id of spatial item.

        A server-generated ID for the object.  # noqa: E501

        :param id: The id of this spatial item.  # noqa: E501
        :type id: int
        """
        self._id = id

    @property
    def attributes(self) -> dict:
        """Gets the attributes of spatial item..  # noqa: E501


        :return: The attributes of this spatial item.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._attributes

    @attributes.setter
    def attributes(self, attributes: dict):
        """Sets the attributes of spatial item..


        :param attributes: The attributes of this spatial item.  # noqa: E501
        :type attributes: dict(str, object)
        """

        self._attributes = attributes

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, UpdateSpatialItem):
            return False
        return self.to_dict() == other.to_dict()

    def __str__(self):
        return json.dumps(self.to_dict(), indent=2)

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        result = {}

        for attr in self.visible_types:
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(lambda x: x.to_dict() if hasattr(x, "to_dict") else x, value))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict())
                        if hasattr(item[1], "to_dict")
                        else (item[0], item[1].tolist())
                        if isinstance(item[1], (np.ndarray, np.generic))
                        else item,
                        value.items(),
                    )
                )
            else:
                result[attr] = value

        return result


class SpatialItem(UpdateSpatialItem, Geometry):
    visible_types = [
        "id",
        "external_id",
        "name",
        "description",
        "metadata",
        "asset_ids",
        "layer",
        "crs",
        "attributes",
        "created_time",
        "last_updated_time",
        "source",
    ]

    def __init__(
        self,
        name: str,
        layer: str,
        crs: str,
        id: int = None,
        external_id: str = None,
        description: str = None,
        metadata: dict = None,
        asset_ids: List[int] = None,
        source: str = None,
        attributes: dict = None,
        created_time: int = None,
        last_updated_time: int = None,
    ):
        """Spatial item

            Args:
                name (str): spatial item name
                layer (str): the layer to which the object belongs
                crs (str): the crs where geometry attributes are defined
                id (int): the id
                external_id (str): external_id reference
                description (str): the description
                metadata (dict): metadata of the object
                asset_ids (List[int]): a list of associated asset ids
                source (str): the source of the object
                attributes (dict): a map of attribute's name and value
                created_time (int): a created time of spatial item (managed by server)
                last_updated_time (int): an updated time of spatial item (managed by server)
        """
        super().__init__(
            name=name,
            id=id,
            external_id=external_id,
            description=description,
            metadata=metadata,
            asset_ids=asset_ids,
            source=source,
            attributes=attributes,
        )
        self._layer = layer
        self._crs = crs
        self._created_time = created_time
        self._last_updated_time = last_updated_time
        self._layer_info = None
        self.client = None

    @property
    def crs(self) -> str:
        """Gets the crs of spatial item.  # noqa: E501

        CRS specified using epsg:<number>  # noqa: E501

        :return: The crs of this spatial item.  # noqa: E501
        :rtype: str
        """
        return self._crs

    @crs.setter
    def crs(self, crs: str):
        """Sets the crs of spatial item.

        CRS specified using epsg:<number>  # noqa: E501

        :param crs: The crs of this spatial item.  # noqa: E501
        :type crs: str
        """
        self._crs = crs

    @property
    def layer(self) -> str:
        """Gets the layer of spatial item.  # noqa: E501

        The feature layer of this spatial item  # noqa: E501

        :return: The layer of this spatial item.  # noqa: E501
        :rtype: str
        """
        return self._layer

    @layer.setter
    def layer(self, layer: str):
        """Sets the layer of spatial item.

        The feature layer of this spatial item  # noqa: E501

        :param layer: The layer of this spatial item.  # noqa: E501
        :type layer: str
        """
        self._layer = layer

    @property
    def last_updated_time(self) -> int:
        """Gets the last_updated_time of spatial item.  # noqa: E501

        The number of milliseconds since 00:00:00 Thursday, 1 January 1970, Coordinated Universal Time (UTC), minus leap seconds.  # noqa: E501

        :return: The last_updated_time of this spatial item.  # noqa: E501
        :rtype: int
        """
        return self._last_updated_time

    @last_updated_time.setter
    def last_updated_time(self, last_updated_time: int):
        """Sets the last_updated_time of spatial item.

        The number of milliseconds since 00:00:00 Thursday, 1 January 1970, Coordinated Universal Time (UTC), minus leap seconds.  # noqa: E501

        :param last_updated_time: The last_updated_time of this  spatial item.  # noqa: E501
        :type last_updated_time: int
        """
        self._last_updated_time = last_updated_time

    @property
    def created_time(self) -> int:
        """Gets the created_time of spatial item.  # noqa: E501

        The number of milliseconds since 00:00:00 Thursday, 1 January 1970, Coordinated Universal Time (UTC), minus leap seconds.  # noqa: E501

        :return: The created_time of this  spatial item.  # noqa: E501
        :rtype: int
        """
        return self._created_time

    @created_time.setter
    def created_time(self, created_time: int):
        """Sets the created_time of spatial item.

        The number of milliseconds since 00:00:00 Thursday, 1 January 1970, Coordinated Universal Time (UTC), minus leap seconds.  # noqa: E501

        :param created_time: The created_time of this spatial item.  # noqa: E501
        :type created_time: int
        """
        self._created_time = created_time

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, SpatialItem):
            return False
        return (
            super().__eq__(other)
            and self._layer == other.layer
            and self._crs == other.crs
            and self._created_time == other.created_time
            and self._last_updated_time == other.last_updated_time
        )

    def _set_layer_info(self, layer):
        self._layer_info = layer

    def layer_info(self):
        """Get spatial item layer.
        """
        if self._layer_info is None:
            self._layer_info = self.client.get_layer(name=self._layer)
        return self._layer_info

    def _add_double(self, name: str, vector):
        self.attributes[name] = np.array(vector, dtype=np.double)

    def _add_integer(self, name: str, vector):
        self.attributes[name] = np.array(vector, dtype=np.int32)

    def _add_long(self, name: str, vector):
        self.attributes[name] = np.array(vector, dtype=np.int64)

    def _add_boolean(self, name: str, vector):
        self.attributes[name] = np.array(vector, dtype=bool)

    def _add_text(self, name: str, value):
        self.attributes[name] = value

    def __getitem__(self, name: str):
        if name in self.attributes:
            return self.attributes[name]

        attributes = self.client.get_attributes(attributes=[name], id=self._id)
        if name in attributes:
            return attributes[name]

        return None

    @lru_cache(maxsize=32)
    def coverage(self, dimensional_space: str = "2d", output_crs: str = None, geometry_format: str = None):
        """Retrieve the coverage of the spatial object.
        Args:
            dimensional_space (str): The geometry projection of the coverage. Valid values are "2d" (default), "3d"
            output_crs (str): the crs of the coverage
            geometry_format (str): Geometry format wkt or geojson
        """
        if output_crs is None:
            output_crs = self._crs

        coverage = self.client.get_coverage(output_crs=output_crs, id=self._id, dimensional_space=dimensional_space)
        if geometry_format is None or geometry_format == "wkt":
            return wkt.loads(coverage.coverage)

        return {"geojson": coverage}

    def delete(self) -> bool:
        """Delete spatial item.
        """
        item = self.client.delete_spatial(id=self._id)
        return item is not None

    def _layer_meta(self):
        if self._layer_info is None:
            self._layer_info = self.client.get_layer(self._layer)

            if self._layer_info is None:
                raise GeospatialError("Layer is not defined")
        return self._layer_info._meta

    def _geometry_definition(self) -> GeometryDefinition:
        geometry = GeometryDefinition()
        layer_meta = self._layer_meta()

        affine_transformation_name = layer_meta.affine_transformation()
        if affine_transformation_name is not None:
            affine_transformation = self[affine_transformation_name]
            if affine_transformation is not None:
                m = np.array(affine_transformation)
                geometry.affine = m
                geometry.origin = Position2(m[2], m[5])

                # distance between vectors
                geometry.space_xy = Position2(np.linalg.norm(m[[1, 4]]), np.linalg.norm(m[[0, 3]]))

                # rotation
                geometry.rotation_ij = Position2(
                    np.arctan2(m[3], m[0]) - np.pi / 2.0, np.arctan2(m[1], m[4]) - np.pi / 2.0
                )

        extent = layer_meta.extent()
        if extent is not None:
            geometry.top_left = Position2(self[layer_meta.extent_top_left_x()], self[layer_meta.extent_top_left_y()])
            geometry.top_right = Position2(self[layer_meta.extent_top_right_x()], self[layer_meta.extent_top_right_y()])
            geometry.bottom_right = Position2(
                self[layer_meta.extent_bottom_right_x()], self[layer_meta.extent_bottom_right_y()]
            )
            geometry.bottom_left = Position2(
                self[layer_meta.extent_bottom_left_x()], self[layer_meta.extent_bottom_left_y()]
            )

        grid_step = layer_meta.grid_step()
        if grid_step is not None:
            geometry.space_ij = Index2(self[layer_meta.grid_step_i()], self[layer_meta.grid_step_j()])

        grid_box = layer_meta.grid_box()
        if grid_box is not None:
            geometry.grid_top_left = Index2(self[layer_meta.grid_box_min_i()], self[layer_meta.grid_box_min_j()])
            geometry.grid_bottom_right = Index2(self[layer_meta.grid_box_max_i()], self[layer_meta.grid_box_max_j()])

        return geometry

    def surface(self) -> Surface:
        geometry = self._geometry_definition()
        data = self.get()
        return Surface(data, geometry, self.name, grided=True)

    def get(self):
        """ Get numpy arrays of x,y,z if the layer is raster/seismic/horizon. Otherwise, get geometry in the form of wkt
        """
        x_name, y_name, z_name = self._layer_meta().axes()
        x = self.__getitem__(x_name)
        y = self.__getitem__(y_name)

        if z_name is None:
            data = np.stack((x, y), axis=-1)
        else:
            z = self.__getitem__(z_name)
            data = np.stack((x, y, z), axis=-1)
        active_name = self._layer_meta().active()
        if active_name is None:
            return data
        active = self.__getitem__(active_name)
        if active is None:
            return data
        active = active[: len(data)]
        return data[active]

    def height(self):
        """ Get the difference between maximum and minimum inline
        """
        rows = self._row_min_max()
        return self._get_side_size(rows, self._layer_meta().height())

    def width(self):
        """ Get the difference between maximum and minimum xline
        """
        columns = self._column_min_max()
        return self._get_side_size(columns, self._layer_meta().width())

    def _get_side_size(self, min_max, size_name):
        if min_max is not None:
            min_ = self.__getitem__(min_max[0])
            max_ = self.__getitem__(min_max[1])
            if min_ is not None and max_ is not None:
                return int(max_) - int(min_) + 1
        elif size_name is not None:
            return self.__getitem__(size_name)
        return None

    def _row_min_max(self):
        minJ = self._layer_meta().grid_box_min_j()
        maxJ = self._layer_meta().grid_box_max_j()
        if minJ is not None and maxJ is not None:
            return (minJ, maxJ)

    def _column_min_max(self):
        minI = self._layer_meta().grid_box_min_i()
        maxI = self._layer_meta().grid_box_max_i()
        if minI is not None and maxI is not None:
            return (minI, maxI)
        return None

    def _xyz(self):
        xyz = self._layer_meta().axes()
        if len(xyz) == 2:
            return xyz + (None,)
        return xyz

    def _row_column(self):
        return self._layer_meta().row_column()

    def _height_name(self):
        return self._layer_meta().height()

    def _width_name(self):
        return self._layer_meta().width()

    def grid(self):
        """ Get the discrete grid representation if the layer is raster/seismic/horizon
        Seismic: grid[xline][inline] zero based index (grid[ xline - seismic_geo[“xline_min”] ][ inline - seismic_geo[“inline_min”] ]).
        """
        row_name, column_name = self._layer_meta().row_column()
        x_name, y_name, z_name = self._layer_meta().axes()

        x = self.__getitem__(x_name)
        y = self.__getitem__(y_name)

        if z_name is None:
            points = np.stack((x, y), axis=-1)
        else:
            z = self.__getitem__(z_name)
            points = np.stack((x, y, z), axis=-1)

        width = self.width()
        height = self.height()
        active_name = self._layer_meta().active()

        if active_name is None:
            rows = self.__getitem__(row_name)
            columns = self.__getitem__(column_name)
            if rows is None or columns is None:
                return None
            data = np.ndarray(shape=(height, width, points.shape[1]), dtype=np.double)
            for i in range(len(points)):
                r = rows[i] - rows.min()
                c = columns[i] - columns.min()
                data[r, c] = points[i]
        else:
            active = self.__getitem__(active_name)
            data = np.ndarray(shape=(width, height, points.shape[1]), dtype=np.double)
            size = len(active)
            active_indx = np.argwhere(active[:size] == True)  # noqa: E712
            for i in active_indx:
                r = int(i % height)
                c = int((i - r) / height)
                data[c, r] = points[i]

        return data

    def __hash__(self):
        return self._id

    def plot(self, attributes=None, label=None, title=None, xlabel="x", ylabel="y", output_crs=None):
        """ Plot coverage using holoview.

        Note:
            holoview should be installed separately.

        Args:
            attributes (List[str]): geometry attributes to visualize (default coverage)
            label (str): label of the geometry
            title (str): title of the plot
            xlabel (str): x axis label (default: x)
            ylabel (str): y axis label (default: y)
            output_crs (str): CRS of geometry
        Returns:
            holoview plot
        """
        plot = None
        if attributes is None:
            geometry = self.coverage(dimensional_space="2d", geometry_format="wkt", output_crs=output_crs)
            plot = plot_geometry(
                geometry, label=label or "Coverage", title=title or "Coverage", xlabel=xlabel, ylabel=ylabel
            )
        else:
            layer = self.layer_info()
            attribute_map = _attributes_map(layer)
            points = []
            for name in attributes:
                layer_attribute = attribute_map[name]
                value = self.__getitem__(name)
                if _is_geometry(layer_attribute):
                    geometry = wkt.loads(value)
                    if plot is None:
                        plot = plot_geometry(
                            geometry, label=label or name, title=title or name, xlabel=xlabel, ylabel=ylabel
                        )
                    else:
                        plot = plot * plot_geometry(
                            geometry, label=label or name, title=title or name, xlabel=xlabel, ylabel=ylabel
                        )
                elif _is_number(layer_attribute):
                    points.append(value)

            if len(points) > 0 and len(points) % 2 == 0:
                line = [(points[i], points[i + 1]) for i in range(0, len(points), 2)]
                line.append(line[0])
                geometry = LineString(line)
                if plot is None:
                    plot = plot_geometry(
                        geometry, label=label or "Attributes", title=title or "Attributes", xlabel=xlabel, ylabel=ylabel
                    )
                else:
                    plot = plot * plot_geometry(
                        geometry, label=label or "Attributes", title=title or "Attributes", xlabel=xlabel, ylabel=ylabel
                    )

        return plot

    def plot_compute_grid(self):
        """ Plot compute grid  using holoview. Supported only for seismic layer.

        Note:
            holoview should be installed separately.

        Returns:
            holoview plot
        """
        grid_box = self._layer_meta().grid_box()
        if grid_box is not None:
            return self.plot(
                attributes=[
                    grid_box[1],
                    grid_box[0],
                    grid_box[3],
                    grid_box[0],
                    grid_box[3],
                    grid_box[2],
                    grid_box[1],
                    grid_box[2],
                ],
                title="Grid in xline/inline",
                label="File",
                xlabel="inline",
                ylabel="xline",
            )
        return None

    def plot_bounding(self):
        """ Plot bounded box of spatial object

        Note:
            holoview should be installed separately.

        Returns:
            holoview plot
        """
        extent_name = self._layer_meta().extent()
        if extent_name is not None:
            return self.plot(
                attributes=list(extent_name),
                label="File",
                title="Grid in UTM-coordinates",
                xlabel="UTM-X",
                ylabel="UTM-Y",
            )

        geometry = self.coverage(dimensional_space="2d", geometry_format="wkt")
        if geometry is not None:
            (minx, miny, maxx, maxy) = geometry.bounds
            box_geometry = LineString([(minx, miny), (minx, maxy), (maxx, maxy), (maxx, miny), (minx, miny)])
            return plot_geometry(box_geometry, title="Grid in UTM-coordinates")

        return None

    def plot_grid(self, label="Grid", title="Grid", xlabel="x", ylabel="y"):
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
        points_array = self.get()
        return plot_grid_point(points_array, label, title, xlabel, ylabel)


class SpatialList(list):
    def __init__(self, client, layer_name: str = None):
        self.client = client
        self.layer_name = layer_name

    def plot(self, attributes=None, label=None, title=None, xlabel="x", ylabel="y", output_crs=None):
        """ Plot all geoemtries of the list using holoview.

        Note:
            holoview should be installed separately.

        Args:
            attributes (List[str]): geometry attributes to visualize (default coverage)
            label (str): label of the geometry
            title (str): title of the plot
            xlabel (str): x axis label (default: x)
            ylabel (str): y axis label (default: y)
            output_crs (str): CRS of geometry
        Returns:
            holoview plot
        """
        plot = None
        for item in self:
            if plot is None:
                plot = item.plot(
                    attributes=attributes, label=label, title=title, xlabel=xlabel, ylabel=ylabel, output_crs=output_crs
                )
            else:
                plot = plot * item.plot(
                    attributes=attributes, label=label, title=title, xlabel=xlabel, ylabel=ylabel, output_crs=output_crs
                )
        return plot
