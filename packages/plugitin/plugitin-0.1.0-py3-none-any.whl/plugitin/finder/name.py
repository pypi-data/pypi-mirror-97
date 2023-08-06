from typing import Generator
import importlib
import pkgutil

from plugitin.finder.base import PluginFinder
from plugitin.metas.module import PythonModuleMeta


class PackageNameFinder(PluginFinder[PythonModuleMeta]):
    metadata_class = PythonModuleMeta

    def __init__(self, prefix: str):
        self.prefix = prefix

    def find(self) -> Generator[PythonModuleMeta, None, None]:
        name: str
        for finder, name, ispkg in pkgutil.iter_modules():
            if name.startswith(self.prefix):
                mod = importlib.import_module(name)
                meta = PythonModuleMeta(name, mod)
                yield meta