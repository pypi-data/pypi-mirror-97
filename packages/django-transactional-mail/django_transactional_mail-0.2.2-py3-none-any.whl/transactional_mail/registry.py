"""
Implements a registry for previews similar to the ModelAdmin registry in
the standard Django Admin app.
"""

from .emails import Email

class AlreadyRegistered(Exception):
    "Raised if a handler is registered to a previously registered owner"

class Registry:
    """
    The JobResultAnalyzer registry is analogous to the admin site registry.
    Register handlers to owners. Handlers should be subclasses of
    JobResultAnalyzer.
    """
    def __init__(self):
        self._registry = {}

    def register(self, name, klass):
        """Register an email class for preview"""
        if not issubclass(klass, Email):
            raise ValueError("Wrapped class must subclass Email")

        if name in self._registry:
            raise AlreadyRegistered()

        self._registry[name] = klass

    def get_handler(self, name):
        """Get the class for this name"""
        return self._registry.get(name)


_default_registry = Registry() #pylint: disable=invalid-name

def register(name):
    """Register the given object the wrapped handler class"""
    def wrapper(email_class):
        _default_registry.register(name, email_class)

        return email_class
    return wrapper


def get_handler(name):
    """Get the handler class for this name from the default registry"""
    return _default_registry.get_handler(name)
