import click
from gopublic.cli import pass_context, json_loads
from gopublic.decorators import custom_exception, dict_output


@click.command('publish')
@click.argument("path", type=str)
@click.argument("username", type=str)
@click.option(
    "--version",
    help="Version of the file to publish",
    default="1",
    show_default=True,
    type=int
)
@click.option(
    "--contact",
    help="Contact email for this file",
    type=str
)
@click.option(
    "--email",
    help="Contact email for notification when publication is done",
    type=str
)
@pass_context
@custom_exception
@dict_output
def cli(ctx, path, username, version=1, contact="", email=""):
    """Launch a publish task

Output:

    Dictionnary containing the response
    """
    return ctx.gi.file.publish(path, username, version=version, contact=contact, email=email)
