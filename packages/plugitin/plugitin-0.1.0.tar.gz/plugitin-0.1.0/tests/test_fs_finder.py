from typing import Any, List

from plugitin import FileSystemFinder
from plugitin.metas.fs import FilePluginMeta
from tests import config as conf
from tests.input_files.project_1.spec import MyPluginSpec


def _assert_found(finder: FileSystemFinder, found: Any):
    find_iter: List[FilePluginMeta] = [item for item in finder.find()]
    find_iter.sort(key=lambda meta: meta.name)
    assert find_iter == found
    assert sorted(finder.find_all(), key=lambda meta: meta.name) == found


def test_fs_finder_find_names_python():
    finder = FileSystemFinder(
        ["on_nothing"], search_paths=[conf.PROJECT_1_FS_PYTHON_PLUG_PATH]
    )
    expect_meta = FilePluginMeta(conf.PROJECT_1_FS_PYTHON_PLUG_PATH / "on_nothing.py")
    _assert_found(finder, [expect_meta])


def test_fs_finder_find_exts_python():
    finder = FileSystemFinder(
        find_exts=["py"], search_paths=[conf.PROJECT_1_FS_PYTHON_PLUG_PATH]
    )
    _assert_found(finder, conf.EXPECT_PROJECT_1_PYTHON_METAS)


def test_fs_finder_from_spec_python():
    finder = FileSystemFinder.from_spec(
        MyPluginSpec, search_paths=[conf.PROJECT_1_FS_PYTHON_PLUG_PATH]
    )
    _assert_found(finder, conf.EXPECT_PROJECT_1_PYTHON_METAS)


def test_fs_finder_find_names_js():
    finder = FileSystemFinder(
        ["on_nothing"], search_paths=[conf.PROJECT_1_FS_JS_PLUG_PATH]
    )
    expect_meta = FilePluginMeta(conf.PROJECT_1_FS_JS_PLUG_PATH / "on_nothing.js")
    _assert_found(finder, [expect_meta])


def test_fs_finder_find_exts_js():
    finder = FileSystemFinder(
        find_exts=["js"], search_paths=[conf.PROJECT_1_FS_JS_PLUG_PATH]
    )
    _assert_found(finder, conf.EXPECT_PROJECT_1_JS_METAS)


def test_fs_finder_from_spec_js():
    finder = FileSystemFinder.from_spec(
        MyPluginSpec, search_paths=[conf.PROJECT_1_FS_JS_PLUG_PATH]
    )
    _assert_found(finder, conf.EXPECT_PROJECT_1_JS_METAS)