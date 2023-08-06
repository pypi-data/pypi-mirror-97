"""
DEFINE required flags of context, this is useful for multi entry project
"""
import click
import functools
import os
import tempfile
from contextlib import ExitStack
from bmlx.utils.var_utils import parse_vars
from bmlx.cli.constants import BMLX_CONFIG_FILE
from bmlx.context import BmlxContext

__context_options = [
    click.option("-n", "--namespace", help="default project namespace"),
    click.option(
        "-f",
        "--file",
        default=BMLX_CONFIG_FILE,
        type=str,
        help="configuration file of this run",
    ),
    click.option(
        "--entry",
        type=str,
        default="",
        help="bmlx entry pipeline file, bmlx will extract from bmlx.yml if 'entry' is not set",
    ),
    click.option(
        "-P",
        "--parameter",
        default=None,
        type=str,
        help="parameter",
        multiple=True,
    ),
    click.option(
        "--dry_run", default=False, is_flag=True, help="just dry run and test"
    ),
    click.option(
        "--local", default=False, is_flag=True, help="remote execution or not"
    ),
    click.option(
        "--env",
        type=str,
        default="prod",
        help="remote environment, prod or dev",
    ),
    click.option(
        "--skip_auth",
        type=bool,
        default=False,
        help="should skip auth or not",
    ),
    click.option(
        "--engine",
        type=click.Choice(["bmlxflow", "local"]),
        default="bmlxflow",
        help="if remote mode, ",
    ),
    click.option(
        "--pipeline_storage_base",
        type=str,
        default="",
        help="pipeline package storage base",
    ),
    click.option(
        "--package_uri",
        type=str,
        default="",
        help="pipeline package uri",
    ),
    click.option(
        "--workflow_id",
        type=str,
        default="",
        help="argo workflow id",
    ),
]


def pass_bmlx_context(f):
    @click.pass_obj
    def new_func(
        obj,
        pipeline_storage_base,
        engine,
        local,
        env,
        skip_auth,
        namespace,
        file,
        entry,
        parameter,
        dry_run,
        workflow_id,
        package_uri,
        **kwargs
    ):
        ctx = click.get_current_context()
        bmlx_ctx = ctx.ensure_object(BmlxContext)
        if not local:
            with ExitStack() as stack:
                package = None
                checksum = None
                if (
                    kwargs.get("package") is not None
                    and kwargs.get("checksum") is not None
                ):
                    package = kwargs["package"]
                    checksum = kwargs["checksum"]
                    tmp = stack.enter_context(
                        tempfile.TemporaryDirectory(prefix=package)
                    )
                    from bmlx.project_spec import Project

                    Project.load_from_remote(
                        pipeline_storage_base=pipeline_storage_base,
                        dst=tmp,
                        package=package,
                        checksum=checksum,
                        package_uri=package_uri,
                    )
                    os.chdir(tmp)

                bmlx_ctx.package = package
                bmlx_ctx.checksum = checksum

                if "package" in kwargs:
                    del kwargs["package"]
                if "checksum" in kwargs:
                    del kwargs["checksum"]
                bmlx_ctx.init(
                    namespace=namespace,
                    custom_config_file=file,
                    custom_entry_file=entry,
                    custom_parameters=parse_vars(parameter),
                    dry_run=dry_run,
                    local_mode=local,
                    env=env,
                    skip_auth=skip_auth,
                    engine=engine,
                    workflow_id=workflow_id,
                    package_uri=package_uri,
                )
                f(bmlx_ctx, **kwargs)
        else:
            if "package" in kwargs:
                bmlx_ctx.package = kwargs["package"]
                del kwargs["package"]
            if "checksum" in kwargs:
                bmlx_ctx.checksum = kwargs["checksum"]
                del kwargs["checksum"]

            bmlx_ctx.init(
                namespace=namespace,
                custom_config_file=file,
                custom_entry_file=entry,
                custom_parameters=parse_vars(parameter),
                dry_run=dry_run,
                local_mode=local,
                env=env,
                skip_auth=skip_auth,
                engine=engine,
                workflow_id=workflow_id,
                package_uri=package_uri,
            )

            f(bmlx_ctx, **kwargs)

    for option in __context_options:
        f = option(f)
    return functools.update_wrapper(new_func, f)
