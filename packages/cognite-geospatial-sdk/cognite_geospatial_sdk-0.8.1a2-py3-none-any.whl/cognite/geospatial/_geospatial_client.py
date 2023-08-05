# Copyright 2020 Cognite AS
"""Cognite Geospatial API store and query spatial data.

 Spatial objects represent a revision of an object present in a geographic position at a point
 in time (or for all time if no time is specified). The object has a position according to a
 specific coordinate reference system and can be a point, linestring, polygon, or surface
 defined by a position in 3-dimensional space. Within the defined area, the object can have
 attributes or values associated with more specific points or areas.

"""
import base64
import os
import tempfile
from functools import lru_cache
from typing import Dict, List, Optional, Union

import numpy as np
import pyarrow as pa
from cognite import geospatial as geospatial
from shapely import wkt
from shapely.geometry import shape
from shapely.geometry.base import BaseGeometry

from ._client import (
    AttributeTypeDTO,
    Configuration,
    CreateSpatialItemsDTO,
    DataExtractorDTO,
    EitherIdDTO,
    FeatureLayerNameDTO,
    FeatureLayersFilterDTO,
    GeometryDTO,
    GeometryItemsDTO,
    GridCoverageRequestDTO,
    InternalIdDTO,
    IntersectionQueryDTO,
    ItemAttributeDTO,
    ItemAttributesDTO,
    SpatialApi,
    SpatialCoverageRequestDTO,
    SpatialDataRequestDTO,
    SpatialIdsDTO,
    SpatialRelationshipDTO,
    SpatialSearchRequestDTO,
    TextBasedGeometryDTO,
    UpdateSpatialItemsDTO,
)
from ._retry_client import RetryApiClient
from ._spatial_filter_object import SpatialFilterObject
from .error import GeospatialError, api_exception_handler
from .types import (
    DataExtractor,
    Geometry,
    GridCoverage,
    Layer,
    SpatialItem,
    SpatialItemId,
    SpatialList,
    SpatialRelationship,
    TextBasedGeometry,
    UpdateSpatialItem,
)
from .utils._token_generator import TokenGenerator

from ._util import (  # _check_either_external_id,; _filter_simple_attributes,
    _check_external_id,
    _check_id,
    _create_spatial_id,
    _create_spatial_ids,
    _decode_attribute,
    _filter_list_attributes,
    _first_item,
    _get_response_items,
    _is_primitive,
    _single_or_array,
    _to_array,
    _to_core_geometry_spatial_item,
    _to_spatial_items,
    _to_update_spatial_item,
    _write_parquet,
    _to_spatial_item,
)


class CogniteGeospatialClient:
    """
    The client to access geospatial services

    Args:
        api_key (str): API key. Defaults to the api key set in the environment variable COGNITE_API_KEY
        project (str): Project. Defaults to project set in the environment variable COGNITE_PROJECT
        base_url (str): Base url to send requests to. Defaults to "https://api.cognitedata.com"
        port (int): the port of the server to user. Defaults to 443
        timeout (int): Timeout on requests sent to the api. Defaults to 600 seconds.
        api_token (str): A jwt to use for authentication.
        token_url (str): Optional url to use for token generation.
            This is only used if both api-key and token are not set.
        token_client_id (str): Optional client id to use for token generation.
            This is only used if both api-key and token are not set.
        token_client_secret (str): Optional client secret to use for token generation.
            This is only used if both api-key and token are not set.
        token_scopes (str): Optional list of scopes to use for token generation.
            This is only used if both api-key and token are not set.
        token_custom_args (Dict): Optional additional arguments to use for token generation.
            This will be passed in as optional additional kwargs to OAuth2Session fetch_token and will only be used
            if both api-key and token are not set.
    """

    def __init__(
        self,
        api_key: str = None,
        base_url: str = None,
        port: int = None,
        api_token: Optional[str] = None,
        token_url: Optional[str] = None,
        token_client_id: Optional[str] = None,
        token_client_secret: Optional[str] = None,
        token_scopes: Optional[List[str]] = None,
        token_custom_args: Optional[Dict[str, str]] = None,
        project: str = None,
        timeout: int = 600,  # seconds
    ):
        # configure env
        api_key = api_key or os.getenv("COGNITE_API_KEY")
        self.configuration = Configuration()
        self.configuration.client_side_validation = False
        self.configuration.access_token = api_token
        token_generator = None
        if api_token is not None:
            self.configuration.access_token = api_token
        elif api_key is not None:
            self.configuration.api_key["api-key"] = api_key.strip()
        else:
            token_generator = TokenGenerator(
                token_url=token_url,
                client_id=token_client_id,
                client_secret=token_client_secret,
                scopes=token_scopes,
                custom_args=token_custom_args or {},
            )
            if token_generator.token_params_set():
                api_token = token_generator.return_access_token()
                self.configuration.access_token = api_token

            if api_token is None:
                raise ValueError("No API key or token or token generation arguments have been specified")

        base_url = base_url or "api.cognitedata.com"
        base_url = base_url.strip("/")
        port = port or 443

        if not base_url.startswith("http://") and not base_url.startswith("https://"):
            if port == 443:
                base_url = "https://" + base_url
            else:
                base_url = "http://" + base_url

        self.configuration.host = base_url + ":" + str(port)

        self.project = project or os.getenv("COGNITE_PROJECT")
        if self.project is None:
            raise ValueError("Project must be provided")

        api_client = RetryApiClient(self.configuration, token_generator=token_generator, retry_for_statuses=[401])
        api_client.user_agent = "Cognite-Geospatial-SDK_" + geospatial.__version__ + "/python"
        self.api = SpatialApi(api_client)
        self.timeout = timeout
        self.ingestion_timeout = 21600

    @api_exception_handler
    def parquet_file_save(self, file, id: int = -1, external_id: str = ""):
        return self.api.file_save(
            self.project,
            file_type="parquet",
            file=file,
            id=id,
            external_id=external_id,
            _request_timeout=self.ingestion_timeout,
        )

    def add_spatial_item_data(self, id: int, name: str, value, attribute_type: str):
        value_buff = None
        if not _is_primitive(value):
            if attribute_type == "int":
                value_buff = value.astype(">i4").tobytes()
            elif attribute_type == "long":
                value_buff = value.astype(">i8").tobytes()
            elif attribute_type == "float":
                value_buff = value.astype(">f4").tobytes()
            elif attribute_type == "double":
                value_buff = value.astype(">f8").tobytes()
            elif attribute_type == "string":
                value_buff = bytearray(value, encoding="utf-8")
            elif attribute_type == "boolean":
                end_value = np.append(value.astype(np.uint8), 1)
                pack_int = np.packbits(end_value, bitorder="little")  # uint8
                value_buff = pack_int.tobytes()

        if value_buff is not None:
            value_data = str(base64.urlsafe_b64encode(value_buff), "utf-8")
        else:
            value_data = value

        spatial_data = ItemAttributesDTO(
            items=[
                ItemAttributeDTO(
                    item_id=EitherIdDTO(id=id, local_vars_configuration=self.configuration), name=name, value=value_data
                )
            ]
        )
        response = api_exception_handler(self.api.add_spatial_item_attributes)(
            self.project, spatial_data, _request_timeout=self.timeout
        )
        return _get_response_items(response)

    def store_spatial_item_data(self, id: int, name: str, value, attribute_type: str):
        if (
            type(value) is dict
            or np.isscalar(value)
            or value.size <= 100
            or attribute_type == "string"
            or attribute_type == "boolean"
        ):
            self.add_spatial_item_data(id, name, value, attribute_type)
        else:
            pa_type = None
            if attribute_type == "int":
                pa_type = pa.int32()
            elif attribute_type == "long":
                pa_type = pa.int64()
            elif attribute_type == "float":
                pa_type = pa.float32()
            elif attribute_type == "double":
                pa_type = pa.float64()
            with tempfile.NamedTemporaryFile() as fp:
                _write_parquet(fp.name, name, value, pa_type)
                self.parquet_file_save(file=fp.name, id=id)

    def _store_attribute(self, spatial_item: SpatialItem, attribute_name: str, value: list):
        layer = spatial_item._layer_info
        attribute = None
        for attr in layer.attributes:
            if attr.name == attribute_name:
                attribute = attr
                break
        if attribute is None:
            raise GeospatialError("Attribute not found")
        elif not attribute.is_array:
            raise GeospatialError("Only array attributes can be stored")

        self.store_spatial_item_data(spatial_item.id, attribute_name, value, attribute.type)

        if attribute.type == AttributeTypeDTO.DOUBLE:
            spatial_item._add_double(attribute_name, value)
        elif attribute.type == AttributeTypeDTO.INT:
            spatial_item._add_integer(attribute_name, value)
        elif attribute.type == AttributeTypeDTO.LONG:
            spatial_item._add_long(attribute_name, value)
        elif attribute.type == AttributeTypeDTO.BOOLEAN:
            spatial_item._add_boolean(attribute_name, value)

    @api_exception_handler
    def get_spatial_info(self, id: int = None, external_id: str = None) -> Optional[SpatialItem]:
        """Retrieves spatial item information by internal ids or external ids.

        Args:
            id (int): the id of the spatial object
            external_id (str): the external_id reference of the spatial object

        Returns:
            SpatialItem: A spatial object
        """
        spatial_by_ids = _create_spatial_ids(id, external_id)
        response = self.api.by_ids_spatial_items(self.project, spatial_by_ids, _request_timeout=self.timeout)
        return _to_spatial_items(self, response, True)

    @api_exception_handler
    def create_spatial(self, items: Union[SpatialItem, List[SpatialItem]]) -> Union[SpatialItem, List[SpatialItem]]:
        """`Create one or more spatial items with additional attributes.`

        Args:
            item (Union[SpatialItem, List[SpatialItem]]): SpatialItem or list of spatial items.
        Returns:
            Union[SpatialItem, List[SpatialItem]]: The created spatial items(s).
        """
        (items, single_item) = _to_array(items)
        if len(items) == 0:
            return []
        spatial_items = [_to_core_geometry_spatial_item(item) for item in items]

        create_spatial_items = CreateSpatialItemsDTO(items=spatial_items)
        response = self.api.create_spatial(self.project, create_spatial_items, _request_timeout=self.timeout)

        stored_items = _to_spatial_items(self, response, False)
        layer_map = {}

        for spatial_item, create_item in zip(stored_items, items):
            attributes = _filter_list_attributes(create_item.attributes)
            if len(attributes) > 0:
                spatial_item._layer_info = self._load_layer(spatial_item.layer, layer_map)
                for name, value in attributes.items():
                    self._store_attribute(spatial_item, name, value)

        return _single_or_array(stored_items, single_item)

    def _load_layer(self, layer_name: str, layer_cache: dict):
        layer = layer_cache.get(layer_name)
        if layer is None:
            layer = self.list_layers(layer_name)
            layer_cache[layer_name] = layer
        return layer

    @api_exception_handler
    def create_update_spatial(self, items: Union[SpatialItem, List[SpatialItem]]) -> Optional[SpatialItem]:
        """`Create or update one or more spatial items with additional attributes.`

        Args:
            item (Union[SpatialItem, List[SpatialItem]]): SpatialItem or list of spatial items.
        Returns:
            Union[SpatialItem, List[SpatialItem]]: The created or updated spatial items(s).
        """
        (items, single_item) = _to_array(items)
        if len(items) == 0:
            return []

        items_ids = [
            _create_spatial_id(item.id, item.external_id)
            for item in items
            if item.id is not None or item.external_id is not None
        ]

        existing_items_ids = set()
        existing_items_external_ids = set()
        if len(items_ids) > 0:
            response = self.api.by_ids_spatial_items(
                self.project, SpatialIdsDTO(items=items_ids), _request_timeout=self.timeout
            )
            existing_items = _to_spatial_items(self, response, single=False)
            for item in existing_items:
                existing_items_ids.add(item.id)
                if item.external_id is not None:
                    existing_items_external_ids.add(item.external_id)

        items_to_create = []
        items_to_update = []

        if len(existing_items_ids) == 0:
            items_to_create = items
        else:
            for item in items:
                if (item.id in existing_items_ids) or (item.external_id in existing_items_external_ids):
                    items_to_update.append(item)
                else:
                    items_to_create.append(item)

        created_items = self.create_spatial(items_to_create)
        updated_items = self.update_spatial(items_to_update)

        # return in the same order
        created_updated_items = created_items + updated_items
        created_updated_id_map = {item.id: item for item in created_updated_items}
        created_updated_external_map = {
            item.external_id: item for item in created_updated_items if item.external_id is not None
        }

        result_items = []
        for item in items:
            if item.id in created_updated_id_map:
                result_items.append(created_updated_id_map[item.id])
            elif item.external_id in created_updated_external_map:
                result_items.append(created_updated_external_map[item.external_id])

        return _single_or_array(result_items, single_item)

    @api_exception_handler
    def delete_spatial(self, id: int = None, external_id: str = None) -> Optional[SpatialItem]:
        """Delete spatial item by internal ids or external ids.

        Args:
            id (int): the id of the spatial object
            external_id (str): the external_id reference of the spatial object

        Returns:
            SpatialItem: spatial object
        """
        spatial_delete_ids = _create_spatial_ids(id, external_id)
        response = self.api.delete_spatial(self.project, spatial_delete_ids, _request_timeout=self.timeout)
        return _to_spatial_items(self, response, True)

    @api_exception_handler
    def get_coverage(
        self,
        output_crs: str,
        id: int = None,
        external_id: str = None,
        dimensional_space: str = "2d",
        geometry_format: str = None,
    ):
        """Retrieve the coverage of the spatial object by internal ids or external ids.

        Args:
            id (int): the id of the spatial object
            external_id (str): the external_id reference of the spatial object
            dimensional_space (str): The spatial dimension of the coverage. Valid values are "2d", "3d"
            output_crs (str): the crs of the output coverage
            geometry_format (str): Geometry format wkt or geojson

        Returns:
            SpatialItemCoverageDTO: spatial object's data
        """
        dimensional_space = dimensional_space.lower()
        if dimensional_space not in ["2d", "3d"]:
            raise GeospatialError("dimensional_space - must be 2d or 3d only")

        item_id = _create_spatial_id(id, external_id)
        spatial_coverage_request = SpatialCoverageRequestDTO(
            items=[item_id],
            dimensional_space=dimensional_space,
            output_crs=output_crs,
            local_vars_configuration=self.configuration,
        )
        response = api_exception_handler(self.api.get_spatial_coverage)(
            self.project, spatial_coverage_request, geometry=geometry_format, _request_timeout=self.timeout
        )
        return _first_item(response)

    @api_exception_handler
    def interpret(self, id: int = None, external_id: str = None):
        """Interpret attributes from spatial item by internal id or external id.

        Args:
            id (int): the id of the spatial object
            external_id (str): the external_id reference of the spatial object
        """
        spatial_by_ids = _create_spatial_ids(id, external_id)
        return self.api.interpret(self.project, spatial_by_ids, _request_timeout=self.ingestion_timeout)

    def get_spatial(
        self, id: int = None, external_id: str = None, extractors: List[DataExtractor] = None
    ) -> Optional[SpatialItem]:
        """Retrieves spatial item data by internal ids or external ids.

        Args:
            id (int): the id of the spatial object
            external_id (str): the external_id reference of the spatial object
            extractors (List[DataExtractor]): a list of extractors. Each extractor will be applied to a specific
                attribute so that we don't get entire data for that attribute, but only the part we are interested in

        Returns:
            SpatialItem: spatial object's data
        """
        spatial_item = self.get_spatial_info(id=id, external_id=external_id)
        if spatial_item is None:
            return None

        layer = self.list_layers(spatial_item.layer)
        if layer is not None:
            spatial_item._set_layer_info(layer)

            attribute_types = {
                attribute.name: attribute
                for attribute in layer.attributes
                if attribute.name not in spatial_item.attributes
            }
            attribute_data = self._get_attributes(
                item_id=spatial_item, attributes=list(attribute_types.keys()), extractors=extractors
            )
            for name, data in attribute_data.items():
                if not attribute_types[name].is_array:
                    spatial_item._add_text(name, data)
                elif attribute_types[name].type == AttributeTypeDTO.DOUBLE:
                    spatial_item._add_double(name, data)
                elif attribute_types[name].type == AttributeTypeDTO.INT:
                    spatial_item._add_integer(name, data)
                elif attribute_types[name].type == AttributeTypeDTO.BOOLEAN:
                    spatial_item._add_boolean(name, data)

        return spatial_item

    @api_exception_handler
    def _get_attributes(self, item_id: SpatialItemId, attributes: List[str], extractors: List[DataExtractor] = None):
        if isinstance(item_id, SpatialItem):
            spatial_item = item_id
        else:
            spatial_item = self.get_spatial_info(item_id.id, item_id.external_id)

        request_attributes = [attribute for attribute in attributes if attribute not in spatial_item.attributes]
        result = {name: value for name, value in spatial_item.attributes.items() if name in attributes}

        if len(result) == len(attributes):
            return result

        layer_name = spatial_item.layer
        layer = self.list_layers(layer_name)
        if layer is None:
            raise GeospatialError("layer does not exist")

        extractors_dto = (
            [DataExtractorDTO(e.attribute, e.min_val, e.max_val) for e in extractors]
            if extractors is not None
            else None
        )

        data_request = SpatialDataRequestDTO(
            spatial_id=InternalIdDTO(id=spatial_item.id), attributes=request_attributes, extractors=extractors_dto
        )
        response = self.api.get_spatial_item_attributes(
            self.project, spatial_data_request_dto=data_request, _request_timeout=self.timeout
        )
        layer_types = {la.name: la.type for la in layer.attributes}
        for attribute, value in response.items():
            result[attribute] = _decode_attribute(value, layer_types[attribute])
        return result

    @api_exception_handler
    def list_layers(self, names: Union[str, List[str]] = None) -> Union[Layer, List[Layer]]:
        """List all available layers.

        Args:
            names (List[str]): list of layer's names to retrieve. Use None to list all available layers.

        Returns:
            list[Layer]: list of layers
        """
        if names is None:
            names = []
        (names, single_name) = _to_array(names)

        layer_filter = FeatureLayersFilterDTO(names=names)
        response = self.api.find_feature_layer(self.project, layer_filter, _request_timeout=self.timeout)
        items = _get_response_items(response)
        layers = [Layer(client=self, layer=layer) for layer in items]

        return _single_or_array(layers, single_name)

    def find_spatial(
        self,
        layer: str,
        spatial_relationship: SpatialRelationship = None,
        geometry: Geometry = None,
        distance: float = None,
        name: str = None,
        asset_ids: List[int] = None,
        attributes: List[str] = None,
        metadata: Dict[str, str] = None,
        source: str = None,
        external_id_prefix: str = None,
        output_crs: str = None,
        limit: int = 10,
        offset: int = 0,
        geometry_format: str = None,
    ) -> SpatialList:
        """Search the spatial objects based on metadata or spatial relationships.

        Args:
            layer (str): the layer to which objects belong
            spatial_relationship (SpatialRelationship): the spatial relationship between looking objects and the input geometry
            geometry (Geometry): the input geometry
            distance (float): the distance to the input geometry when spatial_relationship is within distance.
            name (str): the name of returned objects
            asset_ids (List[int]): the list of asset ids which spatial objects must link to
            attributes (List[str]): the list of attribute names are returned together with spatial objects
            metadata (dict): a set of metadata pairs which spatial objects must have
            source (str): the source of spatial objects
            external_id_prefix (str): the prefix of external_id reference which spatial objects must have
            output_crs (str): the crs of the output geometry attribute in case `geometry` attributes are queried
            limit (int): number of objects to be returned
            offset (int): the starting offset of objects in the results
            geometry_format (str): the output format of the geometry if any. Valid values: wkt, geojson. Default to wkt
        Returns:
            SpatialList: spatial object's data

        Example:
                >>> # search within the geometry of another spatial item
                >>> client.find_spatial(layer="polygon", spatial_relationship=SpatialRelationship.within,
                ...        geometry=Geometry(external_id="external_id"),
                ...    )
                >>> # search within a specific area defined by user
                >>> items = client.find_spatial(
                ...     layer="polygon",
                ...     spatial_relationship=SpatialRelationship.within,
                ...     geometry=Geometry(
                ...         wkt="POLYGON ((289999 5999999, 290006 5999999, 290006 6000006, 289999 6000006, 289999 5999999))",
                ...         crs="epsg:23031",
                ...         ),
                ...     )

        """

        def _create_geometry(geometry: Geometry):
            wkt = None
            geojson = None
            if geometry.id is not None:
                _check_id(geometry.id)
            elif geometry.external_id is not None:
                _check_external_id(geometry.external_id)
            elif geometry.wkt is not None:
                wkt = geometry.wkt
                if geometry.crs is None:
                    raise ValueError("crs must be provided")
            elif geometry.geojson is not None:
                geojson = geometry.geojson
                if geometry.crs is None:
                    raise ValueError("crs must be provided")
            else:
                raise ValueError("geometry is not defined")

            return GeometryDTO(
                id=geometry.id,
                external_id=geometry.external_id,
                wkt=wkt,
                geojson=geojson,
                crs=geometry.crs,
                local_vars_configuration=self.configuration,
            )

        spatial_filter = None
        if spatial_relationship is not None:
            geometry = _create_geometry(geometry)
            spatial_relationship = SpatialRelationshipDTO(
                name=spatial_relationship.value, distance=distance, local_vars_configuration=self.configuration
            )
            spatial_filter = SpatialFilterObject(
                spatial_relationship, geometry, local_vars_configuration=self.configuration
            )

        spatial_search_request = SpatialSearchRequestDTO(
            name=name,
            asset_ids=asset_ids,
            metadata=metadata,
            source=source,
            external_id_prefix=external_id_prefix,
            spatial_filter=spatial_filter,
            layer=layer,
            attributes=attributes,
            output_crs=output_crs,
        )

        if limit is None or limit == -1 or limit == float("inf") or limit > 100:
            _offset = 0
            _limit = 100
            total = float("inf") if (limit is None or limit == -1 or limit == float("inf")) else limit
            spatial_list = SpatialList(client=self, layer_name=layer)
            while True:
                if total - _offset < _limit:
                    _limit = total - _offset

                spatial_search_request.offset = _offset
                spatial_search_request.limit = _limit
                response = api_exception_handler(self.api.search_spatial)(
                    self.project,
                    spatial_search_request_dto=spatial_search_request,
                    _request_timeout=self.timeout,
                    geometry=geometry_format,
                )

                items = _get_response_items(response)
                spatial_list.extend(list(map(lambda x: _to_spatial_item(self, x), items)))
                _offset += _limit
                response_size = len(response.items)
                if response_size != _limit or _offset == total:
                    break
            return spatial_list
        else:
            spatial_search_request.offset = offset
            spatial_search_request.limit = limit
            response = api_exception_handler(self.api.search_spatial)(
                self.project,
                spatial_search_request_dto=spatial_search_request,
                _request_timeout=self.timeout,
                geometry=geometry_format,
            )

            return _to_spatial_items(self, response, False, layer_name=layer)

    @api_exception_handler
    def shape_file_save(
        self,
        file,
        layer: str,
        create_layer: bool = False,
        cleanup_old_data: bool = False,
        id_field: str = None,
        attributes: List[str] = None,
    ):
        """Extract spatial items from shapefile and save it into geospatial.

        Args:
            file (str): file location on local drive
            layer (str): the layer name to save
            create_layer (bool): create layer if not exists
            cleanup_old_data (bool): Default false, clean up all data in the existing layer before ingesting data from shape file
            id_field (str): The field contains the unique ID of the row. The externalId will be created as <layer_name>_<id>
            attributes (Optional[List[str]]): attributes to save (if None save all attributes)
        """
        params = {
            "file_type": "shp",
            "file": file,
            "layer": layer,
            "create_layer": create_layer,
            "cleanup_old_data": cleanup_old_data,
            "_request_timeout": self.ingestion_timeout,
        }
        if attributes is not None:
            params["attributes"] = ",".join(attributes)
        if id_field is not None:
            params["id_field"] = id_field
        return self.api.file_save(self.project, **params)

    @api_exception_handler
    def get_grid_coverage(
        self, geometry: TextBasedGeometry, id: int = None, external_id: str = None, distance: float = None
    ) -> GridCoverage:
        """Given a geometry and a seismic volume (identified by id or external_id), return a list of inlines and xlines of
        the volume covered by the geometry extent (by distance unit, default to geometry itself if distance is not specified).

        Args:
            id (int): the id of the spatial object (seismic volume)
            external_id (str): the external_id reference of the spatial object (seismic volume)
            geometry (TextBasedGeometry): the input geometry
            distance (float): the distance to extend the input geometry
        Returns:
            GridCoverage: a map from each line (inline) to a list of cross points (xlines)
        """
        spatial_id = _create_spatial_id(id=id, external_id=external_id)
        geom = TextBasedGeometryDTO(
            geojson=geometry.geojson, crs=geometry.crs, wkt=geometry.wkt, local_vars_configuration=self.configuration
        )
        grid_coverage_request = GridCoverageRequestDTO(spatial_id=spatial_id, geometry=geom, distance=distance)
        response = self.api.grid_coverage(self.project, grid_coverage_request, _request_timeout=self.ingestion_timeout)
        return GridCoverage({item.linenumber: item.list for item in response.rows})

    @api_exception_handler
    def update_spatial(
        self, items: Union[UpdateSpatialItem, List[UpdateSpatialItem]]
    ) -> Union[SpatialItem, List[SpatialItem]]:
        """ Update spatial object(s) with given id or external_id

        Args:
            item (Union[UpdateSpatialItem, List[UpdateSpatialItem]]): SpatialItem or list of spatial items.
        Returns:
            Union[SpatialItem, List[SpatialItem]]: The updated spatial object
        """
        (items, single_item) = _to_array(items)
        if len(items) == 0:
            return []

        update_items = [_to_update_spatial_item(item) for item in items]
        update_spatial_items = UpdateSpatialItemsDTO(items=update_items)
        response = self.api.update_spatial(self.project, update_spatial_items, _request_timeout=self.timeout)
        updated_items = _to_spatial_items(self, response, False)

        layer_map = {}
        for spatial_item, create_item in zip(updated_items, items):
            attributes = _filter_list_attributes(create_item.attributes)
            if len(attributes) > 0:
                spatial_item._layer_info = self._load_layer(spatial_item.layer, layer_map)
                for name, value in attributes.items():
                    self._store_attribute(spatial_item, name, value)

        return _single_or_array(updated_items, single_item)

    @api_exception_handler
    def get_intersections(
        self, geometry: Geometry, geometries: List[Geometry], output_crs, geometry_format: str = None
    ) -> List[BaseGeometry]:
        """ Find intersection between an array of geometries and another geometry

        Args:
            geometry (Geometry): a single geometry
            geometries (List[Geometry]): an array of geometries
            output_crs (str): the crs of intersection geometries
            geometry_format (str): the output format of the geometry if any. Valid values: wkt, geojson. Default to wkt
        Returns:
            List[BaseGeometry]: a list of intersections, each is a shapely geometry

        Example:
                >>> intersections = client.get_intersections(
                ...         output_crs="epsg:4326",
                ...         geometry=Geometry(external_id="external_id_1"),
                ...         geometries=[
                ...             Geometry(external_id="external_id_2"),
                ...             Geometry(external_id="external_id_3"),
                ...             Geometry(external_id="external_id_4"),
                ...         ],
                ...     )

        """

        geometry_dto = _create_spatial_id(id=geometry.id, external_id=geometry.external_id)
        geometries_dto = [_create_spatial_id(id=geom.id, external_id=geom.external_id) for geom in geometries]
        intersection_query_dto = IntersectionQueryDTO(
            geometry=geometry_dto, geometries=geometries_dto, output_crs=output_crs
        )
        response = self.api.find_intersection(
            self.project, intersection_query_dto, geometry=geometry_format, _request_timeout=self.timeout
        )
        if response is None:
            return None
        return [
            shape(geometry.intersection) if geometry_format == "geojson" else wkt.loads(geometry.intersection)
            for geometry in response.geometries
        ]

    def persist_spatial_attribute(self, id: int, external_id: str, name: str, value) -> None:
        """Persist spatial attribute of the specified item into data store. The data must follow the  format specified
        in the layer of the item

        Args:
            id (int): the id of the spatial object
            external_id (str): the external_id reference of the spatial object
            name (str): the name of the attribute
            value: the value of the attribute
        """

        def _persis_data(id: int, external_id: str, name: str, value):
            spatial_item = self.get_spatial_info(id, external_id)
            layer_name = spatial_item.layer
            layer = self.list_layers(layer_name)
            attributes = layer.attributes
            attribute = next((attribute for attribute in attributes if attribute.name == name), None)
            if attribute is None:
                raise GeospatialError("Attribute is not defined in the layer")
            self.store_spatial_item_data(spatial_item.id, name, value, attribute.type)

        return _persis_data(id, external_id, name, value)

    def get_attributes(
        self, attributes: List[str], id: int = None, external_id: str = None, extractors: List[DataExtractor] = None
    ) -> Dict[str, object]:
        """ Get spatial object's attributes

        Args:
            id (int): the id of the spatial object
            external_id (str): the external_id reference of the spatial object
            attributes (List[str]): a list of attribute names to get
            extractors (List[DataExtractor]): a list of extractors. Each extractor will be applied to a specific
                attribute so that we don't get entire data for that attribute, but only the part we are interested in

        Returns:
            Dict[str, object]: a dict of attribute's name and its value
        """

        item_id = SpatialItemId(id=id, external_id=external_id)
        return self._get_attributes(item_id, attributes, extractors)

    @lru_cache(maxsize=128)
    def get_layer(self, name: str) -> Layer:
        """Get layer by name.

        Args:
            name (str): name of the layer

        Returns:
            Layer: layer information
        """
        if name is None:
            raise GeospatialError(message="Layer name required")
        return self.list_layers(name)

    def within(
        self,
        layer: str,
        geometry: Geometry,
        name: str = None,
        asset_ids: List[int] = None,
        attributes: List[str] = None,
        metadata: Dict[str, str] = None,
        source: str = None,
        external_id_prefix: str = None,
        output_crs: str = None,
        limit: int = 10,
        offset: int = 0,
        geometry_format: str = None,
    ) -> SpatialList:
        """Search the spatial objects within 2D geometry.

        Args:
            layer (str): the layer to which objects belong
            geometry (Geometry): the input geometry
            name (str): the name of returned objects
            asset_ids (List[int]): the list of asset ids which spatial objects must link to
            attributes (List[str]): the list of attribute names are returned together with spatial objects
            metadata (dict): a set of metadata pairs which spatial objects must have
            source (str): the source of spatial objects
            external_id_prefix (str): the prefix of external_id reference which spatial objects must have
            output_crs (str): the crs of the output geometry attribute in case `geometry` attributes are queried
            limit (int): number of objects to be returned. Defaults to 10. For values None, -1 or float(“inf”) search is unlimited.
            offset (int): the starting offset of objects in the results
            geometry_format (str): the output format of the geometry if any. Valid values: wkt, geojson. Default to wkt
        Returns:
            SpatialList: spatial object's data

        Example:
                >>> # search within the geometry of another spatial item
                >>> client.within(layer="polygon",
                ...        geometry=Geometry(external_id="external_id"),
                ...    )
                >>> # search within a specific area defined by user
                >>> items = client.within(
                ...     layer="polygon",
                ...     geometry=Geometry(
                ...         wkt="POLYGON ((289999 5999999, 290006 5999999, 290006 6000006, 289999 6000006, 289999 5999999))",
                ...         crs="epsg:23031",
                ...         ),
                ...     )

        """
        return self.find_spatial(
            layer,
            SpatialRelationship.within,
            geometry,
            None,
            name,
            asset_ids,
            attributes,
            metadata,
            source,
            external_id_prefix,
            output_crs,
            limit,
            offset,
            geometry_format,
        )

    def within_distance(
        self,
        layer: str,
        geometry: Geometry,
        distance: float,
        name: str = None,
        asset_ids: List[int] = None,
        attributes: List[str] = None,
        metadata: Dict[str, str] = None,
        source: str = None,
        external_id_prefix: str = None,
        output_crs: str = None,
        limit: int = 10,
        offset: int = 0,
        geometry_format: str = None,
    ) -> SpatialList:
        """Search the spatial objects within distance 2D geometry.

        Args:
            layer (str): the layer to which objects belong
            geometry (Geometry): the input geometry
            distance (float): the distance to the input geometry when spatial_relationship is within distance
            name (str): the name of returned objects
            asset_ids (List[int]): the list of asset ids which spatial objects must link to
            attributes (List[str]): the list of attribute names are returned together with spatial objects
            metadata (dict): a set of metadata pairs which spatial objects must have
            source (str): the source of spatial objects
            external_id_prefix (str): the prefix of external_id reference which spatial objects must have
            output_crs (str): the crs of the output geometry attribute in case `geometry` attributes are queried
            limit (int): number of objects to be returned
            offset (int): the starting offset of objects in the results
            geometry_format (str): the output format of the geometry if any. Valid values: wkt, geojson. Default to wkt
        Returns:
            SpatialList: spatial object's data

        Example:
                >>> # search within the geometry of another spatial item
                >>> client.within_distance(layer="polygon",
                ...        geometry=Geometry(external_id="external_id"),
                ...        distance=10,
                ...    )
                >>> # search within a specific area defined by user
                >>> items = client.within_distance(
                ...     layer="polygon",
                ...     geometry=Geometry(
                ...         wkt="POLYGON ((289999 5999999, 290006 5999999, 290006 6000006, 289999 6000006, 289999 5999999))",
                ...         crs="epsg:23031",
                ...         ),
                ...     distance=10,
                ...     )

        """
        return self.find_spatial(
            layer,
            SpatialRelationship.within_distance,
            geometry,
            distance,
            name,
            asset_ids,
            attributes,
            metadata,
            source,
            external_id_prefix,
            output_crs,
            limit,
            offset,
            geometry_format,
        )

    def within_completely(
        self,
        layer: str,
        geometry: Geometry,
        name: str = None,
        asset_ids: List[int] = None,
        attributes: List[str] = None,
        metadata: Dict[str, str] = None,
        source: str = None,
        external_id_prefix: str = None,
        output_crs: str = None,
        limit: int = 10,
        offset: int = 0,
        geometry_format: str = None,
    ) -> SpatialList:
        """Search the spatial objects within distance 2D geometry.

        Args:
            layer (str): the layer to which objects belong
            geometry (Geometry): the input geometry
            name (str): the name of returned objects
            asset_ids (List[int]): the list of asset ids which spatial objects must link to
            attributes (List[str]): the list of attribute names are returned together with spatial objects
            metadata (dict): a set of metadata pairs which spatial objects must have
            source (str): the source of spatial objects
            external_id_prefix (str): the prefix of external_id reference which spatial objects must have
            output_crs (str): the crs of the output geometry attribute in case `geometry` attributes are queried
            limit (int): number of objects to be returned
            offset (int): the starting offset of objects in the results
            geometry_format (str): the output format of the geometry if any. Valid values: wkt, geojson. Default to wkt
        Returns:
            SpatialList: spatial object's data

        Example:
                >>> # search within the geometry of another spatial item
                >>> client.within_completely(layer="polygon",
                ...        geometry=Geometry(external_id="external_id"),
                ...    )
                >>> # search within a specific area defined by user
                >>> items = client.within_completely(
                ...     layer="polygon",
                ...     geometry=Geometry(
                ...         wkt="POLYGON ((289999 5999999, 290006 5999999, 290006 6000006, 289999 6000006, 289999 5999999))",
                ...         crs="epsg:23031",
                ...         ),
                ...     )

        """
        return self.find_spatial(
            layer,
            SpatialRelationship.within_completely,
            geometry,
            None,
            name,
            asset_ids,
            attributes,
            metadata,
            source,
            external_id_prefix,
            output_crs,
            limit,
            offset,
            geometry_format,
        )

    def intersect(
        self,
        layer: str,
        geometry: Geometry,
        name: str = None,
        asset_ids: List[int] = None,
        attributes: List[str] = None,
        metadata: Dict[str, str] = None,
        source: str = None,
        external_id_prefix: str = None,
        output_crs: str = None,
        limit: int = 10,
        offset: int = 0,
        geometry_format: str = None,
    ) -> SpatialList:
        """Search the spatial objects intersect 2D geometry.

        Args:
            layer (str): the layer to which objects belong
            geometry (Geometry): the input geometry
            name (str): the name of returned objects
            asset_ids (List[int]): the list of asset ids which spatial objects must link to
            attributes (List[str]): the list of attribute names are returned together with spatial objects
            metadata (dict): a set of metadata pairs which spatial objects must have
            source (str): the source of spatial objects
            external_id_prefix (str): the prefix of external_id reference which spatial objects must have
            output_crs (str): the crs of the output geometry attribute in case `geometry` attributes are queried
            limit (int): number of objects to be returned
            offset (int): the starting offset of objects in the results
            geometry_format (str): the output format of the geometry if any. Valid values: wkt, geojson. Default to wkt
        Returns:
            SpatialList: spatial object's data

        Example:
                >>> # search within the geometry of another spatial item
                >>> client.intersect(layer="polygon",
                ...        geometry=Geometry(external_id="external_id"),
                ...    )
                >>> # search within a specific area defined by user
                >>> items = client.intersect(
                ...     layer="polygon",
                ...     geometry=Geometry(
                ...         wkt="POLYGON ((289999 5999999, 290006 5999999, 290006 6000006, 289999 6000006, 289999 5999999))",
                ...         crs="epsg:23031",
                ...         ),
                ...     )

        """
        return self.find_spatial(
            layer,
            SpatialRelationship.intersect,
            geometry,
            None,
            name,
            asset_ids,
            attributes,
            metadata,
            source,
            external_id_prefix,
            output_crs,
            limit,
            offset,
            geometry_format,
        )

    def within_3d(
        self,
        layer: str,
        geometry: Geometry,
        name: str = None,
        asset_ids: List[int] = None,
        attributes: List[str] = None,
        metadata: Dict[str, str] = None,
        source: str = None,
        external_id_prefix: str = None,
        output_crs: str = None,
        limit: int = 10,
        offset: int = 0,
        geometry_format: str = None,
    ) -> SpatialList:
        """Search the spatial objects within 3D geometry.

        Args:
            layer (str): the layer to which objects belong
            geometry (Geometry): the input geometry
            name (str): the name of returned objects
            asset_ids (List[int]): the list of asset ids which spatial objects must link to
            attributes (List[str]): the list of attribute names are returned together with spatial objects
            metadata (dict): a set of metadata pairs which spatial objects must have
            source (str): the source of spatial objects
            external_id_prefix (str): the prefix of external_id reference which spatial objects must have
            output_crs (str): the crs of the output geometry attribute in case `geometry` attributes are queried
            limit (int): number of objects to be returned
            offset (int): the starting offset of objects in the results
            geometry_format (str): the output format of the geometry if any. Valid values: wkt, geojson. Default to wkt
        Returns:
            SpatialList: spatial object's data

        Example:
                >>> # search within the geometry of another spatial item
                >>> client.within_3d(layer="polygon",
                ...        geometry=Geometry(external_id="external_id"),
                ...    )
                >>> # search within a specific area defined by user
                >>> items = client.within_3d(
                ...     layer="polygon",
                ...     geometry=Geometry(
                ...         wkt="POLYGON ((289999 5999999, 290006 5999999, 290006 6000006, 289999 6000006, 289999 5999999))",
                ...         crs="epsg:23031",
                ...         ),
                ...     )

        """
        return self.find_spatial(
            layer,
            SpatialRelationship.within_3d,
            geometry,
            None,
            name,
            asset_ids,
            attributes,
            metadata,
            source,
            external_id_prefix,
            output_crs,
            limit,
            offset,
            geometry_format,
        )

    def within_distance_3d(
        self,
        layer: str,
        geometry: Geometry,
        distance: float,
        name: str = None,
        asset_ids: List[int] = None,
        attributes: List[str] = None,
        metadata: Dict[str, str] = None,
        source: str = None,
        external_id_prefix: str = None,
        output_crs: str = None,
        limit: int = 10,
        offset: int = 0,
        geometry_format: str = None,
    ) -> SpatialList:
        """Search the spatial objects within distance 3D geometry.

        Args:
            layer (str): the layer to which objects belong
            geometry (Geometry): the input geometry
            distance (float): the distance to the input geometry when spatial_relationship is within distance.
            name (str): the name of returned objects
            asset_ids (List[int]): the list of asset ids which spatial objects must link to
            attributes (List[str]): the list of attribute names are returned together with spatial objects
            metadata (dict): a set of metadata pairs which spatial objects must have
            source (str): the source of spatial objects
            external_id_prefix (str): the prefix of external_id reference which spatial objects must have
            output_crs (str): the crs of the output geometry attribute in case `geometry` attributes are queried
            limit (int): number of objects to be returned
            offset (int): the starting offset of objects in the results
            geometry_format (str): the output format of the geometry if any. Valid values: wkt, geojson. Default to wkt
        Returns:
            SpatialList: spatial object's data

        Example:
                >>> # search within the geometry of another spatial item
                >>> client.within_distance_3d(layer="polygon",
                ...        geometry=Geometry(external_id="external_id"),
                ...    )
                >>> # search within a specific area defined by user
                >>> items = client.within_distance_3d(
                ...     layer="polygon",
                ...     geometry=Geometry(
                ...         wkt="POLYGON ((289999 5999999, 290006 5999999, 290006 6000006, 289999 6000006, 289999 5999999))",
                ...         crs="epsg:23031",
                ...         ),
                ...     )

        """
        return self.find_spatial(
            layer,
            SpatialRelationship.within_distance_3d,
            geometry,
            distance,
            name,
            asset_ids,
            attributes,
            metadata,
            source,
            external_id_prefix,
            output_crs,
            limit,
            offset,
            geometry_format,
        )

    def within_completely_3d(
        self,
        layer: str,
        geometry: Geometry,
        name: str = None,
        asset_ids: List[int] = None,
        attributes: List[str] = None,
        metadata: Dict[str, str] = None,
        source: str = None,
        external_id_prefix: str = None,
        output_crs: str = None,
        limit: int = 10,
        offset: int = 0,
        geometry_format: str = None,
    ) -> SpatialList:
        """Search the spatial objects completely 3D geometry.

        Args:
            layer (str): the layer to which objects belong
            geometry (Geometry): the input geometry
            name (str): the name of returned objects
            asset_ids (List[int]): the list of asset ids which spatial objects must link to
            attributes (List[str]): the list of attribute names are returned together with spatial objects
            metadata (dict): a set of metadata pairs which spatial objects must have
            source (str): the source of spatial objects
            external_id_prefix (str): the prefix of external_id reference which spatial objects must have
            output_crs (str): the crs of the output geometry attribute in case `geometry` attributes are queried
            limit (int): number of objects to be returned
            offset (int): the starting offset of objects in the results
            geometry_format (str): the output format of the geometry if any. Valid values: wkt, geojson. Default to wkt
        Returns:
            SpatialList: spatial object's data

        Example:
                >>> # search within the geometry of another spatial item
                >>> client.within_completely_3d(layer="polygon",
                ...        geometry=Geometry(external_id="external_id"),
                ...    )
                >>> # search within a specific area defined by user
                >>> items = client.within_completely_3d(
                ...     layer="polygon",
                ...     geometry=Geometry(
                ...         wkt="POLYGON ((289999 5999999, 290006 5999999, 290006 6000006, 289999 6000006, 289999 5999999))",
                ...         crs="epsg:23031",
                ...         ),
                ...     )

        """
        return self.find_spatial(
            layer,
            SpatialRelationship.within_completely_3d,
            geometry,
            None,
            name,
            asset_ids,
            attributes,
            metadata,
            source,
            external_id_prefix,
            output_crs,
            limit,
            offset,
            geometry_format,
        )

    def intersect_3d(
        self,
        layer: str,
        geometry: Geometry,
        name: str = None,
        asset_ids: List[int] = None,
        attributes: List[str] = None,
        metadata: Dict[str, str] = None,
        source: str = None,
        external_id_prefix: str = None,
        output_crs: str = None,
        limit: int = 10,
        offset: int = 0,
        geometry_format: str = None,
    ) -> SpatialList:
        """Search the spatial objects inersect 3D geometry.

        Args:
            layer (str): the layer to which objects belong
            geometry (Geometry): the input geometry
            name (str): the name of returned objects
            asset_ids (List[int]): the list of asset ids which spatial objects must link to
            attributes (List[str]): the list of attribute names are returned together with spatial objects
            metadata (dict): a set of metadata pairs which spatial objects must have
            source (str): the source of spatial objects
            external_id_prefix (str): the prefix of external_id reference which spatial objects must have
            output_crs (str): the crs of the output geometry attribute in case `geometry` attributes are queried
            limit (int): number of objects to be returned
            offset (int): the starting offset of objects in the results
            geometry_format (str): the output format of the geometry if any. Valid values: wkt, geojson. Default to wkt
        Returns:
            SpatialList: spatial object's data

        Example:
                >>> # search within the geometry of another spatial item
                >>> client.intersect_3d(layer="polygon",
                ...        geometry=Geometry(external_id="external_id"),
                ...    )
                >>> # search within a specific area defined by user
                >>> items = client.intersect_3d(
                ...     layer="polygon",
                ...     geometry=Geometry(
                ...         wkt="POLYGON ((289999 5999999, 290006 5999999, 290006 6000006, 289999 6000006, 289999 5999999))",
                ...         crs="epsg:23031",
                ...         ),
                ...     )

        """
        return self.find_spatial(
            layer,
            SpatialRelationship.intersect_3d,
            geometry,
            None,
            name,
            asset_ids,
            attributes,
            metadata,
            source,
            external_id_prefix,
            output_crs,
            limit,
            offset,
            geometry_format,
        )

    def get_layer_items(
        self, layer: str, attributes: List[str] = None, output_crs: str = None, geometry_format: str = None
    ) -> List[SpatialItem]:
        """Get all spatial items belong to layer.

        Warning:
            This method will load all spatial items into memory and has a risk to get memory overflow.

        Args:
            layer (str): the layer to which objects belong
            attributes (List[str]): the list of attribute names are returned together with spatial objects
            output_crs (str): the crs of the output geometry attribute in case `geometry` attributes are queried
            geometry_format (str): the geometry format of the output geometries. Valid values: wkt, geojson. Default to wkt

        Returns:
            SpatialList: spatial object list
        """
        spatial_list = SpatialList(client=self, layer_name=layer)
        items = []
        offset = 0
        limit = 100
        while True:
            bucket = self.find_spatial(
                layer=layer,
                attributes=attributes,
                limit=limit,
                offset=offset,
                output_crs=output_crs,
                geometry_format=geometry_format,
            )
            items.extend(bucket)
            offset += limit
            if limit != len(bucket):
                break
        spatial_list.extend(items)
        return spatial_list

    def has_spatial_relationship(
        self, geometry: Geometry, other: Geometry, spatial_relationship: SpatialRelationship, distance: float = None
    ) -> bool:
        """ Test if a spatial relationship exists between two spatial objects

        Args:
            geometry (Geometry): the first geometry
            other (Geometry): the second geoemtry
            spatial_relationship (SpatialRelationship): the spatial relationship between objects to check.
            distance (float): the distance between spatial objects in case of checking "within distance" relationship
        Returns:
            bool: True or False

        """
        geometry_info = self.get_spatial_info(id=geometry.id, external_id=geometry.external_id)
        if geometry_info is None:
            return None

        offset = 0
        limit = 10

        while True:
            items = self.find_spatial(
                layer=geometry_info.layer,
                geometry=other,
                external_id_prefix=geometry_info.external_id,
                spatial_relationship=spatial_relationship,
                distance=distance,
                limit=limit,
                offset=offset,
            )
            for item in items:
                if item.external_id == geometry.external_id or item.id == geometry.id:
                    return True
            if len(items) < limit:
                return False

            offset = offset + limit

    @api_exception_handler
    def union(self, items: List[Geometry], output_crs: str, geometry_format: str = "wkt") -> BaseGeometry:
        """Compute representation of the union of the given 2D geometric objects

        Args:
            items (List[Geometry]): a list of geometries to compute the union
            output_crs (str): the desired crs of the output
            geometry_format (str): the geometry format of the output. Valid values: wkt, geojson. Default to wkt

        Returns:
            BaseGeometry: the union of input geometries
        """

        items_dto = [
            GeometryDTO(
                id=item.id,
                external_id=item.external_id,
                wkt=item.wkt,
                crs=item.crs,
                geojson=item.geojson,
                local_vars_configuration=self.configuration,
            )
            for item in items
        ]
        geometry_items = GeometryItemsDTO(items=items_dto, output_crs=output_crs)
        response = self.api.operation_union(
            project=self.project,
            geometry_items_dto=geometry_items,
            _request_timeout=self.timeout,
            geometry=geometry_format,
        )
        geometry = shape(response.geojson) if geometry_format == "geojson" else wkt.loads(response.wkt)
        return geometry

    def delete_layer(self, layer_name: str):
        """Delete feature layer and all related seismic items.

        Args:
            layer_name (str): name of the layer
        """
        layer_dto = FeatureLayerNameDTO(name=layer_name)
        self.api.delete_layer(self.project, layer_dto, _request_timeout=self.timeout)
