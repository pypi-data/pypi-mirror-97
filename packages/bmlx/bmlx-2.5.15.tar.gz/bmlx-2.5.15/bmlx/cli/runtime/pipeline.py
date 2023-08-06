"""
runtime is internal entrance, user should never call this
"""
import click
from bmlx.cli.context import pass_bmlx_context
from bmlx.utils.import_utils import import_func_from_module

__remote_options = [
    click.option("--package"),
    click.option("--checksum"),
]


def bmlx_remote_project(f):
    for option in __remote_options:
        f = option(f)
    return f


"""
clean up all components in a workflow
"""


@click.command()
@click.option(
    "--execution_name", "-E", type=str, required=True,
)
@click.option(
    "--experiment_id", type=str, required=True,
)
@click.option(
    "--workflow_status", type=str, required=True,
)
@bmlx_remote_project
@pass_bmlx_context
def cleanup(ctx, execution_name, experiment_id, workflow_status):
    # update plugin
    import_func_from_module("bmlx.cli.handlers.plugin", "update")(
        version=ctx.project.components_version
    )

    import_func_from_module("bmlx.cli.handlers.pipeline", "cleanup")(
        ctx=ctx,
        execution_name=execution_name,
        experiment_id=experiment_id,
        workflow_status=workflow_status,
    )
