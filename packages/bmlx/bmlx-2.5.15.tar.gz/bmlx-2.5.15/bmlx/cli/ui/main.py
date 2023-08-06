"""
bmlx cmdline handlers
"""
import click
import logging
import sys

import bmlx.cli.ui.project as project
from bmlx.utils.import_utils import import_func_from_module
from bmlx.utils.var_utils import parse_vars
from bmlx.cli.cli_exception import BmlxCliException


@click.group()
@click.option("--debug", "-D", is_flag=True, default=False)
@click.version_option()
def cli_group(debug):
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
        from http.client import HTTPConnection

        HTTPConnection.debuglevel = 1
    else:
        logging.getLogger().setLevel(logging.INFO)
    logging.basicConfig(format="%(asctime)-7s %(message)s")


@click.command()
@click.option(
    "--local", "-R", default=False, is_flag=True, help="use local metadata mode"
)
@click.option(
    "--env", default="prod", help="remote environment type, prod or dev",
)
@click.option("--page_size", default=10, help="max pipelines")
@click.option("--page_token", default="", help="pagination token")
@click.argument("resource", required=True)
@click.option(
    "-F", "--filter", default=None, type=str, help="filter", multiple=True,
)
@click.option(
    "-o",
    "format",
    type=click.Choice(["json", "yaml", ""]),
    help="output format",
)
def get(local, env, page_size, page_token, resource, filter, format):
    list_func = None
    try:
        list_func = import_func_from_module(
            "bmlx.cli.handlers.%s" % resource, "list"
        )
    except ImportError:
        try:
            if resource.endswith("s"):
                list_func = import_func_from_module(
                    "bmlx.cli.handlers.%s" % resource[:-1], "list"
                )
        except ImportError:
            pass
    if not list_func:
        click.echo("unsupported resource %s" % resource)
        sys.exit(-1)
    try:
        list_func(
            page_size=page_size,
            page_token=page_token,
            format=format,
            filters=parse_vars(filter),
            local_mode=local,
            env=env,
        )
    except Exception as e:
        logging.warning("Failed with exception %s when list %s", e, resource)
        sys.exit(-2)


@click.command()
@click.option(
    "--token",
    type=str,
    help="token, you could get token at http://www.mlp.bigo.inner/user-center or http://bmlx-ci.mlp.bigo.inner/profile",
)
@click.option("--user", type=str, help="Username (without email suffix)")
@click.option("--env", type=str, default="prod", help="env")
def login(user, token, env):
    if not user:
        user = click.prompt("Entering username", type=str)
    if not token:
        click.echo(
            "Hint: you could go {} get your token".format(
                "http://www.mlp.bigo.inner/profile"
                if env == "prod"
                else "http://bmlx-ci.mlp.bigo.inner/profile"
            )
        )
        # do not hide input to avoid user confusion on pasting token into terminal
        token = click.prompt("Entreing token", type=str, hide_input=False)

    import_func_from_module("bmlx.cli.handlers.login", "login")(
        user, token, env
    )


@click.command()
@click.argument("version", default="")
def update(version):
    import_func_from_module("bmlx.cli.handlers.plugin", "update")(
        version=version
    )


@click.command()
@click.option("--tf", help="tensorflow graph", required=True)
@click.option("--xdl", help="xdl graph", required=True)
def convert(tf, xdl):
    import_func_from_module("bmlx.cli.handlers.graph", "convert")(
        tf=tf, xdl=xdl
    )


cli_group.add_command(project.upload)
cli_group.add_command(project.run)
cli_group.add_command(project.download)
cli_group.add_command(update)
cli_group.add_command(get)
cli_group.add_command(login)
cli_group.add_command(convert)


def main():
    try:
        cli_group()
    except BmlxCliException as e:
        click.echo(e, err=True)
        sys.exit(-10)
    except Exception:
        logging.exception("unknown error happens")
        sys.exit(-11)


if __name__ == "__main__":
    main()
