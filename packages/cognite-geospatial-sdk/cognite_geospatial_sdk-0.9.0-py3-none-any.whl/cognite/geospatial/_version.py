# Copyright 2020 Cognite AS
# flake8: noqa
# mypy: allow-untyped-defs


def get_version():
    try:
        from importlib import metadata as importlib_metadata
    except ImportError:
        import importlib_metadata
    try:
        return importlib_metadata.version("cognite-geospatial-sdk")
    except:
        return "0.0.0-dev"
