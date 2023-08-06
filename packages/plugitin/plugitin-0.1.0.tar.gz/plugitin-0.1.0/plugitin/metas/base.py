from typing_extensions import Protocol


class PluginMeta(Protocol):

    def plugin_name(self) -> str:
        ...