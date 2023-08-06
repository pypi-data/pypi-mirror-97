from typing import Tuple, Any, Dict
import sys
import json


def load_args_kwargs() -> Tuple[Tuple[Any, ...], Dict[str, Any]]:
    input_data = json.loads(sys.stdin.read())
    args, kwargs = input_data["args"], input_data["kwargs"]
    return args, kwargs


def output_args_kwargs(*args, **kwargs):
    if len(args) == 1:
        args = args[0]
    data = dict(args=args, kwargs=kwargs)
    json_str = json.dumps(data)
    print(json_str)
