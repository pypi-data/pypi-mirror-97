__all__ = ["logger"]

import inspect
import logging
import logging.config
from functools import wraps


class Logger:
    """
    Proxy for `logging.Logger` but you always get the right logger for the module you're in.
    """
    @wraps(logging.config.fileConfig)
    def file_config(self, *args, **kwargs):
        """
        Proxy for `logging.config.fileConfig`. Uses `@wraps` to preserve original signature.
        """
        return logging.config.fileConfig(*args, **kwargs)
    
    @wraps(logging.config.dictConfig)
    def dict_config(self, *args, **kwargs):
        """
        Proxy for `logging.config.dictConfig`. Uses `@wraps` to preserve original signature.
        """
        return logging.config.dictConfig(*args, **kwargs)
    
    @wraps(logging.config.listen)
    def listen(self, *args, **kwargs):
        """
        Proxy for `logging.config.listen`. Uses `@wraps` to preserve original signature
        """
        return logging.config.listen(*args, **kwargs)
    
    @wraps(logging.config.stopListening)
    def stop_listening(self, *args, **kwargs):
        """
        Proxy for `logging.config.stopListening`. Uses `@wraps` to preserve original signature
        """
        return logging.config.stopListening(*args, **kwargs)
    
    def __getattr__(self, name):
        """
        Get the attribute with the same `name` but from the correct logger, as returned by
        `logger.getLogger`. The name of the logger is obtained by inspecting the stack and
        checking where we're called from.

        Args:
            name (str):

        Returns:
            attribute of the correct `Logger` object
        """
        # Get the module from which the call originates
        caller_module = inspect.getmodule(inspect.stack()[1][0])
        caller_name = caller_module.__name__

        # If the caller is invoked directly, get the correct name from the module spec
        if caller_name == "__main__" and caller_module.__spec__ is not None:
            caller_name = caller_module.__spec__.name

        # Get the requested attribute from the caller's logger
        return getattr(logging.getLogger(caller_name), name)


logger = Logger()
