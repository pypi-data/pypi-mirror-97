from typing import Optional

import typer

from plugitin.codegen.logic import generate_plugin_code_from_spec_file

cli = typer.Typer()


def generate_code(
    file: str = typer.Argument(
        ..., help="Input file which should contain subclass of PluginSpec"
    ),
    output_file: Optional[str] = typer.Option(
        None,
        "-o",
        "--output",
        help="Output file to write generated Plugin classes to. If not specified, writes to stdout",
    ),
):
    """
    Takes a file containing subclass(es) of PluginSpec and generates implementations
    of supported Plugin classes based on the call signatures and
    type annotations in PluginSpec
    """
    generate_plugin_code_from_spec_file(file, output_file=output_file)


def main():
    typer.run(generate_code)


if __name__ == "__main__":
    main()
