import click
from gopublic.commands.file.list import cli as list
from gopublic.commands.file.publish import cli as publish
from gopublic.commands.file.search import cli as search


@click.group()
def cli():
    """
    Manipulate files managed by Gopublish
    """
    pass


cli.add_command(list)
cli.add_command(publish)
cli.add_command(search)
