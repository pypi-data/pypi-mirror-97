import click
from gopublic.cli import pass_context, json_loads
from gopublic.decorators import custom_exception, list_output


@click.command('list')
@pass_context
@custom_exception
@list_output
def cli(ctx):
    """List files published in Gopublish

Output:

    List of files
    """
    return ctx.gi.file.list()
