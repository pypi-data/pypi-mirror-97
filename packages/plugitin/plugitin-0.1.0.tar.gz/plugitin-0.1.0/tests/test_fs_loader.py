from typing import Dict
from unittest.mock import patch

from plugitin import FilePluginLoader
from plugitin.metas.fs import FilePluginMeta
from tests import config as conf
from tests.input_files.project_1.spec import MyChainPlugin, MyAggregatePlugin


class FileLoaderTest:
    loader = FilePluginLoader()
    meta_dict: Dict[str, FilePluginMeta] = {}
    file_extension: str

    def test_load_and_run_chain(self):
        plugin_class = MyChainPlugin
        plug = MyChainPlugin()
        expect_single_arg = self.meta_dict["on_single_arg"]
        (plugin,) = self.loader.load(expect_single_arg)
        with plugin_class.register(plugin):
            assert plug.on_single_arg(5) == 25

        expect_two_args = self.meta_dict["on_two_args"]
        (plugin,) = self.loader.load(expect_two_args)
        with plugin_class.register(plugin):
            assert plug.on_two_args(5, 10) == (25, 30)

        expect_nothing = self.meta_dict["on_nothing"]
        with patch("plugitin.loader.fs.run_file") as mock:
            (plugin,) = self.loader.load(expect_nothing)
            with plugin_class.register(plugin):
                plug.on_nothing()
                mock.assert_called_once_with(
                    self.loader.file_executors[self.file_extension],
                    expect_nothing.file_path,
                )

        expect_kwargs = self.meta_dict["on_kwargs"]
        (plugin,) = self.loader.load(expect_kwargs)
        with plugin_class.register(plugin):
            assert plug.on_kwargs(value=5) == dict(value=25)

        expect_args_and_kwargs = self.meta_dict["on_args_and_kwargs"]
        (plugin,) = self.loader.load(expect_args_and_kwargs)
        with plugin_class.register(plugin):
            assert plug.on_args_and_kwargs(5, value2=10) == (25, dict(value2=30))

    def test_load_and_run_aggregate(self):
        plugin_class = MyAggregatePlugin
        plug = MyAggregatePlugin()
        expect_single_arg = self.meta_dict["on_single_arg"]
        (plugin,) = self.loader.load(expect_single_arg)
        with plugin_class.register(plugin):
            assert plug.on_single_arg(5) == [25]

        expect_two_args = self.meta_dict["on_two_args"]
        (plugin,) = self.loader.load(expect_two_args)
        with plugin_class.register(plugin):
            assert plug.on_two_args(5, 10) == [(25, 30)]

        expect_nothing = self.meta_dict["on_nothing"]
        with patch("plugitin.loader.fs.run_file") as mock:
            (plugin,) = self.loader.load(expect_nothing)
            with plugin_class.register(plugin):
                plug.on_nothing()
                mock.assert_called_once_with(
                    self.loader.file_executors[self.file_extension],
                    expect_nothing.file_path,
                )

        expect_kwargs = self.meta_dict["on_kwargs"]
        (plugin,) = self.loader.load(expect_kwargs)
        with plugin_class.register(plugin):
            assert plug.on_kwargs(value=5) == [dict(value=25)]

        expect_args_and_kwargs = self.meta_dict["on_args_and_kwargs"]
        (plugin,) = self.loader.load(expect_args_and_kwargs)
        with plugin_class.register(plugin):
            assert plug.on_args_and_kwargs(5, value2=10) == [(25, dict(value2=30))]


class TestPythonFileLoader(FileLoaderTest):
    meta_dict = conf.EXPECT_PROJECT_1_PYTHON_META_DICT
    file_extension = "py"


class TestJSFileLoader(FileLoaderTest):
    meta_dict = conf.EXPECT_PROJECT_1_JS_META_DICT
    file_extension = "js"
