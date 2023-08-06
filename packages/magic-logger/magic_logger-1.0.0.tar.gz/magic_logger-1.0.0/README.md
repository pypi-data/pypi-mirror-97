# magic_logger
This very simple module does its best to help you use Python's `logging` correctly, by always
calling the correct logger for a module. No more boilerplace `logger.getLogger(__name__)` in every module!

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
For anything else, just use `logging` directly. `magic_logger` just proxies call over anyway so you can use `logging` as usual.

## How does it works?
When you ask for an attribute of `magic_logger.logger` (other than the configuration ones listed above),
it looks at the stack and determines the module from where the call originates. It then returns the attribute
of the same name of the correct logger for that module, using `logging.getLogger`. As simple as that!

### What if I call a module using `python -m` and log something from it, will that use the logger for `__main__`?
No, it will simply look at the module's `__spec__` for the name. Unless you're running an interactive session, you won't use the logger for `__main__`!

