[![pipeline status](https://gitlab.com/DAtek/app-utils/badges/master/pipeline.svg)](https://gitlab.com/DAtek/app-utils/-/commits/master)
[![coverage report](https://gitlab.com/DAtek/app-utils/badges/master/coverage.svg)](https://gitlab.com/DAtek/app-utils/-/commits/master)

# Utilities for building applications.

## Contains: 
- Logging
- Loading config from environment variables

## Config usage: 
```python
import os

from datek_app_utils.env_config import BaseConfig

os.environ["COLOR"] = "RED"
os.environ["TEMPERATURE"] = "50"


class Config(BaseConfig):
    COLOR: str
    TEMPERATURE: int


assert Config.COLOR == "RED"
assert Config.TEMPERATURE == 50
```

The values are being casted if you read them.
Moreover, you can test whether all of the variables have been set or not.

```python
import os

from datek_app_utils.env_config import BaseConfig, validate_config

os.environ["COLOR"] = "RED"


class Config(BaseConfig):
    COLOR: str
    TEMPERATURE: int


assert not validate_config(Config)
```
outputs:
```
2021-03-05 19:03:22,023 [env_config.py:58] INFO     Validating config: Config
2021-03-05 19:03:22,023 [env_config.py:62] INFO     COLOR: RED
2021-03-05 19:03:22,023 [env_config.py:66] ERROR    Environmental variable `TEMPERATURE` is not set. Required type: <class 'int'>
```