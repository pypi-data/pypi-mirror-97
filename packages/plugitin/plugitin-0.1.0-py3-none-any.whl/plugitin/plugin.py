from abc import ABC, abstractmethod
from typing import List, Any, Tuple, Dict, Optional, Type

from plugitin.spec import PluginSpec

class RegisterContext:

    def __init__(self, plugin: Type['Plugin'], spec: PluginSpec):
        self.plugin = plugin
        self.spec = spec

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.plugin.handlers.remove(self.spec)

class Plugin(ABC):
    handlers: List[PluginSpec] = []

    @classmethod
    def register(cls, plugin: PluginSpec) -> RegisterContext:
        cls.handlers.append(plugin)
        return RegisterContext(cls, plugin)

    @classmethod
    def deregister(cls, plugin: PluginSpec):
        cls.handlers.remove(plugin)

    @abstractmethod
    def execute(self, method_name: str, *args, **kwargs):
        ...
