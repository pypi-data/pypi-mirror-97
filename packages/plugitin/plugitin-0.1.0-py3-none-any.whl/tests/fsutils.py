import os
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Union


@contextmanager
def change_directory(dir: Union[str, Path]):
    current_directory = os.getcwd()
    os.chdir(dir)
    yield
    os.chdir(current_directory)


@contextmanager
def use_path(dir: Union[str, Path]):
    if isinstance(dir, Path):
        path_str = str(dir.resolve())
    else:
        path_str = str(dir)

    sys.path.insert(0, path_str)
    yield
    sys.path.remove(path_str)