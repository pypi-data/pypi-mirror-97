import inspect
from types import ModuleType
from typing import List, Type

from plugitin import PluginSpec
from plugitin.loader.base import PluginLoader
from plugitin.metas.module import PythonModuleMeta


def get_plugin_specs_from_module(mod: ModuleType) -> List[PluginSpec]:
    specs: List[PluginSpec] = []
    for val in mod.__dict__.values():
        if not inspect.isclass(val):
            continue
        # Library authors will be writing their own subclass of PluginSpec,
        # then their end users will be writing subclasses of their subclass.
        # We only want to pick up those final user subclasses and not the
        # library author subclasses
        if _is_non_direct_subclass(val, PluginSpec):
            specs.append(val())
    return specs


def _is_non_direct_subclass(cls: Type, base_type: Type):
    if not issubclass(cls, base_type):
        return False
    for base in inspect.getmro(cls)[1:]:  # first is same class, so skip
        if issubclass(base, base_type) and base != base_type:
            # A base class of cls is a subclass of base_type
            return True
    return False


class PythonModuleLoader(PluginLoader[PythonModuleMeta]):
    metadata_class = PythonModuleMeta

    def load(self, meta: PythonModuleMeta) -> List[PluginSpec]:
        return get_plugin_specs_from_module(meta.module)