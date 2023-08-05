# Copyright 2020 Cognite AS

"""
Expose public exceptions & warnings
"""

import asyncio
import json
from json.decoder import JSONDecodeError

from cognite.geospatial._client.rest import ApiException


class GeospatialError(Exception):
    """Geospatial reised for internal errors.
    Attributes:
        message: explanation of the error
    """

    def __init__(self, message):
        super().__init__(message)


def _throw_exception(ex: ApiException) -> None:
    if ex.body:
        try:
            error_json = json.loads(ex.body)
        except JSONDecodeError:
            # not a json
            raise ex
        if "error" in error_json:
            error = error_json["error"]
            raise GeospatialError(message=error["message"])
    raise ex


def api_exception_handler(func):
    if asyncio.iscoroutinefunction(func):

        async def inner_function(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except ApiException as e:
                _throw_exception(e)

        return inner_function
    else:

        def inner_function(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ApiException as e:
                _throw_exception(e)

        return inner_function
