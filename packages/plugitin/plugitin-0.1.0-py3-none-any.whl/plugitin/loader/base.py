from typing import Generator, TypeVar, Type, List, Sequence, Iterable
from typing_extensions import Protocol

from plugitin import ChainPlugin, AggregatePlugin, PluginSpec

T = TypeVar("T")


class PluginLoader(Protocol[T]):
    metadata_class: Type[T]

    def load(self, meta: T) -> List[PluginSpec]:
        ...

    def load_all(self, metas: Iterable[T]) -> List[PluginSpec]:
        meta_lists = [self.load(meta) for meta in metas]
        flat_list: List[PluginSpec] = []
        for ml in meta_lists:
            flat_list.extend(ml)
        return flat_list
