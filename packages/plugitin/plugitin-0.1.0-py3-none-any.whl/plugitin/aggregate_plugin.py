from typing import Tuple, Any, Dict, Optional

from plugitin import Plugin


class AggregatePlugin(Plugin):
    def execute(self, method_name: str, *args, **kwargs):
        results = []
        for handler in self.handlers:
            method = getattr(handler, method_name)
            result = method(*args, **kwargs)
            results.append(result)
        return results
