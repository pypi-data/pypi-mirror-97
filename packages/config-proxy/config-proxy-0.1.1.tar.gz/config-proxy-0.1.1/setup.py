# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['config_proxy']
install_requires = \
['jsonpath-ng>=1.5.2,<2.0.0', 'jsonschema>=3.2.0,<4.0.0']

setup_kwargs = {
    'name': 'config-proxy',
    'version': '0.1.1',
    'description': 'Configuration proxy that enables specifying both source json path and / or environmental variable in order to get configuration value',
    'long_description': '# config-proxy\n\nThis is a Python module that enables you to setup paths for both json configuration and configuration from env variables.\n\nIt automatically looks into environmental variables and either uses its value, or looks it up in json configuration file or falls back to default.\n\n## Install\n\nEither clone from this repository or use `pip` / `poetry` like so:\n\n### Via `pip`\n\n```console\npip install config-proxy\n```\n\n### Using `poetry`\n\n```console\npoetry add config-proxy\n```\n\n## Usage\n\n### Basic usage\n\nIf your configuration file is either called `config.json` and is expected in the current working directory or its location is set using `CONFIG_PATH` environmental variable, the usage is fairly easy:\n\n#### `config.json`\n\n```json\n{\n  "database": {\n    "host": "mydbhost.databases.com"\n  }\n}\n```\n\n#### `main.py`\n\n```python\nfrom config_proxy import StringProperty\n\ndatabase_host = StringProperty(path="database.host", env="DATABASE_HOST", default="localhost")\n\nprint(database_host.value)\n```\n\n```bash\n$ python main.py\nmydbhost.databases.com\n\n$ DATABASE_HOST="overridden.database.com" python main.py\noverridden.database.com\n```\n\n### Advanced usage\n\nIf you want to specify configuration file path and customize env variable that stores the path, you have to extend the `ConfigProxy` class and overload attributes you wish to change.\n\n#### `my-special-config.json`\n\n```json\n{\n    "database": {\n        "host": "mydbhost.databases.com"\n    }\n}\n```\n\n#### `custom.py`\n\n```python\nfrom config_proxy import ConfigProxy as _ConfigProxy, StringProperty\n\nclass ConfigProxy(_ConfigProxy):\n    env_location = "ENV_VARIABLE_THAT_CONTAINS_MY_CONFIG_PATH"\n    config_file_names = ["my-special-config.json"]\n\n```\n\n**Please note**, that `StringProperty` now does not know it should use your subclass instead, do not forget to specify it when creating the property:\n\n```python\ndatabase_host = StringProperty(path="database.host", env="DATABASE_HOST", default="localhost", proxy=ConfigProxy)\n\nprint(database_host.value)\n```\n\nIf you want to specify a custom config file, you can use:\n\n```bash\n$ ENV_VARIABLE_THAT_CONTAINS_MY_CONFIG_PATH="/actual/path/to/my/config.json" python custom.py\nmydbhost.databases.com\n```\n',
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
