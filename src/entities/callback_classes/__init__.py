import pkgutil
import importlib
import inspect

from aiogram.filters.callback_data import CallbackData


__all__ = []


def _recursive_import_callback_classes():
    for finder, module_name, ispkg in pkgutil.walk_packages(__path__, __name__ + "."):
        module = importlib.import_module(module_name)
        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)
            if (
                inspect.isclass(attribute)
                and issubclass(attribute, CallbackData)
                and attribute.__module__ == module.__name__
            ):
                globals()[attribute_name] = attribute
                __all__.append(attribute_name)


_recursive_import_callback_classes()
