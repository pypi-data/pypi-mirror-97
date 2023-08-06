import os
from typing import Tuple, Iterable, Generator, Sequence, Optional, List, Type

from plugitin.metas.fs import FilePluginMeta
from plugitin.spec import PluginSpec
from plugitin.finder.base import PluginFinder

DEFAULT_SEARCH_PATHS: Tuple[str, ...] = ("plugins",)


class FileSystemFinder(PluginFinder[FilePluginMeta]):
    metadata_class = FilePluginMeta

    def __init__(
        self,
        find_names: Optional[Sequence[str]] = None,
        find_exts: Optional[Sequence[str]] = None,
        search_paths: Iterable[str] = DEFAULT_SEARCH_PATHS,
    ):
        self.find_names = find_names
        self.find_exts = find_exts
        self.search_paths = search_paths
        self._validate()

    def _validate(self):
        if self.find_names is None and self.find_exts is None:
            raise ValueError("must pass at least one of find_names or find_exts")

    @classmethod
    def from_spec(cls, spec: Type[PluginSpec], search_paths: Iterable[str] = DEFAULT_SEARCH_PATHS,):
        return cls(find_names=spec._method_names(), search_paths=search_paths)

    def find(self) -> Generator[FilePluginMeta, None, None]:
        found_meta: List[FilePluginMeta] = []
        for sp in self.search_paths:
            for root, _, files in os.walk(sp):
                for file in files:
                    file_path = os.path.join(root, file)
                    meta = FilePluginMeta(file_path)   # type: ignore
                    if self.find_names is not None:
                        if meta.name in self.find_names:
                            found_meta.append(meta)
                            yield meta
                    if self.find_exts is not None:
                        if meta.extensions_match(self.find_exts):
                            if meta not in found_meta:
                                found_meta.append(meta)
                                yield meta
