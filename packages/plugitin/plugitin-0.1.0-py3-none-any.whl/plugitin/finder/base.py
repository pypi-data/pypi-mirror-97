from typing import Generator, TypeVar, Type, List
from typing_extensions import Protocol

T = TypeVar("T")


class PluginFinder(Protocol[T]):
    metadata_class: Type[T]

    def find(self) -> Generator[T, None, None]:
        ...

    def find_all(self) -> List[T]:
        return [item for item in self.find()]
