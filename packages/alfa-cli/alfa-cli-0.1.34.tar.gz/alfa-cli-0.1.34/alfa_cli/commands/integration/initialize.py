import click
from alfa_cli.common.click import BaseCliCommand
from alfa_cli.lib.initializer import generate_specification, generate_files

@click.command(cls=BaseCliCommand)
def init():
    """Create the file structure for a new algorithm"""
    specification = generate_specification("integration")
    generate_files(specification, "integration")
