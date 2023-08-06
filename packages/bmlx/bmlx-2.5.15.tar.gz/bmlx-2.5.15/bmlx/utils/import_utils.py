"""Import Utils"""
import importlib
from typing import Any, Callable, Text, Type
from bmlx.utils import io_utils


def import_class_by_path(class_path: Text) -> Type[Any]:
    """Import a class by its <module>.<name> path.

    Args:
      class_path: <module>.<name> for a class.

    Returns:
      Class object for the given class_path.
    """
    classname = class_path.split(".")[-1]
    modulename = ".".join(class_path.split(".")[0:-1])
    mod = importlib.import_module(modulename)
    return getattr(mod, classname)


def import_func_from_source(source_path: Text, fn_name: Text) -> Callable:
    """Imports a function from a module provided as source file."""
    try:
        spec = importlib.util.spec_from_file_location(
            "user_module", source_path
        )

        if not spec:
            raise ImportError()

        user_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(user_module)  # pytype: disable=attribute-error
        return getattr(user_module, fn_name)

    except IOError:
        raise ImportError(
            "{} in {} not found in import_func_from_source()".format(
                fn_name, source_path
            )
        )


def import_func_from_module(
    module_path: Text, fn_name: Text
) -> Callable:  # pylint: disable=g-bare-generic
    """Imports a function from a module provided as source file or module path."""
    user_module = importlib.import_module(module_path)
    return getattr(user_module, fn_name)
