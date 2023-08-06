"""
runtime is internal entrance, user should never call this
"""
import click
import sys
import logging
from bmlx.cli.context import pass_bmlx_context
from bmlx.utils.import_utils import import_func_from_module
from bmlx.utils.var_utils import parse_vars

__remote_options = [
    click.option("--package"),
    click.option("--checksum"),
]


def bmlx_remote_project(f):
    for option in __remote_options:
        f = option(f)
    return f


"""
run component only, this is very useful in distributed environment
we only run one component in one distribute node
(so we do not provide any help informations :-) )
"""


@click.command()
@click.argument("component")
@click.option(
    "--execution_name", "-E", type=str, required=True,
)
@click.option("--experiment_id", type=str, required=True, default="")
@click.option(
    "--extra",
    "-T",  # similar as context.parameters, but this is only useful for component
    multiple=True,
    type=str,
)
@click.option(
    "--sub_component",
    type=bool,
    is_flag=True,
    default=False,
    help="run sub-componet or not",
)
@bmlx_remote_project
@pass_bmlx_context
def run(ctx, component, execution_name, experiment_id, extra, sub_component):
    # update plugin
    import_func_from_module("bmlx.cli.handlers.plugin", "update")(
        version=ctx.project.components_version
    )

    import_func_from_module("bmlx.cli.handlers.component", "run_component")(
        ctx=ctx,
        experiment_id=experiment_id,
        component_id=component,
        execution_name=execution_name,
        component_parameters=parse_vars(extra),
        sub_component=sub_component,
    )
