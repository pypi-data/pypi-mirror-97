from typing import List


class PluginSpec:
    name: str = ""

    def __init__(self):
        if not self.name:
            self.name = self.__class__.__name__

    @classmethod
    def _method_names(cls) -> List[str]:
        skip_names: List[str] = [
            "name",
        ]
        return [
            name
            for name in dir(cls)
            if not name.startswith("_") and name not in skip_names
        ]
