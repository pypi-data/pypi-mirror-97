# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'python/src'}

packages = \
['cognite',
 'cognite.geospatial',
 'cognite.geospatial._client',
 'cognite.geospatial._client.api',
 'cognite.geospatial._client.models',
 'cognite.geospatial.error',
 'cognite.geospatial.shape',
 'cognite.geospatial.types',
 'cognite.geospatial.utils',
 'cognite.geospatial.visualization']

package_data = \
{'': ['*']}

install_requires = \
['cognite-sdk-core>=2.11.1,<3.0.0',
 'numpy',
 'pyarrow>=1.0,<2.0',
 'python-dateutil>=2.8,<3.0',
 'requests-oauthlib>=1.3.0,<2.0.0',
 'scipy>=1.5.4,<2.0.0',
 'shapely>=1.7,<2.0',
 'six>=1.15,<2.0',
 'urllib3>=1.25,<2.0']

setup_kwargs = {
    'name': 'cognite-geospatial-sdk',
    'version': '0.9.0',
    'description': 'Cognite Geospatial SDK store and query spatial objects in 2D and 3D space',
    'long_description': '<a href="https://cognite.com/">\n    <img src="https://github.com/cognitedata/cognite-python-docs/blob/master/img/cognite_logo.png" alt="Cognite logo" title="Cognite" align="right" height="80" />\n</a>\n\nCognite Geospatial SDK\n==========================\n[![PyPI version](https://badge.fury.io/py/cognite-geospatial-sdk.svg)](https://pypi.org/project/cognite-geospatial-sdk/)\n\nCognite Geospatial SDK for developers and data scientists working with Cognite Data Fusion (CDF).\n\n# Python\n\nA Python Geospatial SDK for the geospatial API. https://cognite-geospatial-sdk.readthedocs-hosted.com/\n\n## Prerequisites\nIn order to start using the Python SDK, you need\n- Python3 (>= 3.5) and pip\n- An API key. Never include the API key directly in the code or upload the key to github. Instead, set the API key as an environment variable. See the usage example for how to authenticate with the API key.\n\nThis is how you set the API key as an environment variable on Mac OS and Linux:\n```bash\n$ export COGNITE_API_KEY=<your API key>\n```\n\n## Installation\nTo install this package:\n```bash\n$ pip install cognite-geospatial-sdk\n```\n\n',
    'author': 'Cognite AS',
    'author_email': 'support@cognite.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
