import sys
import click
import traceback

from alfa_cli import __version__
from alfa_cli.common.logger import Logger


#


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option("-d", "--verbose", is_flag=True, default=None, help="Enable verbose outputs.")
@click.option("-p", "--pretty", is_flag=True, default=None, help="Pretty print the results.")
@click.option("-of", "--output-file", type=str, help="Path of file to write the output to.")
@click.version_option(version=__version__)
@click.pass_context
def alfa(ctx=None, verbose=None, pretty=None, output_file=None):
    """CLI tools for working with ALFA (Algorithm Factory)."""

    if ctx.obj is None:
        ctx.obj = dict()

    logger = Logger(verbose=verbose, pretty=pretty, output_file=output_file)
    ctx.obj["pretty"] = pretty
    ctx.obj["logger"] = logger
