from dataclasses import dataclass
from pathlib import Path
from typing import List, Sequence

from plugitin.metas.base import PluginMeta


@dataclass
class FilePluginMeta(PluginMeta):
    file_path: Path

    def __post_init__(self):
        self.file_path = Path(self.file_path).resolve()

    @property
    def extensions(self) -> List[str]:
        return [suff.replace(".", "").casefold() for suff in self.file_path.suffixes]

    @property
    def extension(self) -> str:
        exts = self.extensions
        if len(exts) > 1:
            raise NotImplementedError(f'more than one extension exists for {self}')
        return exts[0]

    @property
    def name(self) -> str:
        return self.file_path.stem

    @property
    def plugin_name(self) -> str:
        return self.file_path.parent.stem

    def extensions_match(self, exts: Sequence[str]) -> bool:
        exts = [ext.replace(".", "").casefold() for ext in exts]
        return all([ext in exts for ext in self.extensions])