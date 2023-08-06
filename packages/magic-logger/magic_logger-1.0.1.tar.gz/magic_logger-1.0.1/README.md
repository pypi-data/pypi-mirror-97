# magic_logger
| Coverage | Release |
| :------: | :-----: |
| [![Coverage Status](https://coveralls.io/repos/github/RaduG/magic_logger/badge.svg?branch=master)](https://coveralls.io/github/RaduG/magic_logger?branch=master) | ![Release](https://badge.fury.io/py/magic-logger.svg) |

This very simple module does its best to help you use Python's `logging` correctly, by making sure you always
invoke the right `Logger` for a module. No more boilerplace `logger.getLogger(__name__)`! All this
without any external dependencies - this is just a tiny wrapper for `logging`.

## Getting started
To install:
```bash
pip install magic_logger==1.0.0
```

## Overview
Import `logger` from `magic_logger` and just call any methods you'd normally call on a `logging.Logger` instance:

```python
# Let's assume we are in `mypackage.mymodule`
from magic_logger import logger

logger.info("Someting very informative")  # equivalent to logging.getLogger(__name__).info(...)
```

`magic_logger.logger` also acts like a proxy for other commonly used functions in `logging.config`:
```python
logger.dict_config(...)  # dispatches to logging.config.dictConfig
logger.file_config(...)  # dispatches to logging.config.file_config
logger.listen(...)  # dispatches to logging.config.listen
logger.stop_listening(...)  # dispatches to logging.config.stopListening
``` 

### What about the other stuff in `logging`
For anything else, just use `logging` directly. `magic_logger` just proxies calls over anyway so you can use `logging` as usual.

## How does it work?
When you ask for an attribute of `magic_logger.logger` (other than the configuration ones listed above),
it looks at the stack and determines the module from where the call originates. It then returns the attribute
of the same name of the correct logger for that module, using `logging.getLogger`. As simple as that!

### What if I call a module using `python -m` and log something from it, will that use the logger for `__main__`?
No, it will simply look at the module's `__spec__` for the name. Unless you run an interactive session and log straight from it,
you won't ever use the logger for `__main__`!

