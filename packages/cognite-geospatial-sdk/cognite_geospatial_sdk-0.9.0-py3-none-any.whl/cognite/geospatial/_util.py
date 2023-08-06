# Copyright 2020 Cognite AS

import base64
from typing import Optional, Union

import numpy as np
import pyarrow as pa
from cognite.geospatial._client import (
    AttributeTypeDTO,
    CoreGeometrySpatialItemDTO,
    ExternalIdDTO,
    InternalIdDTO,
    SpatialIdsDTO,
    UpdateSpatialItemDTO,
    UpdateSpatialItemWithIdDTO,
)
from cognite.geospatial.error import GeospatialError
from cognite.geospatial.types import SpatialItem, SpatialList, UpdateSpatialItem
from pyarrow import parquet as pq


def _check_id(id: int):
    """Check id integer limits.
    """
    if id is not None and id > 9007199254740991:
        raise ValueError("Invalid value for `id`, must be a value less than or equal to `9007199254740991`")
    if id is not None and id < 1:
        raise ValueError("Invalid value for `id`, must be a value greater than or equal to `1`")


def _check_external_id(external_id: str):
    """Check externalId limits (max=255).
    """
    if external_id is None:
        raise ValueError("Invalid value for `external_id`, must not be `None`")
    if external_id is not None and len(external_id) > 255:
        raise ValueError("Invalid value for `external_id`, length must be less than or equal to `255`")


def _check_either_external_id(id: int = None, external_id: str = None):
    """Check if id or external_id provided.
    """
    if id is None and external_id is None:
        raise ValueError("Either id or external_id must be provided")


def _get_response_items(response):
    if response is None:
        raise GeospatialError("Empty response")
    if response.items is None:
        raise GeospatialError("No items in response")
    return response.items


def _first_item(response):
    items = _get_response_items(response)
    if len(items) == 0:
        return None
    return items[0]


def _to_array(items):
    if items is None:
        raise GeospatialError("Data could not be None")
    else:
        single_item = not isinstance(items, list)
        if single_item:
            items = [items]
    return (items, single_item)


def _single_or_array(items, single):
    if single:
        return next(iter(items), None)

    return items


def _create_spatial_id(id: int = None, external_id: str = None):
    _check_either_external_id(id, external_id)
    if id is not None:
        return InternalIdDTO(id=id)
    elif external_id is not None:
        return ExternalIdDTO(external_id=external_id)
    raise GeospatialError(message="Id or external id is not provided")


def _create_spatial_ids(id: int = None, external_id: str = None) -> SpatialIdsDTO:
    item = _create_spatial_id(id=id, external_id=external_id)
    return SpatialIdsDTO(items=[item])


def _to_update_spatial_item(item: UpdateSpatialItem) -> UpdateSpatialItemDTO:
    update = UpdateSpatialItemDTO(
        name=item.name,
        description=item.description,
        metadata=item.metadata,
        asset_ids=item.asset_ids,
        attributes=_filter_simple_attributes(item.attributes),
        source=item.source,
    )
    return UpdateSpatialItemWithIdDTO(item_id=_create_spatial_id(item.id, item.external_id), update=update)


def _to_spatial_item(client, response) -> SpatialItem:
    spatial_item = SpatialItem(
        layer=response.layer,
        crs=response.crs,
        id=response.id,
        external_id=response.external_id,
        name=response.name,
        description=response.description,
        metadata=response.metadata,
        asset_ids=response.asset_ids,
        source=response.source,
        attributes=response.attributes,
        created_time=response.created_time,
        last_updated_time=response.last_updated_time,
    )
    spatial_item.client = client
    return spatial_item


def _to_spatial_items(client, response, single: bool, layer_name: str = None) -> Union[SpatialItem, SpatialList]:
    items = _get_response_items(response)

    spatial_list = SpatialList(client=client, layer_name=layer_name)
    spatial_list.extend(list(map(lambda x: _to_spatial_item(client, x), items)))

    if single:
        return next(iter(spatial_list), None)

    return spatial_list


def _to_core_geometry_spatial_item(item: SpatialItem) -> CoreGeometrySpatialItemDTO:
    if item.id is not None:
        raise GeospatialError("Spatial item id must not be defined")
    return CoreGeometrySpatialItemDTO(
        name=item.name,
        external_id=item.external_id,
        description=item.description,
        metadata=item.metadata,
        asset_ids=item.asset_ids,
        layer=item.layer,
        source=item.source,
        attributes=_filter_simple_attributes(item.attributes),
        crs=item.crs,
    )


def _is_list(value) -> bool:
    return isinstance(value, list) or isinstance(value, np.ndarray) or isinstance(value, np.generic)


def _is_primitive(value) -> bool:
    return not _is_list(value)


def _filter_simple_attributes(attributes: Optional[dict]) -> dict:
    if attributes is None:
        return {}
    return {k: v for k, v in attributes.items() if _is_primitive(v)}


def _filter_list_attributes(attributes: Optional[dict]) -> dict:
    if attributes is None:
        return {}
    return {k: v for k, v in attributes.items() if _is_list(v)}


def _write_parquet(file, field_name: str, values, data_type):
    schema = pa.schema([pa.field(field_name, pa.list_(data_type))])
    records = list()
    records.append({field_name: values})
    columns = list()

    for column in schema.names:
        filed_type = schema.types[schema.get_field_index(column)]
        field_data = pa.array([v[column] for v in records], type=filed_type)
        columns.append(field_data)

    table = pa.Table.from_arrays(columns, schema=schema)
    with pq.ParquetWriter(file, schema, compression="zstd", use_byte_stream_split=True) as writer:
        writer.write_table(table)


def _decode_attribute(value, type: AttributeTypeDTO):
    if isinstance(value, str) and type in [AttributeTypeDTO.DOUBLE, AttributeTypeDTO.INT, AttributeTypeDTO.BOOLEAN]:
        byte_buffer = base64.urlsafe_b64decode(value)
        if type == AttributeTypeDTO.DOUBLE:
            return np.frombuffer(byte_buffer, dtype=">d")
        elif type == AttributeTypeDTO.INT:
            return np.frombuffer(byte_buffer, dtype=">i")
        elif type == AttributeTypeDTO.BOOLEAN:
            vector = np.frombuffer(byte_buffer, dtype=np.uint8)
            bit_array = np.unpackbits(vector, bitorder="little")
            bool_data = np.array(bit_array, dtype=bool)
            if len(bool_data) == 0:
                return bool_data
            true_index = np.argwhere(bool_data == True).flatten()  # noqa: E712
            if len(true_index) == 0:
                return bool_data
            return bool_data[: true_index[-1]]

    return value
