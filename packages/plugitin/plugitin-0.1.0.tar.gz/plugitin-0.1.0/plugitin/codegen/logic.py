import ast
from copy import deepcopy
from pathlib import Path
from typing import List, Any, Optional

import astor
import black


def get_ast_from_file(path: Path) -> ast.Module:
    return ast.parse(path.read_text())


class PluginSpecAstExtractor(ast.NodeVisitor):
    def __init__(self):
        self.class_defs: List[ast.ClassDef] = []

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        for base in node.bases:
            # TODO [#1]: make codegen work if PluginSpec is renamed on import
            if base.id == "PluginSpec":  # type: ignore
                self.class_defs.append(node)
                break
        self.generic_visit(node)


def get_plugin_spec_asts_from_module_ast(tree: ast.Module) -> List[ast.ClassDef]:
    extractor = PluginSpecAstExtractor()
    extractor.visit(tree)
    return extractor.class_defs


def _ast_method_args_to_call_args(args: ast.arguments) -> ast.arguments:
    args = deepcopy(args)
    del args.args[0]  # delete self argument
    arg_attrs = (
        "args",
        "posonlyargs",
        "kwonlyargs",
        "vararg",
        "kwarg",
        "kw_defaults",
        "defaults",
    )
    for attr in arg_attrs:
        arg_list = getattr(args, attr)
        if arg_list is None:
            continue
        for arg in arg_list:
            arg.annotation = None
    # Up to here, for call signature (a: int, b: int = 10) will be
    # getting (a, b=10). Need to get to (a, b=b)
    for i, default in enumerate(reversed(args.defaults)):
        matched_arg = args.args[-(i + 1)]
        default.value = matched_arg.arg  # type: ignore
    # Now have (a, b="b"), will need to remove quotes after converting to string
    return args


class PluginTransformer:
    def transform_class_def(
        self,
        node: ast.ClassDef,
        replace_name: str = "Chain",
        plugin_name: str = "ChainPlugin",
    ) -> ast.ClassDef:
        new_node = deepcopy(node)
        plugin_spec_name = node.name
        new_name = plugin_spec_name.replace("Spec", replace_name)
        new_node.name = new_name
        new_bases = []
        for base in node.bases:
            if base.id == "PluginSpec":  # type: ignore
                new_base = deepcopy(base)
                new_base.id = plugin_name  # type: ignore
                new_bases.append(new_base)
            else:
                new_bases.append(base)
        new_node.bases = new_bases

        new_body = []
        for func_def in node.body:
            if not isinstance(func_def, ast.FunctionDef):
                # Don't modify non-methods
                new_body.append(func_def)
                continue
            new_def = deepcopy(func_def)
            new_def = self.transform_method(new_def)
            new_body.append(new_def)
        new_node.body = new_body
        return new_node

    def transform_method(self, func_def: ast.FunctionDef) -> ast.FunctionDef:
        execute_args = _ast_method_args_to_call_args(func_def.args)
        # Coming as (a, b="b"), replace quotes to get (a, b=b)
        execute_args_str = (
            astor.to_source(execute_args).replace('"', "").replace("'", "")
        )
        body_str = f'return self.execute("{func_def.name}", {execute_args_str})'
        ast_return = ast.parse(body_str).body
        func_def.body = ast_return
        return func_def


class ChainPluginTransformer(ast.NodeTransformer, PluginTransformer):
    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        new_node = self.transform_class_def(node, "Chain", "ChainPlugin")
        return new_node


class AggregatePluginTransformer(ast.NodeTransformer, PluginTransformer):
    def transform_method(self, func_def: ast.FunctionDef) -> ast.FunctionDef:
        func_def = super().transform_method(func_def)
        orig_ret = func_def.returns
        if orig_ret is None:
            return func_def
        # Wrap return type annotation in list
        new_ret = ast.Subscript(
            value=ast.Name(id="List"), slice=ast.Index(value=orig_ret)
        )
        func_def.returns = new_ret
        return func_def

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        new_node = self.transform_class_def(node, "Aggregate", "AggregatePlugin")
        return new_node


def plugin_spec_ast_to_chain_definition(tree: ast.ClassDef) -> str:
    tree = deepcopy(tree)
    transformer = ChainPluginTransformer()
    tree = transformer.visit(tree)
    return astor.to_source(tree)


def plugin_spec_ast_to_aggregate_definition(tree: ast.ClassDef) -> str:
    tree = deepcopy(tree)
    transformer = AggregatePluginTransformer()
    tree = transformer.visit(tree)
    return astor.to_source(tree)


def pretty_format_str(string: str) -> str:
    fm = black.FileMode()
    out_str = black.format_str(string, mode=fm)
    return out_str


def generate_plugin_code_from_spec_file(file: str, output_file: Optional[str] = None):
    path = Path(file)
    tree = get_ast_from_file(path)
    spec_defs = get_plugin_spec_asts_from_module_ast(tree)
    import_defs = [
        "from typing import *",
        "from plugitin import ChainPlugin, AggregatePlugin",
    ]
    import_def = "\n".join(import_defs)
    chain_defs = [plugin_spec_ast_to_chain_definition(spec) for spec in spec_defs]
    agg_defs = [plugin_spec_ast_to_aggregate_definition(spec) for spec in spec_defs]
    all_defs = [import_def, *chain_defs, *agg_defs]
    full_str = "\n\n".join(all_defs)
    pretty = pretty_format_str(full_str)
    if output_file is not None:
        Path(output_file).write_text(pretty)
    else:
        print(pretty)

    return pretty