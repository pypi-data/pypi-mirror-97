from tests.input_files.project_1.impl import MyPluginImplementation
from tests.input_files.project_1.spec import MyAggregatePlugin


def test_aggregate_plugin():
    plug_impl = MyPluginImplementation()
    with MyAggregatePlugin.register(plug_impl):
        plug = MyAggregatePlugin()
        assert plug.on_single_arg(10) == [20]
        assert plug.on_two_args(100, 200) == [(110, 210)]
        assert plug.on_kwargs(100) == [dict(value=110)]
        assert plug.on_args_and_kwargs(50, 60) == [(60, dict(value2=70))]
        assert plug.on_nothing() == [None]
        assert plug_impl.should_be_ten == 10
