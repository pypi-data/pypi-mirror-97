from dataclasses import dataclass
from types import ModuleType
from typing import List

from plugitin.metas.base import PluginMeta


@dataclass
class PythonModuleMeta(PluginMeta):
    import_path: str
    module: ModuleType

    @property
    def path_parts(self) -> List[str]:
        return self.import_path.split('.')

    @property
    def plugin_name(self) -> str:
        return self.path_parts[-1]
