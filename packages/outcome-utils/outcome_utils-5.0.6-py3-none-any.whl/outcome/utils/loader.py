"""Load objects from a mod:obj path."""

from importlib import import_module, util
from types import ModuleType  # pragma: no cover
from typing import Optional, Type, TypeVar, cast

T = TypeVar('T')


def load_obj(objspec: str, default_obj: Optional[str] = None, *, t: Type[T] = object) -> T:
    parts = objspec.split(':')
    modname = None
    objname = None

    if len(parts) == 1:
        modname = parts[0]
        objname = default_obj

    elif len(parts) == 2:
        modname, objname = parts

    if not (modname and objname):
        raise ValueError(f'Invalid objspec: {objspec}')

    o = getattr(import_module(modname), objname)

    return cast(T, o)


def load_module(name: str, path: str, *, t: Type[T] = ModuleType) -> T:  # pragma: no cover
    spec = util.spec_from_file_location(name, path)
    mod = util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)  # type: ignore
    return cast(T, mod)
