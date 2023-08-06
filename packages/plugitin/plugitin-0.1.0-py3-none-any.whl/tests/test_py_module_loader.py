from plugitin import PythonModuleLoader
from plugitin.metas.module import PythonModuleMeta
from tests.input_files.project_1.spec import MyChainPlugin, MyAggregatePlugin
from tests.input_files.project_1 import impl

MODULE_METADATA = PythonModuleMeta("tests.input_files.project_1.impl", impl)


def test_load_and_run_chain_from_module():
    plugin_class = MyChainPlugin
    plug = MyChainPlugin()
    loader = PythonModuleLoader()
    (plugin,) = loader.load(MODULE_METADATA)

    with plugin_class.register(plugin):
        assert plug.on_single_arg(5) == 15
        assert plug.on_two_args(5, 10) == (15, 20)
        plug.on_nothing()
        assert plugin.should_be_ten == 10
        assert plug.on_kwargs(value=5) == dict(value=15)
        assert plug.on_args_and_kwargs(5, value2=10) == (15, dict(value2=20))


def test_load_and_run_aggregate_from_module():
    plugin_class = MyAggregatePlugin
    plug = MyAggregatePlugin()
    loader = PythonModuleLoader()
    (plugin,) = loader.load(MODULE_METADATA)

    with plugin_class.register(plugin):
        assert plug.on_single_arg(5) == [15]
        assert plug.on_two_args(5, 10) == [(15, 20)]
        plug.on_nothing()
        assert plugin.should_be_ten == 10
        assert plug.on_kwargs(value=5) == [dict(value=15)]
        assert plug.on_args_and_kwargs(5, value2=10) == [(15, dict(value2=20))]
