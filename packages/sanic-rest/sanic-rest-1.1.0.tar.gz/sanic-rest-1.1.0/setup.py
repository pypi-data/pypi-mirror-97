# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sanic_rest']

package_data = \
{'': ['*']}

install_requires = \
['gcp-pilot[storage,datastore]', 'sanic', 'sanic-openapi']

extras_require = \
{'auth': ['sanic-jwt', 'passlib', 'argon2_cffi']}

setup_kwargs = {
    'name': 'sanic-rest',
    'version': '1.1.0',
    'description': 'Sanic Rest Framework with Google Cloud Datastore',
    'long_description': '![Github CI](https://github.com/flamingo-run/sanic-rest/workflows/Github%20CI/badge.svg)\n[![Maintainability](https://api.codeclimate.com/v1/badges/0d6eb6158bc33aa2af1c/maintainability)](https://codeclimate.com/github/flamingo-run/sanic-rest/maintainability)\n[![Test Coverage](https://api.codeclimate.com/v1/badges/0d6eb6158bc33aa2af1c/test_coverage)](https://codeclimate.com/github/flamingo-run/sanic-rest/test_coverage)\n[![python](https://img.shields.io/badge/python-3.9-blue.svg)]()\n\n# Sanic Rest Framework\n\n## Installation\n\n`pip install sanic-rest`\n',
    'author': 'Joao Daher',
    'author_email': 'joao@daher.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/flamingo-run/sanic-rest',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
