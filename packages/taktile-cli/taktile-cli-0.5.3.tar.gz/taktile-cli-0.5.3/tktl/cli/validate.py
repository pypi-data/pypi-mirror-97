import click

from tktl.cli.common import (
    ClickGroup,
    validate_integration_shared_options,
    validate_project_shared_options,
)
from tktl.commands.validate import (
    validate_all,
    validate_import,
    validate_integration,
    validate_profiling,
    validate_project_config,
    validate_unittest,
)
from tktl.core.config import settings


@click.group(
    "validate", help="Validate the project", cls=ClickGroup, **settings.HELP_COLORS_DICT
)
def validate():
    pass


@validate.command("config", help="Validate the configuration")
@click.option(
    "--path", "-p", help="Validate project located at this path", type=str, default="."
)
def validate_config_command(path) -> None:
    """Validates a new project for the necessary scaffolding, as well as the supporting
    files needed. The directory structure of a new project.
    """
    validate_project_config(path=path)


@validate.command("import", help="Validate src/endpoints.py")
@validate_project_shared_options
def validate_import_command(path: str, nocache: bool) -> None:
    validate_import(path=path, nocache=nocache)


@validate.command("unittest", help="Validate the unittests")
@validate_project_shared_options
def validate_unittest_command(path: str, nocache: bool) -> None:
    validate_unittest(path=path, nocache=nocache)


@validate.command("integration", help="Validate integration")
@validate_integration_shared_options
@validate_project_shared_options
def validate_integration_command(
    path: str, nocache: bool, timeout: int, retries: int
) -> None:
    validate_integration(path=path, nocache=nocache, timeout=timeout, retries=retries)


@validate.command("profiling", help="Validate profiling")
@validate_integration_shared_options
@validate_project_shared_options
def validate_profiling_command(
    path: str, nocache: bool, timeout: int, retries: int
) -> None:
    validate_profiling(path=path, nocache=nocache, timeout=timeout, retries=retries)


@validate.command("all", help="Validate everything")
@validate_integration_shared_options
@validate_project_shared_options
def validate_all_command(path: str, nocache: bool, timeout: int, retries: int) -> None:
    validate_all(path=path, nocache=nocache, timeout=timeout, retries=retries)
