import click
import click_completion  # type: ignore

from tktl.cli.common import ClickGroup
from tktl.cli.delete import delete as delete_commands
from tktl.cli.get import get as get_commands
from tktl.cli.health import health
from tktl.cli.init import init
from tktl.cli.login import login, logout
from tktl.cli.run import run
from tktl.cli.validate import validate
from tktl.commands.version import get_version
from tktl.core.config import settings
from tktl.core.loggers import set_verbosity

click_completion.init()


@click.group(cls=ClickGroup, **settings.HELP_COLORS_DICT)
@click.option("-v", "--verbose", count=True, help="Set verbosity level")
def cli(verbose):
    set_verbosity(verbose)


cli.add_command(get_version)
cli.add_command(logout)
cli.add_command(login)
cli.add_command(init)
cli.add_command(get_version)
cli.add_command(delete_commands)
cli.add_command(get_commands)
cli.add_command(validate)
cli.add_command(run)
cli.add_command(health)
