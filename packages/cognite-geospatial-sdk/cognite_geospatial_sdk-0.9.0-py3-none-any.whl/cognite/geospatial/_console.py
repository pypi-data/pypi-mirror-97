# Copyright 2020 Cognite AS
# flake8: noqa

# Detect environment


def in_interactive_session():
    try:
        return __IPYTHON__ or False  # noqa
    except NameError:
        return False


def in_ipython_frontend():
    try:
        from IPython import get_ipython

        ip = get_ipython()  # noqa
        return "zmq" in str(type(ip)).lower()
    except NameError:
        pass
    except ModuleNotFoundError:
        pass

    return False
