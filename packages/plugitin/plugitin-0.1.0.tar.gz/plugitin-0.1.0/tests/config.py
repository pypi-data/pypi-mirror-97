from pathlib import Path
from typing import List, Dict

from plugitin.metas.fs import FilePluginMeta

TESTS_PATH = Path(__file__).parent
INPUT_FILES_PATH = TESTS_PATH / 'input_files'
PROJECT_1_PATH = INPUT_FILES_PATH / 'project_1'
PROJECT_1_PLUGINS_PATH = PROJECT_1_PATH / 'plugins'
PROJECT_1_SPEC_FILE = PROJECT_1_PATH / 'spec.py'
PROJECT_1_GENERATED_PLUGINS_FILE = PROJECT_1_PATH / 'plugins_generated.py'
PROJECT_1_FS_PYTHON_PLUG_PATH = PROJECT_1_PLUGINS_PATH / 'mypythonplug'
PROJECT_1_FS_JS_PLUG_PATH = PROJECT_1_PLUGINS_PATH / 'myjsplug'

EXPECT_PROJECT_1_PYTHON_META_DICT: Dict[str, FilePluginMeta] = {
    'on_nothing' : FilePluginMeta(PROJECT_1_FS_PYTHON_PLUG_PATH / "on_nothing.py"),
    'on_args_and_kwargs' : FilePluginMeta(PROJECT_1_FS_PYTHON_PLUG_PATH / "on_args_and_kwargs.py"),
    'on_kwargs' : FilePluginMeta(PROJECT_1_FS_PYTHON_PLUG_PATH / "on_kwargs.py"),
    'on_single_arg' : FilePluginMeta(PROJECT_1_FS_PYTHON_PLUG_PATH / "on_single_arg.py"),
    'on_two_args' : FilePluginMeta(PROJECT_1_FS_PYTHON_PLUG_PATH / "on_two_args.py"),
}
EXPECT_PROJECT_1_PYTHON_METAS: List[FilePluginMeta] = [val for val in EXPECT_PROJECT_1_PYTHON_META_DICT.values()]
EXPECT_PROJECT_1_PYTHON_METAS.sort(key=lambda meta: meta.name)

EXPECT_PROJECT_1_JS_META_DICT: Dict[str, FilePluginMeta] = {
    'on_nothing' : FilePluginMeta(PROJECT_1_FS_JS_PLUG_PATH / "on_nothing.js"),
    'on_args_and_kwargs' : FilePluginMeta(PROJECT_1_FS_JS_PLUG_PATH / "on_args_and_kwargs.js"),
    'on_kwargs' : FilePluginMeta(PROJECT_1_FS_JS_PLUG_PATH / "on_kwargs.js"),
    'on_single_arg' : FilePluginMeta(PROJECT_1_FS_JS_PLUG_PATH / "on_single_arg.js"),
    'on_two_args' : FilePluginMeta(PROJECT_1_FS_JS_PLUG_PATH / "on_two_args.js"),
}
EXPECT_PROJECT_1_JS_METAS: List[FilePluginMeta] = [val for val in EXPECT_PROJECT_1_JS_META_DICT.values()]
EXPECT_PROJECT_1_JS_METAS.sort(key=lambda meta: meta.name)