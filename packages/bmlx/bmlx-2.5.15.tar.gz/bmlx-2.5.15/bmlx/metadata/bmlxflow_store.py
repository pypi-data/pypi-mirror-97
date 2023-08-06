"""
bmlx api-server wrapper
"""

import os
import logging
import urllib
import requests
import json
import time
import datetime
import itertools
import bmlx_openapi_client
from bmlx_openapi_client.exceptions import ApiException as ApiException
import pathlib
import google.protobuf.descriptor as descriptor
from bmlx import flow

from google.protobuf.message import Message
from typing import Text, List, Optional, Tuple, Dict, Any
from pytz import timezone
from bmlx.bmlx_ini import BmlxINI  # TODO add global varaibe
from bmlx.utils import io_utils, proc_utils
from bmlx.proto.metadata import (
    execution_pb2,
    artifact_pb2,
    pipeline_pb2,
    experiment_pb2,
)

BMLX_API_HOST = "www.mlp.bigo.inner"
BMLX_API_PORT = 80

BMLX_DEV_API_HOST = "bmlx-ci.mlp.bigo.inner"
BMLX_DEV_API_PORT = 80

QUICK_TEST_API_HOST = "103.97.83.75"
QUICK_TEST_API_PORT = 8080

_TIMEOUT = 10

# 用于创建临时的experiment 和 run的实验
PUBLIC_TEST_RESOURCE_GROUP = "PublicTest"


def get_api_endpoint(env: Optional[Text] = "prod"):
    if (
        "BMLX_API_SERVICE_HOST" in os.environ
        and "BMLX_API_SERVICE_PORT" in os.environ
    ):
        return "http://{}:{}/api/v1".format(
            os.environ["BMLX_API_SERVICE_HOST"],
            os.environ["BMLX_API_SERVICE_PORT"],
        )
    elif env == "prod":
        return f"http://{BMLX_API_HOST}:{BMLX_API_PORT}/api/v1"
    elif env == "dev":
        return f"http://{BMLX_DEV_API_HOST}:{BMLX_DEV_API_PORT}/api/v1"
    elif env == "quick_test":
        return f"http://{QUICK_TEST_API_HOST}:{QUICK_TEST_API_PORT}/api/v1"
    else:
        raise ValueError("Invalid env %s" % env)


def _retry_handler(f):
    return proc_utils.retry(
        retry_count=3,
        delay=5,
        allowed_exceptions=(ApiException),
    )(f)


class BmlxflowStore(object):
    def __init__(self, api_endpoint=None, env="prod", skip_auth=False):
        if not api_endpoint:
            api_endpoint = get_api_endpoint(env)

        self._setup_client(api_endpoint, env, skip_auth)

    def _setup_client(self, api_endpoint: Text, env: Text, skip_auth: bool):
        configuration = bmlx_openapi_client.Configuration(api_endpoint)
        if skip_auth:
            configuration.api_key = {
                "X-Auth-User": "bmlx-client",
                "X-Auth-Token": "great-bmlx",
            }
        else:
            ini = BmlxINI(env)
            if not ini.user and not ini.token:
                logging.error(
                    "Please execute `bmlx login` to login meta server using token"
                )
                raise RuntimeError("login required")
            configuration.api_key = {
                "X-Auth-User": ini.user,
                "X-Auth-Token": ini.token,
            }

        self.api_client = bmlx_openapi_client.ApiClient(configuration)
        self.pipeline_api = bmlx_openapi_client.PipelineApi(self.api_client)
        self.pipeline_version_api = bmlx_openapi_client.PipelineVersionApi(
            self.api_client
        )
        self.experiment_api = bmlx_openapi_client.ExperimentApi(self.api_client)
        self.experiment_run_api = bmlx_openapi_client.ExperimentRunApi(
            self.api_client
        )
        self.artifact_api = bmlx_openapi_client.ArtifactApi(self.api_client)
        self.component_run_api = bmlx_openapi_client.ComponentRunApi(
            self.api_client
        )
        self.execution_event_api = bmlx_openapi_client.ExecutionEventApi(
            self.api_client
        )

    class FilterCondition(object):
        __slots__ = ["operator", "field", "value"]

        def __init__(self, field, operator, value):
            self.field = field
            self.operator = operator
            self.value = value

        def __dict__(self):
            return {
                "field": self.field,
                "operator": self.operator,
                "value": self.value,
            }

    def gen_api_filters(self, conds: List[FilterCondition]):
        conditions = []
        for c in conds:
            conditions.append(c.__dict__())
        return json.dumps({"conditions": conditions})

    def get_or_create_pipeline(
        self,
        name: Text = "",
        repo: Text = "",
        user_name: Text = "",
        description: Text = "",
        tags: List[Text] = [],
    ) -> pipeline_pb2.Pipeline:
        filter_expression = self.gen_api_filters(
            [
                BmlxflowStore.FilterCondition(
                    field="repo", operator="=", value=repo
                )
            ]
        )
        resp = self.pipeline_api.get_pipelines(
            page_size=1, filter=filter_expression
        )
        # tags 可能会变化
        if len(resp.pipelines) > 0:
            p = resp.pipelines[0]
            p.tags = p.tags or []
            if len(p.tags) != len(tags) or [t for t in tags if t not in p.tags]:
                p.tags = tags
                p.description = description
                p.user_name = user_name
                p = self.pipeline_api.update_pipeline(id=p.id, pipeline=p)
            return pipeline_api2pb(p)
        try:
            resp = self.pipeline_api.create_pipeline(
                pipeline=bmlx_openapi_client.Pipeline(
                    name=name,
                    repo=repo,
                    owner=user_name,
                    description=description,
                    tags=tags,
                )
            )
            return pipeline_api2pb(resp)
        except ApiException as e:
            logging.warn("Failed to create pipeline, error: %s", e)
            raise

    def get_pipeline_execution_by_id(
        self, pipeline_execution_id: int
    ) -> execution_pb2.Execution:
        run = self.experiment_run_api.get_experiment_run_by_id(
            id=pipeline_execution_id
        )
        if not run:
            raise RuntimeError(
                "Failed to get experiment run by id " % pipeline_execution_id
            )
        exp = self.get_experiment_by_id(run.experiment_id)
        return experiment_run_api2pb(run, exp)

    def create_pipeline_version(
        self,
        pipeline_id: int,
        version: Text,
        committer: Text = "",
        commit_id: Text = "",
        commit_msg: Text = "",
        package_uri: Text = "",
        package_checksum: Text = "",
        dag=[],
        parameters=[],
    ) -> pipeline_pb2.PipelineVersion:
        # 将传给服务器的参数构造成  parameter_config的结构
        """
        type ParameterConfig struct {
            Description string             `json:"description"`
            Required    bool               `json:"required"`
            Default     string             `json:"default"`
            Validator   ParameterValidator `json:"validator"`
        }
        """

        def gen_parameter_config(key, value):
            if isinstance(value, dict):
                value["default"] = str(value["value"])
                del value["value"]
                if "validator" in value:
                    if not value["validator"].get("name"):
                        raise ValueError("Invalid validator, name missing")

                    validator_new = {
                        "name": value["validator"]["name"],
                        "parameters": {},
                    }
                    for k, v in value["validator"].items():
                        if k != "name":
                            validator_new["parameters"][k] = json.dumps(v)
                    value["validator"] = validator_new
                value["name"] = key
                return value
            else:
                return {
                    "name": key,
                    "default": str(value),
                    "required": False if value is None or value == "" else True,
                    "scope": "Experiment",
                }

        try:
            parameter_configs = [
                gen_parameter_config(k, v) for (k, v) in parameters
            ]
            resp = self.pipeline_version_api.create_pipeline_version(
                pipeline_version=bmlx_openapi_client.PipelineVersion(
                    pipeline_id=pipeline_id,
                    name=version,
                    commit_id=commit_id,
                    commit_msg=commit_msg,
                    committer=committer,
                    package_uri=package_uri,
                    package_checksum=package_checksum,
                    dag=dag,
                    parameters=parameter_configs,
                    owner=committer,
                )
            )
            return pipeline_version_api2pb(resp)
        except ApiException as e:
            logging.warn(
                "Failed to create pipeline version with exception: %s", e
            )
            # if (
            #     json.loads(e.body)["error"]
            #     == "UNIQUE constraint failed: pipeline_versions.name, pipeline_versions.commit_id"
            # ):
            #     logging.warn(
            #         "pipeline version with commit_id %s and version %s has already been created!",
            #         commit_id,
            #         version,
            #     )
            #     return
            # else:
            raise

    @_retry_handler
    def create_light_weight_experiment(
        self,
        name: Text,
        package_uri: Text,
        package_checksum: Text = "",
        dag=[],
        parameters={},
    ) -> experiment_pb2.Experiment:
        # pipeline version id = -1，表示不需要通过 pipeline version 去创建 experiment，而是直接使用 package uri
        # 使用 resource_group 为 LightWeighted 用来使用公共资源运行experiment和关联的experiment run
        try:
            exp = self.experiment_api.create_experiment(
                experiment=bmlx_openapi_client.Experiment(
                    name=name,
                    package_uri=package_uri,
                    package_checksum=package_checksum,
                    pipeline_version_id=-1,
                    status="Activated",
                    trigger_type="Manual-Trigger",
                    trigger_instantly=True,
                    resource_group=PUBLIC_TEST_RESOURCE_GROUP,
                    dag=dag,
                    parameters=parameters,
                )
            )
            return experiment_api2pb(exp)
        except ApiException as e:
            logging.warn(
                "Failed to create experiment with name: %s, package uri: %s, exception: %s",
                name,
                package_uri,
                e,
            )
            raise

    def get_experiment_by_name(self, name: Text) -> experiment_pb2.Experiment:
        filter_expression = self.gen_api_filters(
            [
                BmlxflowStore.FilterCondition(
                    field="name", operator="=", value=name
                )
            ]
        )
        resp = self.experiment_api.get_experiments(
            page_size=1, filter=filter_expression
        )
        if len(resp.experiments) == 0:
            return None
        else:
            return resp.experiments[0]

    @_retry_handler
    def get_experiment_by_id(
        self, exp_id: int
    ) -> bmlx_openapi_client.Experiment:
        resp = self.experiment_api.get_experiment_by_id(exp_id)
        return resp

    def get_artifact_by_uri(self, uri: Text) -> artifact_pb2.Artifact:
        filter_expression = self.gen_api_filters(
            [
                BmlxflowStore.FilterCondition(
                    field="uri", operator="=", value=uri
                )
            ]
        )
        resp = self.artifact_api.get_artifacts(
            page_size=1, filter=filter_expression
        )
        if len(resp.artifacts):
            return artifact_api2pb(resp.artifacts[0])
        return None

    def create_artifact(
        self, ar: artifact_pb2.Artifact
    ) -> artifact_pb2.Artifact:
        artifact = artifact_pb2api(ar)
        ret = self.artifact_api.create_artifact(artifact=artifact)
        if not ret:
            raise RuntimeError(
                "Failed to create artifact using data %s", artifact
            )
        return artifact_api2pb(ret)

    def create_component_execution(
        self,
        pipeline_execution: execution_pb2.Execution,
        component_execution: execution_pb2.ComponentExecution,
        pipeline_name: Optional[Text] = None,
    ) -> Tuple[
        execution_pb2.Execution,
        List[artifact_pb2.Artifact],
        List[artifact_pb2.Artifact],
    ]:
        # create component run
        component_execution.context_id = pipeline_execution.id
        run = self.component_run_api.create_component_run(
            component_run=component_run_pb2api(component_execution)
        )
        return (component_run_api2pb(run), [], [])

    def update_component_execution(
        self,
        pipeline_execution: execution_pb2.Execution,
        component_execution: execution_pb2.ComponentExecution,
        pipeline_name: Optional[Text] = None,
        input_artifacts: Optional[List[artifact_pb2.Artifact]] = [],
        output_artifacts: Optional[List[artifact_pb2.Artifact]] = [],
        exec_properties: Dict[Text, Any] = {},
    ) -> Tuple[
        execution_pb2.Execution,
        List[artifact_pb2.Artifact],
        List[artifact_pb2.Artifact],
    ]:
        run = component_run_pb2api(component_execution)
        # input artifacts are all created already
        for ar in input_artifacts:
            artifact = self.get_artifact_by_uri(ar.uri)
            if not artifact:
                continue
                raise RuntimeError("Failed to get artifact by uri: %s" % ar.uri)
            # create execution event
            event = self.execution_event_api.create_execution_event(
                execution_event=bmlx_openapi_client.ExecutionEvent(
                    component_run_id=run.id,
                    artifact_id=artifact.id,
                    event_type="consume",
                )
            )
            if not event:
                raise RuntimeError("Failed to create execution event")

        # create output artifacts
        for ar in output_artifacts:
            self.create_artifact(ar)

        self.component_run_api.update_component_run(
            id=run.id, component_run=run
        )
        final_run = self.component_run_api.get_component_run_by_id(run.id)
        return (
            component_run_api2pb(final_run),
            [artifact_api2pb(ar) for ar in final_run.inputs or []],
            [artifact_api2pb(ar) for ar in final_run.outputs or []],
        )

    def update_component_execution_run_context(
        self,
        component_execution: execution_pb2.ComponentExecution,
        run_context: Dict[Text, Text] = {},
    ):
        for k, v in run_context.items():
            component_execution.run_context[k] = v
        run = component_run_pb2api(component_execution)
        self.component_run_api.update_component_run(
            id=run.id, component_run=run
        )

    @_retry_handler
    def create_or_update_component_execution(
        self,
        pipeline_execution: execution_pb2.Execution,
        component_execution: execution_pb2.ComponentExecution,
        input_artifacts: Optional[List[artifact_pb2.Artifact]] = [],
        output_artifacts: Optional[List[artifact_pb2.Artifact]] = [],
        exec_properties: Dict[Text, Any] = {},
        pipeline_name: Optional[Text] = None,
    ) -> Tuple[
        execution_pb2.Execution,
        List[artifact_pb2.Artifact],
        List[artifact_pb2.Artifact],
    ]:
        if not pipeline_execution.id:
            raise RuntimeError("pipeline exectuion id invalid")
        filter_expression = self.gen_api_filters(
            [
                BmlxflowStore.FilterCondition(
                    field="experiment_run_id",
                    operator="=",
                    value=pipeline_execution.id,
                ),
                BmlxflowStore.FilterCondition(
                    field="component",
                    operator="=",
                    value=component_execution.type,
                ),
            ]
        )
        resp = self.component_run_api.get_component_runs(
            page_size=1, filter=filter_expression
        )
        if len(resp.component_runs) == 0:
            return self.create_component_execution(
                pipeline_execution,
                component_execution,
                pipeline_name,
            )
        else:
            component_execution.id = resp.component_runs[0].id
            # 注意这里的 component_run.run_context
            for k in resp.component_runs[0].run_context or {}:
                component_execution.run_context[k] = resp.component_runs[
                    0
                ].run_context[k]
            return self.update_component_execution(
                pipeline_execution,
                component_execution,
                pipeline_name,
                input_artifacts,
                output_artifacts,
                exec_properties,
            )

    def get_component_runs_by_experiment_run_id(self, experiment_run_id: int):
        filter_expression = self.gen_api_filters(
            [
                BmlxflowStore.FilterCondition(
                    field="experiment_run_id",
                    operator="=",
                    value=experiment_run_id,
                )
            ]
        )
        # should not exceed 20 components in an experiment run
        resp = self.component_run_api.get_component_runs(
            page_size=20, filter=filter_expression
        )
        return resp.component_runs

    @_retry_handler
    def get_previous_artifacts(
        self, pipeline_execution: execution_pb2.Execution
    ) -> Dict[Text, List[artifact_pb2.Artifact]]:
        filter_expression = self.gen_api_filters(
            [
                BmlxflowStore.FilterCondition(
                    field="experiment_run_id",
                    operator="=",
                    value=pipeline_execution.id,
                )
            ]
        )
        # should not exceed 100 artifacts in an experiment run
        resp = self.artifact_api.get_artifacts(
            page_size=100, filter=filter_expression
        )
        ret = {}
        for artifact in resp.artifacts:
            if artifact.producer_component not in ret:
                ret[artifact.producer_component] = []
            ret[artifact.producer_component].append(artifact_api2pb(artifact))
        return ret

    @_retry_handler
    def get_component_executions_of_pipeline(
        self, pipeline_execution: execution_pb2.Execution
    ) -> List[execution_pb2.ComponentExecution]:
        if not pipeline_execution.id:
            raise RuntimeError("unknown pipeline execution")

        return [
            component_run_api2pb(o)
            for o in self.get_component_runs_by_experiment_run_id(
                pipeline_execution.id
            )
        ]

    @_retry_handler
    def get_component_execution(
        self,
        pipeline_execution: execution_pb2.Execution,
        component_id: Text,
    ) -> execution_pb2.ComponentExecution:
        if not pipeline_execution.id:
            raise RuntimeError("unknown pipeline execution")
        filter_expression = self.gen_api_filters(
            [
                BmlxflowStore.FilterCondition(
                    field="experiment_run_id",
                    operator="=",
                    value=pipeline_execution.id,
                ),
                BmlxflowStore.FilterCondition(
                    field="component",
                    operator="=",
                    value=component_id,
                ),
            ]
        )
        resp = self.component_run_api.get_component_runs(
            page_size=1, filter=filter_expression
        )
        if resp.component_runs:
            return component_run_api2pb(resp.component_runs[0])
        else:
            return None

    @_retry_handler
    def get_or_create_pipeline_execution(
        self, execution: execution_pb2.Execution
    ) -> execution_pb2.Execution:
        # get experiment run by experiment_run_name, experiment run name is unique
        if not execution.experiment_id:
            raise RuntimeError(
                "Invalid experiment id, execution: %s" % execution
            )
        run = self.get_experiment_run(
            int(execution.experiment_id), execution.name
        )
        if run:
            logging.info(
                "already created pipeline execution id(experiment run id): %d"
                % run.id
            )
            if run.status == "NotStarted":
                run.status = "Running"
                run.start_time = int(time.time())
                self.experiment_run_api.update_experiment_run(
                    id=run.id, experiment_run=run
                )
        else:
            execution.state = execution_pb2.State.RUNNING
            execution.start_time = int(time.time())
            run = self.create_experiment_run(execution)
        exp = self.get_experiment_by_id(run.experiment_id)
        return experiment_run_api2pb(run, exp)

    @_retry_handler
    def update_pipeline_execution(
        self, execution: execution_pb2.Execution
    ) -> bool:
        run = self.experiment_run_api.get_experiment_run_by_id(id=execution.id)
        if not run:
            raise RuntimeError(
                "Failed to get experiment run by execution ", execution
            )
        updated_run = experiment_run_pb2api(execution)
        run.end_time = updated_run.end_time
        run.status = updated_run.status
        try:
            self.experiment_run_api.update_experiment_run(
                id=execution.id, experiment_run=run
            )
            return True
        except Exception as e:
            logging.warn(
                "Failed to update experiment run by id %d, error: %s",
                execution.id,
                e,
            )
            return False

    def get_experiment_run(
        self, experiment_id: int, name: Text
    ) -> bmlx_openapi_client.ExperimentRun:
        filter_expression = self.gen_api_filters(
            [
                BmlxflowStore.FilterCondition(
                    field="name", operator="=", value=name
                ),
                BmlxflowStore.FilterCondition(
                    field="experiment_id", operator="=", value=experiment_id
                ),
            ]
        )
        resp = self.experiment_run_api.get_experiment_runs(
            page_size=1, filter=filter_expression
        )
        if len(resp.experiment_runs) == 0:
            return None
        else:
            return resp.experiment_runs[0]

    def create_experiment_run(
        self, execution: execution_pb2.Execution
    ) -> bmlx_openapi_client.ExperimentRun:
        try:
            run = experiment_run_pb2api(execution)
            run = self.experiment_run_api.create_experiment_run(
                experiment_run=run
            )
            logging.info(
                "created experiment run, name: %s, id : %d", run.name, run.id
            )
        except ApiException as e:
            if (
                json.loads(e.body)["error"]
                == "UNIQUE constraint failed: experiment_runs.name, experiment_runs.experiment_id"
            ):
                logging.warn(
                    "experiment run with name %s and experiment_id %d has already been created, created with id %d!",
                    run.name,
                    run.experiment_id,
                    run.id,
                )
                run = self.get_experiment_run(
                    execution.experiment_id, execution.name
                )
            else:
                raise
        return run

    def get_artifacts(
        self, page_size, page_token, filters
    ) -> Tuple[List[pipeline_pb2.Pipeline], Text]:
        def convert_filter(k, v):
            if k in ("id", "uri", "producer_component", "type"):
                return k, v
            elif k == "state":
                return (
                    "status",
                    artifact_status_pb2api(
                        artifact_pb2.Artifact.State.Value(v)
                    ),
                )
            elif k == "execution_id":
                return "experiment_run_id", v
            else:
                raise ValueError("Filter key %s is not supported now" % k)

        filter_expression = self.gen_api_filters(
            [
                BmlxflowStore.FilterCondition(
                    field=convert_filter(k, v)[0],
                    operator="=",
                    value=convert_filter(k, v)[1],
                )
                for k, v in filters.items()
            ]
        )
        resp = self.artifact_api.get_artifacts(
            page_size=page_size, page_token=page_token, filter=filter_expression
        )
        return (
            [artifact_api2pb(ar) for ar in resp.artifacts],
            resp.next_page_token,
        )

    def get_pipelines(
        self, page_size, page_token, filters
    ) -> Tuple[List[pipeline_pb2.Pipeline], Text]:
        def convert_filter(k, v):
            if k in ("id", "name", "repo", "owner"):
                return k, v
            else:
                raise ValueError("Filter key %s is not supported now" % k)

        filter_expression = self.gen_api_filters(
            [
                BmlxflowStore.FilterCondition(
                    field=convert_filter(k, v)[0],
                    operator="=",
                    value=convert_filter(k, v)[1],
                )
                for k, v in filters.items()
            ]
        )
        resp = self.pipeline_api.get_pipelines(
            page_size=page_size, page_token=page_token, filter=filter_expression
        )
        return (
            [pipeline_api2pb(ar) for ar in resp.pipelines],
            resp.next_page_token,
        )

    def get_pipeline_versions(
        self, page_size, page_token, filters
    ) -> Tuple[List[pipeline_pb2.PipelineVersion], Text]:
        def convert_filter(k, v):
            if k in (
                "id",
                "name",
                "commit_id",
                "commit_msg",
                "committer",
                "pipeline_id",
                "pipeline_name",
                "package_uri",
            ):
                return k, v
            else:
                raise ValueError("Filter key %s is not supported now" % k)

        filter_expression = self.gen_api_filters(
            [
                BmlxflowStore.FilterCondition(
                    field=convert_filter(k, v)[0],
                    operator="=",
                    value=convert_filter(k, v)[1],
                )
                for k, v in filters.items()
            ]
        )
        resp = self.pipeline_version_api.get_pipeline_versions(
            page_size=page_size, page_token=page_token, filter=filter_expression
        )
        return (
            [pipeline_version_api2pb(ar) for ar in resp.pipeline_versions],
            resp.next_page_token,
        )

    def get_pipeline_executions(
        self, page_size, page_token, filters
    ) -> Tuple[List[execution_pb2.Execution], Text]:
        def convert_filter(k, v):
            if k in ("id", "experiment_id", "resource_group"):
                return k, v
            elif k == "status":
                return (
                    "status",
                    execution_status_pb2api(execution_pb2.State.Value(v)),
                )
            elif k == "run_name":
                return "name", v
            else:
                raise ValueError("Filter key %s is not supported now" % k)

        filter_expression = self.gen_api_filters(
            [
                BmlxflowStore.FilterCondition(
                    field=convert_filter(k, v)[0],
                    operator="=",
                    value=convert_filter(k, v)[1],
                )
                for k, v in filters.items()
            ]
        )
        resp = self.experiment_run_api.get_experiment_runs(
            page_size=page_size, page_token=page_token, filter=filter_expression
        )
        return (
            [experiment_run_api2pb(ar) for ar in resp.experiment_runs],
            resp.next_page_token,
        )

    def get_component_executions(
        self, page_size, page_token, filters
    ) -> Tuple[List[execution_pb2.ComponentExecution], Text]:
        def convert_filter(k, v):
            if k in ("id"):
                return k, v
            elif k == "status":
                return (
                    "status",
                    execution_status_pb2api(execution_pb2.State.Value(v)),
                )
            elif k == "pipeline_execution_id":
                return "experiment_run_id", v
            elif k == "type":
                return "component", v
            else:
                raise ValueError("Filter key %s is not supported now" % k)

        filter_expression = self.gen_api_filters(
            [
                BmlxflowStore.FilterCondition(
                    field=convert_filter(k, v)[0],
                    operator="=",
                    value=convert_filter(k, v)[1],
                )
                for k, v in filters.items()
            ]
        )
        resp = self.component_run_api.get_component_runs(
            page_size=page_size, page_token=page_token, filter=filter_expression
        )
        return (
            [component_run_api2pb(ar) for ar in resp.component_runs],
            resp.next_page_token,
        )

    def get_experiments(
        self, page_size, page_token, filters
    ) -> Tuple[List[experiment_pb2.Experiment], Text]:
        filter_expression = self.gen_api_filters(
            [
                BmlxflowStore.FilterCondition(field=k, operator="=", value=v)
                for k, v in filters.items()
            ]
        )
        resp = self.experiment_api.get_experiments(
            page_size=page_size, page_token=page_token, filter=filter_expression
        )
        return (
            [experiment_api2pb(ar) for ar in resp.experiments],
            resp.next_page_token,
        )


def execution_status_api2pb(st: str):
    status_map = {
        "NotStarted": execution_pb2.State.NOT_STARTED,
        "Running": execution_pb2.State.RUNNING,
        "Succeeded": execution_pb2.State.SUCCEEDED,
        "Failed": execution_pb2.State.FAILED,
        "Cached": execution_pb2.State.CACHED,
        "Canceled": execution_pb2.State.CANCELED,
        "Terminated": execution_pb2.State.TERMINATED,
        "Pending": execution_pb2.State.PENDING,
        "Error": execution_pb2.State.ERROR,
        "Skipped": execution_pb2.State.SKIPPED,
    }
    return status_map.get(st, execution_pb2.State.UNKNOWN)


def execution_status_pb2api(st):
    status_map = {
        execution_pb2.State.NOT_STARTED: "NotStarted",
        execution_pb2.State.RUNNING: "Running",
        execution_pb2.State.SUCCEEDED: "Succeeded",
        execution_pb2.State.FAILED: "Failed",
        execution_pb2.State.CACHED: "Cached",
        execution_pb2.State.CANCELED: "Canceled",
        execution_pb2.State.TERMINATED: "Terminated",
        execution_pb2.State.PENDING: "Pending",
        execution_pb2.State.ERROR: "Error",
        execution_pb2.State.SKIPPED: "Skipped",
    }
    return status_map.get(st, "Unknown")


def artifact_status_pb2api(st):
    status_map = {
        artifact_pb2.Artifact.State.UNKNOWN: "Unknown",
        artifact_pb2.Artifact.State.PENDING: "Pending",
        artifact_pb2.Artifact.State.LIVE: "Live",
        artifact_pb2.Artifact.State.MARKED_FOR_DELETION: "MarkedForDeletion",
        artifact_pb2.Artifact.State.DELETED: "Deleted",
    }
    return status_map.get(st)


def artifact_status_api2pb(st):
    status_map = {
        "Unknown": artifact_pb2.Artifact.State.UNKNOWN,
        "Pending": artifact_pb2.Artifact.State.PENDING,
        "Live": artifact_pb2.Artifact.State.LIVE,
        "MarkedForDeletion": artifact_pb2.Artifact.State.MARKED_FOR_DELETION,
        "Deleted": artifact_pb2.Artifact.State.DELETED,
    }
    return status_map.get(st)


def artifact_pb2api(ar: artifact_pb2.Artifact) -> bmlx_openapi_client.Artifact:
    artifact = bmlx_openapi_client.Artifact(
        status=artifact_status_pb2api(ar.state),
        uri=ar.uri,
        experiment_run_id=int(ar.execution_id),
        producer_component=ar.producer_component,
        type=ar.type,
        name=ar.name,
        import_only=ar.import_only,
        description=ar.description,
    )
    return artifact


def artifact_api2pb(ar: bmlx_openapi_client.Artifact) -> artifact_pb2.Artifact:
    artifact = artifact_pb2.Artifact(
        id=ar.id,
        state=artifact_status_api2pb(ar.status),
        uri=ar.uri,
        execution_id=str(ar.experiment_run_id),
        create_time=ar.create_time,
        producer_component=ar.producer_component,
        type=ar.type,
        name=ar.name,
        import_only=ar.import_only,
        description=ar.description,
    )
    return artifact


def component_run_pb2api(
    execution: execution_pb2.ComponentExecution,
) -> bmlx_openapi_client.ComponentRun:
    def add_pod_info(run):
        run.run_context["argo_node"] = os.environ.get(
            "ARGO_POD_NAME",
            "something is wrong, find bmlx maintainers for help",
        )

    run = bmlx_openapi_client.ComponentRun(
        id=execution.id,
        experiment_run_id=execution.context_id,
        component=execution.type,
        start_time=execution.start_time,
        end_time=execution.finish_time,
        status=execution_status_pb2api(execution.state),
    )
    run.run_context = {}
    for k in execution.run_context or {}:
        run.run_context[k] = execution.run_context[k]

    add_pod_info(run)
    return run


def component_run_api2pb(
    run: bmlx_openapi_client.ComponentRun,
) -> execution_pb2.ComponentExecution:
    execution = execution_pb2.ComponentExecution()
    execution.id = run.id
    execution.start_time = run.start_time
    execution.finish_time = run.end_time
    execution.type = run.component
    execution.context_id = int(run.experiment_run_id)
    execution.state = execution_status_api2pb(run.status)
    # run_context
    for k in run.run_context or {}:
        execution.run_context[k] = run.run_context[k]
    return execution


def experiment_run_pb2api(
    execution: execution_pb2.Execution,
) -> bmlx_openapi_client.ExperimentRun:
    run = bmlx_openapi_client.ExperimentRun(
        name=execution.name,
        experiment_id=int(execution.experiment_id),
        start_time=execution.start_time,
        scheduled_time=execution.schedule_time,
        end_time=execution.finish_time,
        status=execution_status_pb2api(execution.state),
    )
    run.run_context = bmlx_openapi_client.RunContext(
        workflow_name=execution.run_context["workflow_name"],
        workflow_namespace=execution.run_context["workflow_namespace"],
    )
    return run


def experiment_run_api2pb(
    run: bmlx_openapi_client.ExperimentRun,
    exp: bmlx_openapi_client.Experiment = None,
) -> execution_pb2.Execution:
    execution = execution_pb2.Execution()
    execution.id = run.id
    execution.context_id = run.experiment_id
    execution.name = run.name
    execution.create_time = run.create_time
    execution.schedule_time = run.scheduled_time or run.create_time
    execution.start_time = run.start_time
    execution.finish_time = run.end_time
    execution.experiment_id = str(run.experiment_id)
    execution.state = execution_status_api2pb(run.status)
    # get experiment info by exp id
    if exp:
        execution.deployment_running = exp.deployment_running

    execution.run_context["workflow_name"] = run.run_context.workflow_name or ""
    execution.run_context["workflow_namespace"] = (
        run.run_context.workflow_namespace or ""
    )

    return execution


def pipeline_api2pb(
    p: bmlx_openapi_client.Pipeline,
) -> pipeline_pb2.Pipeline:
    ret = pipeline_pb2.Pipeline(
        id=str(p.id),
        name=p.name,
        create_time=p.create_time,
        description=p.description,
        repo=p.repo,
        owner=p.owner,
        tags=p.tags,
    )
    return ret


def pipeline_version_api2pb(
    p: bmlx_openapi_client.PipelineVersion,
) -> pipeline_pb2.PipelineVersion:
    ret = pipeline_pb2.PipelineVersion(
        id=str(p.id), name=p.name, create_time=p.create_time
    )
    ret.commit_id = p.commit_id
    ret.commit_msg = p.commit_msg
    ret.committer = p.committer
    ret.pipeline_id = str(p.pipeline_id)
    ret.pipeline_name = p.pipeline_name
    ret.package_uri = p.package_uri
    return ret


def experiment_status_api2pb(st):
    status_map = {
        "Created": experiment_pb2.Experiment.State.CREATED,
        "Activated": experiment_pb2.Experiment.State.ACTIVATED,
        "Archived": experiment_pb2.Experiment.State.ARCHIVED,
    }
    return status_map.get(st, experiment_pb2.Experiment.State.UNKNOWN)


def experiment_api2pb(
    exp: bmlx_openapi_client.Experiment,
) -> experiment_pb2.Experiment:
    ret = experiment_pb2.Experiment(
        id=str(exp.id),
        pipeline_version_id=exp.pipeline_version_id,
        context_id=exp.pipeline_version_id,
        name=exp.name,
        namespace=exp.namespace,
        resource_group=exp.resource_group,
        package_uri=exp.package_uri,
        create_time=exp.create_time,
        description=exp.description,
        state=experiment_status_api2pb(exp.status),
        trigger_type=exp.trigger_type,
    )
    return ret


def experiment_pb2api(
    exp: experiment_pb2.Experiment,
) -> bmlx_openapi_client.Experiment:
    return bmlx_openapi_client.Experiment(
        name=exp.name,
        create_time=exp.create_time,
        description=exp.description,
        trigger_type=exp.trigger_type,
    )
