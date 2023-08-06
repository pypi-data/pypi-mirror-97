import click
from typing import Text
from bmlx.utils.import_utils import import_func_from_module
from bmlx.cli.context import pass_bmlx_context
from bmlx.context import BmlxContext


@click.command()
@pass_bmlx_context
def info(ctx):
    import_func_from_module("bmlx.cli.handlers.project", "info")(ctx)


@click.command()
@click.option(
    "--execution_name", "--en", type=str, default="", help="set execution name"
)
@click.option(
    "--execution_description",
    "--ed",
    type=str,
    default="",
    help="description of exection",
)
@pass_bmlx_context
def run(ctx: BmlxContext, execution_name: Text, execution_description: Text):
    # update plugin
    import_func_from_module("bmlx.cli.handlers.plugin", "update")(
        version=ctx.project.components_version
    )

    # run
    import_func_from_module("bmlx.cli.handlers.project", "run")(
        ctx,
        execution_name=execution_name,
        execution_description=execution_description,
    )


@click.command()
@pass_bmlx_context
@click.option("--pipeline_name", type=str, default="", help="pipeline name")
@click.option("--version", type=str, default="", help="pipeline version")
@click.option("--user_name", type=str, default="", help="gitlab user name")
@click.option("--repo_url", type=str, default="", help="gitlab repo url")
@click.option("--commit_id", type=str, default="", help="gitlab commit id")
@click.option("--commit_msg", type=str, default="", help="gitlab commit msg")
def upload(
    ctx: BmlxContext,
    pipeline_name: Text,
    version: Text,
    user_name: Text,
    repo_url: Text,
    commit_id: Text,
    commit_msg: Text,
):
    """
    in gitlab-cicd , use beflow command to create pipeline version to api-server
    bmlx upload --pipeline_name $CI_PROJECT_NAME --version $CI_COMMIT_TAG --user_name $GITLAB_USER_NAME
    --repo_url $CI_PROJECT_URL --commit_id $CI_COMMIT_SHA --commit_msg $CI_COMMIT_MESSAGE
    """
    # update plugin
    import_func_from_module("bmlx.cli.handlers.plugin", "update")(
        version=ctx.project.components_version
    )

    import_func_from_module("bmlx.cli.handlers.project", "upload")(
        ctx,
        pipeline_name=pipeline_name,
        version=version,
        user_name=user_name,
        repo_url=repo_url,
        commit_id=commit_id,
        commit_msg=commit_msg,
    )


@click.command()
@click.option(
    "--package_uri", "-p", default="", help='"name" field of bmlx.yml'
)
@click.option("--destination", "-d", default="./")
@click.option(
    "--run_id",
    "-r",
    default=None,
    help="if run id is provided, automatically resolve package and checksum",
)
def download(package_uri, destination, run_id):
    if run_id is not None:
        import_func_from_module(
            "bmlx.cli.handlers.project", "download_with_run_id"
        )(
            int(run_id), destination,
        )
    else:
        import_func_from_module("bmlx.cli.handlers.project", "download")(
            package_uri=package_uri, destination=destination
        )
