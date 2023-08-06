import click
import logging
from bmlx.cli.runtime import component
from bmlx.cli.runtime import pipeline


@click.group()
def cli_group():
    logging.getLogger().setLevel(logging.INFO)
    logging.basicConfig(format="%(asctime)-7s %(message)s")


cli_group.add_command(component.run)
cli_group.add_command(pipeline.cleanup)


def main():
    cli_group()
