# coding: utf-8
import os

import click

from gopublish import GopublishInstance
from gopublic.cli import pass_context
from gopublic import config
from gopublic.io import warn, info

CONFIG_TEMPLATE = """## Gopublish's gopublic: Global Configuration File.
# Each stanza should contain a single gopublish server to control.
#
# You can set the key __default to the name of a default instance
__default: local
local:
    host: "%(host)s"
    port: "%(port)s"
"""

SUCCESS_MESSAGE = (
    "Ready to go! Type `gopublic` to get a list of commands you can execute."
)


@click.command("config_init")
@pass_context
def cli(ctx, url=None, api_key=None, admin=False, **kwds):
    """Help initialize global configuration (in home directory)
    """

    click.echo("""Welcome to Gopublic""")
    if os.path.exists(config.global_config_path()):
        info("Your gopublic configuration already exists. Please edit it instead: %s" % config.global_config_path())
        return 0

    while True:
        # Check environment
        host = click.prompt("Gopublish server host")
        port = click.prompt("Gopublish server port")

        info("Testing connection...")
        try:
            GopublishInstance(host=host, port=port)
            # We do a connection test during startup.
            info("Ok! Everything looks good.")
            break
        except Exception as e:
            warn("Error, we could not access the configuration data for your instance: %s", e)
            should_break = click.prompt("Continue despite inability to contact this instance? [y/n]")
            if should_break in ('Y', 'y'):
                break

    config_path = config.global_config_path()
    if os.path.exists(config_path):
        warn("File %s already exists, refusing to overwrite." % config_path)
        return -1

    with open(config_path, "w") as f:
        f.write(CONFIG_TEMPLATE % {
            'host': host,
            'port': port,
        })
        info(SUCCESS_MESSAGE)

    # We don't want other users to look into this file
    os.chmod(config_path, 0o600)
