"""
A flexible Python plugin framework supporting plugins in multiple languages
"""
from plugitin.spec import PluginSpec
from plugitin.plugin import Plugin
from plugitin.chain_plugin import ChainPlugin
from plugitin.aggregate_plugin import AggregatePlugin
from plugitin.finder.fs import FileSystemFinder
from plugitin.loader.fs import FilePluginLoader
from plugitin.finder.name import PackageNameFinder
from plugitin.loader.module import PythonModuleLoader
from plugitin.pyfs import load_args_kwargs, output_args_kwargs