import subprocess
from functools import partial
from pathlib import Path
import json
import sys
from typing import Dict, Callable, List

from plugitin import PluginSpec
from plugitin.metas.fs import FilePluginMeta
from plugitin.loader.base import PluginLoader

FILE_EXECUTORS: Dict[str, str] = {
    'py': sys.executable,
    'js': 'node'
}


def run_file(executor: str, path: Path, *args, **kwargs):
    arg_spec = dict(args=args, kwargs=kwargs)
    json_str = json.dumps(arg_spec)
    try:
        result = subprocess.run(
            f'{executor} {str(path.resolve())}',
            input=json_str.encode('utf8'),
            capture_output=True,
            check=True,
            shell=True,
        )
    except subprocess.CalledProcessError as e:
        print(e.stderr.decode('utf8'))
        raise e
    if not result.stdout:
        return

    result_dict = json.loads(result.stdout)
    args, kwargs = result_dict["args"], result_dict["kwargs"]
    if not args and not kwargs:
        return
    elif args and not kwargs:
        if isinstance(args, list):
            return tuple(args)
        return args
    elif not args and kwargs:
        return kwargs
    else:
        # args and kwargs
        if isinstance(args, list):
            return tuple(args), kwargs
        return args, kwargs


class FilePluginLoader(PluginLoader[FilePluginMeta]):
    metadata_class = FilePluginMeta
    file_executors: Dict[str, str] = FILE_EXECUTORS

    def _get_run_func(self, meta: FilePluginMeta) -> Callable:
        try:
            executor = self.file_executors[meta.extension]
        except KeyError:
            raise NotImplementedError(f'No implemented executor for extension {meta.extension}')
        run_this_file = partial(run_file, executor, meta.file_path)
        return run_this_file

    def load(self, meta: FilePluginMeta) -> List[PluginSpec]:
        plug = PluginSpec()
        run_this_file = self._get_run_func(meta)
        setattr(plug, meta.name, run_this_file)
        return [plug]
