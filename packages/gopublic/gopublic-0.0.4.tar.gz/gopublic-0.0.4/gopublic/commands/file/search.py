import click
from gopublic.cli import pass_context, json_loads
from gopublic.decorators import custom_exception, list_output


@click.command('search')
@click.argument("file_name", type=str)
@pass_context
@custom_exception
@list_output
def cli(ctx, file_name):
    """Launch a pull task

Output:

    List of files matching the search
    """
    return ctx.gi.file.search(file_name)
