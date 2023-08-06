from typing import Tuple, Any, Dict, Optional

from plugitin import Plugin


class ChainPlugin(Plugin):
    def execute(
        self,
        method_name: str,
        *args,
        **kwargs
    ):
        for handler in self.handlers:
            method = getattr(handler, method_name)
            if not args and not kwargs:
                method()
            elif args and not kwargs:
                args = method(*args)
            elif not args and kwargs:
                kwargs = method(**kwargs)
            else:
                # args and kwargs
                args, kwargs = method(*args, **kwargs)

        if not args and not kwargs:
            return
        elif args and not kwargs:
            return args
        elif not args and kwargs:
            return kwargs
        else:
            # args and kwargs
            return args, kwargs

