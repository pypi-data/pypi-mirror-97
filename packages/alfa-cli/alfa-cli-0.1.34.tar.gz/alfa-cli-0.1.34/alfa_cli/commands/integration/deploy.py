import os
import tempfile
import click

from alfa_sdk.common.helpers import AlfaConfigHelper
from alfa_sdk.common.exceptions import ResourceNotFoundError
from alfa_cli.common.click import BaseCliCommand
from alfa_cli.common.exceptions import AlfaCliError
from alfa_cli.common.helpers.file import package_dir
from alfa_cli.config import algorithm as algorithm_config


@click.command(cls=BaseCliCommand)
@click.argument("path", type=str)
@click.option("--spec", type=str, default=algorithm_config.defaults.specification.path, show_default=True, help="Path of the specification file.")
@click.option("-i", "--id", "id_", type=str, help="Integration id.")
@click.option("-e", "--env", type=str, help="Environment name. Overrides specification file.")
@click.option("-v", "--version", type=str, help="Release version. Overrides specification file.")
@click.option("-d", "--desc", type=str, help="Release description. Overrides specification file.")
@click.option("-n", "--notes", type=str, help="Release notes. Prioritized over --notes-path.")
@click.option("-np", "--notes-path", type=str, help="Path to file with release notes.")
@click.option("-c", "--commit", help="Commit hash to append to release description.")
@click.option("--increment", is_flag=True, help="Enables auto increment of version number.")
@click.pass_obj
def deploy(obj, path, *, increment=False, commit, **kwargs):
    """Deploy a new integration release.

    The integration must be structured in the correct way and contain a valid specification file.
    Information on the integration to deploy will be extracted from the specification file, but
    can be overriden. If a non existing integration environment is specified, it will be created."""

    client = obj["client"]()
    conf = AlfaConfigHelper.load(os.path.join(path, kwargs.get("spec")), is_package=False)

    #

    integration_id = kwargs.get("id_") or conf.get("id")
    environment_name = kwargs.get("env") or conf.get("environment")
    version = kwargs.get("version") or conf.get("version")

    if integration_id is None:
        raise AlfaCliError(message="No integration id found in specification file arguments.")
    if environment_name is None:
        raise AlfaCliError(message="No environment name found in specification file and arguments.")
    if version is None:
        raise AlfaCliError(message="No release version found in specification file and arguments.")

    #

    description = kwargs.get("desc") or conf.get("description", "")
    if commit is not None:
        description = "{} [{}]".format(description, commit)

    notes = kwargs.get("notes")
    notes_path = kwargs.get("notes_path")
    if not notes and notes_path:
        notes = open(notes_path, "r").read()

    #

    try:
        integration = client.get_integration(integration_id)
    except ResourceNotFoundError:
        raise AlfaCliError(
            message="Integration {} not found. You must first create an integration through the ALFA Console.".format(
                integration_id
            )
        )

    try:
        environment = integration.get_environment(environment_name)
    except ResourceNotFoundError:
        environment = integration.create_environment(environment_name)

    #

    if kwargs.get("spec") != algorithm_config.defaults.specification.path:
        os.rename(kwargs.get("spec"), algorithm_config.defaults.specification.path)
    tmp = tempfile.NamedTemporaryFile(prefix="ais-deploy-", suffix=".zip")
    package_dir(path, tmp.name, conf=conf)

    res = environment.deploy(
        version, tmp.name, increment=increment, description=description, release_notes=notes
    )
    return obj["logger"].result(res)
