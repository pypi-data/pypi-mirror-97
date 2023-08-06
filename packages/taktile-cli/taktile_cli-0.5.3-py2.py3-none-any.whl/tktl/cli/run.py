import click

from tktl.commands.run import run_container


@click.command()
@click.option(
    "--path",
    "-p",
    help="Directory where the deployment lives",
    required=False,
    default=".",
)
@click.option(
    "--nocache/--cache",
    help="Enable or disable using cache of images",
    is_flag=True,
    default=False,
)
@click.option("--background", help="Run the image in the background", is_flag=True)
@click.option(
    "--auth/--no-auth",
    help="Run with auth enabled or disabled. Enabled by default",
    default=True,
)
@click.option(
    "--color/--no-color",
    help="Enable or disable colored output",
    is_flag=True,
    default=True,
)
def run(path: str, nocache: bool, background: bool, auth: bool, color: bool) -> None:
    """
    Run a deployment locally

    Parameters
    ----------
    auth
    background
    nocache
    path
    color

    Returns
    -------

    """
    run_container(
        path=path,
        nocache=nocache,
        background=background,
        auth_enabled=auth,
        color_logs=color,
    )
