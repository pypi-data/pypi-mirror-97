import sys
import click

from typing import Text, Optional, List, Dict, Any
from bmlx.execution.runner import Runner
from bmlx.cli.handlers.utils import format_time, list_action
from bmlx.utils.import_utils import import_func_from_source


def list(
    format: Text,
    page_size: int,
    page_token: str,
    filters: Optional[Dict[Text, Any]] = {},
    local_mode: bool = False,
    env: Optional[Text] = None,
):
    def _f(pipelines):
        return (
            ["id", "name", "ctime", "description", "repo", "owner",],
            [
                (
                    pipeline.id,
                    pipeline.name,
                    format_time(pipeline.create_time),
                    pipeline.description,
                    pipeline.repo,
                    pipeline.owner,
                )
                for pipeline in pipelines
            ],
        )

    list_action(
        resources="pipelines",
        tablulate_func=_f,
        format=format,
        page_size=page_size,
        page_token=page_token,
        filters=filters,
        local_mode=local_mode,
        env=env,
    )


def cleanup(ctx, execution_name, experiment_id, workflow_status):
    """
    clean up pipeline run
    """

    # find pipeline entry
    create_pipeline_func = import_func_from_source(
        ctx.project.pipeline_path, "create_pipeline"
    )
    pipeline = create_pipeline_func(ctx)

    runner = Runner(pipeline, ctx)
    ret = runner.cleanup(
        execution_name=execution_name,
        experiment_id=experiment_id,
        workflow_status=workflow_status,
    )
    click.echo("pipeline clean up result: %s" % ret)
