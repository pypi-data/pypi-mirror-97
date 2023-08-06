# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datek_app_utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'datek-app-utils',
    'version': '0.2.0',
    'description': 'Utilities for building applications',
    'long_description': '[![pipeline status](https://gitlab.com/DAtek/app-utils/badges/master/pipeline.svg)](https://gitlab.com/DAtek/app-utils/-/commits/master)\n[![coverage report](https://gitlab.com/DAtek/app-utils/badges/master/coverage.svg)](https://gitlab.com/DAtek/app-utils/-/commits/master)\n\n# Utilities for building applications.\n\n## Contains: \n- Logging\n- Loading config from environment variables\n\n## Config usage: \n```python\nimport os\n\nfrom datek_app_utils.env_config import BaseConfig\n\nos.environ["COLOR"] = "RED"\nos.environ["TEMPERATURE"] = "50"\n\n\nclass Config(BaseConfig):\n    COLOR: str\n    TEMPERATURE: int\n\n\nassert Config.COLOR == "RED"\nassert Config.TEMPERATURE == 50\n```\n\nThe values are being casted if you read them.\nMoreover, you can test whether all of the variables have been set or not.\n\n```python\nimport os\n\nfrom datek_app_utils.env_config import BaseConfig, validate_config\n\nos.environ["COLOR"] = "RED"\n\n\nclass Config(BaseConfig):\n    COLOR: str\n    TEMPERATURE: int\n\n\nassert not validate_config(Config)\n```\noutputs:\n```\n2021-03-05 19:03:22,023 [env_config.py:58] INFO     Validating config: Config\n2021-03-05 19:03:22,023 [env_config.py:62] INFO     COLOR: RED\n2021-03-05 19:03:22,023 [env_config.py:66] ERROR    Environmental variable `TEMPERATURE` is not set. Required type: <class \'int\'>\n```',
    'author': 'Attila Dudas',
    'author_email': 'attila.dudas@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/DAtek/app-utils',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
