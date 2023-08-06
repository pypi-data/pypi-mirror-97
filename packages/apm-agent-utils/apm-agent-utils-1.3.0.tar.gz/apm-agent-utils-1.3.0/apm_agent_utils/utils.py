import importlib
import inspect
import re
import sys

from qualname import qualname
from elasticapm.instrumentation.register import register

builtins = set(sys.builtin_module_names)


def get_python_version():
    return sys.version_info[0]


def get_function_name(func):
    module = func.__module__
    name = qualname(func)
    if hasattr(func, "__qualname__") and func.__qualname__:
        name = func.__qualname__
    return "{}.{}".format(module, name)


def _get_class_methods(c):
    """
    Return list of methods of given class
    """
    python_version = get_python_version()
    if python_version == 2:
        return [
            (func.__module__, qualname(func))
            for _, func in inspect.getmembers(c, inspect.ismethod)
        ]
    else:
        # python3
        return [
            (func.__module__, func.__qualname__)
            for _, func in inspect.getmembers(c, inspect.isfunction)
        ]


def get_module_funcs(module_path, pattern):
    """
    Return list of functions/methods of given module
    """

    def get_all_funcs(module):
        module_name = module.__name__
        functions = []
        for name, obj in inspect.getmembers(module):
            if hasattr(obj, "__module__") and not obj.__module__.startswith(module_name):
                continue
            if name in builtins:
                continue
            if inspect.isfunction(obj):
                functions.append(get_obj_name(obj))
            if inspect.ismethod(obj):
                functions.append(get_obj_name(obj))
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


def get_obj_name(obj):
    module = obj.__module__
    name = qualname(obj)
    if hasattr(obj, "__qualname__") and obj.__qualname__:
        name = obj.__qualname__
    return module, name


def get_instrumentation_path(cls):
    name = cls.__qualname__ or cls.__name__
    module = cls.__module__
    return "{}.{}".format(module, name)


def add_instrumentation(path):
    register(path)
