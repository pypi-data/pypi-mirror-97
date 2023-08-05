import click

from alfa_cli.common.click import BaseCliCommand
from alfa_cli.config import algorithm as algorithm_config
from alfa_cli.lib import trainer
from alfa_cli.lib.trainer.builders import (
    methods as methods_builder,
    search_options as search_options_builder,
)


@click.command(cls=BaseCliCommand)
@click.option(
    "--spec",
    type=str,
    default=algorithm_config.defaults.specification.path,
    show_default=True,
    help="Path of the specification file.",
)
@click.option(
    "--algorithm-id",
    "-a",
    type=str,
    help="If specified, the provided algorithm id will be set in the context; defaults to the algorithm id in the specification file.",
)
@click.option(
    "--environment-name",
    "-e",
    type=str,
    help="If specified, the provided environment name will be set in the context; defaults to the environment name in the specification file.",
)
@click.option(
    "--data", type=str, help="The data on which the algorithm instance needs to be trained",
)
@click.option(
    "--build-configuration",
    "-bc",
    type=str,
    help="The build configuration of the mass customization unit for which an instance needs to be built",
)
@click.option(
    "--tag",
    type=str,
    help="Tag of the mass customization unit for which an instance needs to be built",
)
@click.pass_obj
def train_local(obj, spec, algorithm_id, environment_name, data, build_configuration, tag):
    """
    Train an algorithm instance locally.
    """
    runners = trainer.initialize_runners(obj, spec, algorithm_id, environment_name)
    build_configuration = trainer.fetch_build_configuration(
        build_configuration, runners["build"].environment_id, tag, runners.get("search")
    )
    trainer.validate_build_configuration(build_configuration)
    data = trainer.fetch_data(data, build_configuration)

    res = None
    if runners.get("search") and build_configuration.get("searchOptions"):
        res = search_options_builder.build(build_configuration, runners, data)
    else:
        res = methods_builder.build(build_configuration, runners, data)

    return obj["logger"].result(res)
