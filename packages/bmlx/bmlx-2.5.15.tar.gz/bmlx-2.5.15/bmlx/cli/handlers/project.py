import os
import pathlib
import sys
import logging
import json
import click
import socket
import tempfile
import zipfile
from datetime import datetime
from typing import Text, Optional
from bmlx.utils import io_utils, import_utils, package_utils
from bmlx.flow import Pipeline
from bmlx.context import BmlxContext
from bmlx.cli.constants import BMLX_CONFIG_FILE, BMLX_PIPELINE_ENTRY
from bmlx.cli.cli_exception import BmlxCliException
from bmlx.execution.bmlxflow.bmlxflow_runner import BmlxflowRunner
from bmlx.execution.runner import Runner
from bmlx.execution.multiprocess_runner import MultiProcessRunner
from bmlx import __version__
from bmlx.metadata import metadata
import bmlx.config as bmlx_config


def info(ctx: BmlxContext, detailed=False):
    click.echo(
        json.dumps(
            {
                "version": __version__,
                "bmlx-components version": package_utils.get_local_package_version(
                    "bmlx-components"
                ),
                "project_name": ctx.project.name,
                "entry": ctx.project.pipeline_path,
                "config_files": [
                    source.filename for source in ctx.project.configs.sources
                ],
            },
            indent=2,
        )
    )


def _upload_local_project(ctx: BmlxContext, pipeline: Pipeline) -> None:
    with ctx.project.packing() as (package, checksum):
        remote_uri = ctx.metadata.upload_package(
            pipeline_storage_path=ctx.pipeline_storage_base,
            local_path=package,
            checksum=checksum,
        )
        if not remote_uri:
            logging.warn("uploading package fail")
            return None

        pipeline.meta.uri = remote_uri
        logging.info("upload package success %s (%s)" % (package, checksum))

        ctx.package, ctx.checksum = package, checksum
        return remote_uri, ctx.package, ctx.checksum


def upload(
    ctx: BmlxContext,
    pipeline_name: Text,
    version: Text,
    user_name: Text,
    repo_url: Text,
    commit_id: Text,
    commit_msg: Text,
):
    assert version and user_name and commit_id and repo_url and pipeline_name

    bmlx_pipeline = import_utils.import_func_from_source(
        ctx.project.pipeline_path, "create_pipeline"
    )(ctx)

    # generate dag, settings, parameters of pipeline_version from pipeline.py and bmlx.yaml
    if ctx.engine == "bmlxflow":
        # create pipeline(if needed) to api-server
        resp = ctx.metadata.get_or_create_pipeline(
            name=pipeline_name,
            repo=repo_url,
            user_name=user_name,
            description=ctx.project.description,
            tags=ctx.project.tags,
        )

        try:
            BmlxflowRunner(ctx=ctx, pipeline=bmlx_pipeline).gen_workflow_spec(
                workflow_name=pipeline_name
            )
        except Exception as e:
            logging.warn(
                "BmlxflowRunner failed to generate workflow spec, error: %s", e
            )
            raise

        # upload to package store and get package_url
        remote_uri, _, checksum = _upload_local_project(
            ctx, bmlx_pipeline
        )  # will get checksum
        if not remote_uri:
            raise RuntimeError(
                "Failed to upload pipeline package to package-store"
            )

        #  create pipeline_version to api-server
        # may throw exception here
        resp = ctx.metadata.create_pipeline_version(
            pipeline_id=int(resp.id),
            version=version,
            committer=user_name,
            commit_id=commit_id,
            commit_msg=commit_msg,
            package_uri=remote_uri,
            package_checksum=checksum,
            dag=bmlx_pipeline.get_pipeline_dag(),
            parameters=ctx.project.configurables(),
        )
    click.echo(
        "Bmlx: upload pipeline %s/%s success, version: %s"
        % (ctx.project.namespace, ctx.project.name, ctx.checksum,)
    )


# download package from s3 store by pakcage_uri
def download(package_uri: Text, destination: Text):
    assert package_uri and destination
    package = package_uri.split("/")[-1]
    local_path = os.path.join(destination, package)
    metadata.Metadata._download_package(
        input_path=package_uri, output_path=local_path,
    )
    # with zipfile.ZipFile(
    #     os.path.join(tempdir, package + ".zip"), "r"
    # ) as zip_ref:
    #     zip_ref.extractall(local_dir)


def download_with_run_id(run_id: int, destination: str):
    """this is simply for debugging purpose"""
    md = metadata.Metadata(local_mode=False)

    exe = md.get_pipeline_execution_by_id(run_id)
    output_path = os.path.realpath(
        os.path.join(destination, f"pipeline-run-{run_id}.zip")
    )
    assert not os.path.exists(
        output_path
    ), f"{output_path} exists, please delete it and try again"

    exp = md.store.get_experiment_by_id(exe.experiment_id)
    logging.info(f"Downloading pipeline file from {exp.package_uri}")
    metadata.Metadata._download_package(
        input_path=exp.package_uri, output_path=output_path
    )
    logging.info(f"Pipeline file downloaded and saved as {output_path}")


def run(ctx: BmlxContext, execution_name: Text, execution_description: Text):
    """
    run 是一种轻量级的执行
    """
    pipeline = import_utils.import_func_from_source(
        ctx.project.pipeline_path, "create_pipeline"
    )(ctx)

    if ctx.local_mode:
        execution_name = (
            execution_name
            or f"{pipeline.meta.name}-{datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}"
        )
        runner = Runner(pipeline=pipeline, ctx=ctx)
        runner.run(
            execution_name=execution_name,
            execution_description=execution_description,
        )
    else:
        runner = BmlxflowRunner(ctx=ctx, pipeline=pipeline)
        try:
            runner.gen_workflow_spec(workflow_name=pipeline.meta.name)
        except Exception as e:
            logging.warn(
                "BmlxflowRunner failed to generate workflow spec, err: %s", e
            )
            raise

        remote_uri, _, checksum = _upload_local_project(ctx, pipeline)
        if not remote_uri:
            raise RuntimeError(
                "Failed to upload pipeline package to package-store"
            )
        # 创建 轻量级 experiment, 这条分支只会出现在 本地run 提交一个bmlx flow pipeline 到 argo workflow
        runner.run(
            package_uri=remote_uri,
            package_checksum=checksum,
            execution_description=execution_description,
        )
