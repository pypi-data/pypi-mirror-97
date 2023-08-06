import importlib
import inspect
import re
import sys
from functools import partial

try:
    from functools import partialmethod

    partial_types = (partial, partialmethod)
except ImportError:
    # Python 2
    partial_types = (partial,)

from elasticapm.instrumentation.register import register

builtins = set(sys.builtin_module_names)


def get_function_name(func):
    # partials don't have `__module__` or `__name__`, so we use the values from the "inner" function
    if isinstance(func, partial_types):
        return "partial({})".format(get_function_name(func.func))
    elif hasattr(func, "_partialmethod") and hasattr(
        func._partialmethod, "func"
    ):
        return "partial({})".format(
            get_function_name(func._partialmethod.func)
        )
    module = func.__module__
    name = func.__name__
    if hasattr(func, "__qualname__"):
        if func.__qualname__:
            name = func.__qualname__
    return f"{module}.{name}"


def _get_class_methods(c):
    """
    Return list of methods of given class
    """
    return [
        (func.__module__, func.__qualname__)
        for _, func in inspect.getmembers(c, inspect.isfunction)
    ]


def get_module_funcs(module_path, pattern):
    """
    Return list of functions/methods of given module
    """

    def get_all_funcs(module):
        functions = []
        for name, obj in inspect.getmembers(module):
            if name in builtins:
                continue
            if inspect.isfunction(obj):
                functions.append((obj.__module__, obj.__qualname__))
            if inspect.ismethod(obj):
                functions.append((obj.__module__, obj.__qualname__))
            if inspect.isclass(obj):
                if issubclass(obj, Exception):
                    continue
                functions.extend(_get_class_methods(obj))
        return functions

    try:
        module_obj = importlib.import_module(module_path)
    except ImportError as e:
        return []
    results = []
    functions = get_all_funcs(module_obj)
    for func in functions:
        md_name, func_name = func
        if not md_name or not md_name.startswith(module_obj.__name__):
            continue
        if not re.search(pattern, func_name):
            continue
        results.append(func)
    return results


def get_instrumentation_path(cls: type):
    name = cls.__qualname__ or cls.__name__
    module = cls.__module__
    return f"{module}.{name}"


def add_instrumentation(path):
    register(path)
