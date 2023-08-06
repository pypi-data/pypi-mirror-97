# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['config_proxy']
install_requires = \
['jsonpath-ng>=1.5.2,<2.0.0', 'jsonschema>=3.2.0,<4.0.0']

setup_kwargs = {
    'name': 'config-proxy',
    'version': '0.1.0',
    'description': 'Configuration proxy that enables specifying both source json path and / or environmental variable in order to get configuration value',
    'long_description': None,
    'author': 'Tomas Votava',
    'author_email': 'info@tomasvotava.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
