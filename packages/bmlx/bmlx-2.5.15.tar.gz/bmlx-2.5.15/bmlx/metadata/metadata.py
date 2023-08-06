import abc
import string
import logging
import random
import os
from datetime import datetime

from six import with_metaclass
from bmlx.flow.artifact import Artifact
from bmlx.flow.pipeline import Pipeline
from bmlx.flow.component import Component
from bmlx.flow import Channel
from typing import Text, Dict, List, Any, Optional, Tuple

from bmlx.metadata.bmlxflow_store import BmlxflowStore
from bmlx.proto.metadata import (
    execution_pb2,
    artifact_pb2,
    experiment_pb2,
    pipeline_pb2,
)
from bmlx.utils import io_utils

_MAX_RETRY = 3


class Metadata(with_metaclass(abc.ABCMeta)):
    def __init__(
        self,
        local_mode: bool,
        local_storage_path: Optional[Text] = None,
        api_endpoint: Optional[Text] = None,
        env: Optional[Text] = "prod",
        skip_auth: Optional[bool] = False,
    ):
        # local 模式仍然采用tfx的ml-metadata 作为store
        if local_mode:
            from bmlx.metadata.local_store import LocalStore

            self.store = LocalStore(local_storage_path=local_storage_path)

        else:  # remote 模式使用 bmlxflow的store
            self.store = BmlxflowStore(api_endpoint, env, skip_auth)

    def get_or_create_pipeline(self, **kwargs):
        return self.store.get_or_create_pipeline(**kwargs)

    def create_pipeline_version(self, **kwargs):
        return self.store.create_pipeline_version(**kwargs)

    def create_light_weight_experiment(
        self,
        name: Text,
        package_uri: Text,
        package_checksum: Text = "",
        dag=[],
        parameters={},
    ) -> experiment_pb2.Experiment:
        return self.store.create_light_weight_experiment(
            name, package_uri, package_checksum, dag, parameters
        )

    def build_execution_obj(
        self,
        pipeline: Pipeline,
        experiment_id: Text = "",
        parameters: Dict[Text, Any] = {},
        execution_name: Optional[Text] = None,
        execution_desc: Optional[Text] = None,
    ) -> execution_pb2.Execution:
        # 这个分支 是 用于 local run
        if experiment_id is None:
            experiment = experiment_pb2.Experiment(
                name="LocalExperiment", id="0", context_id=0,
            )
        else:  # 这个分支是用于本地提交到 argo上执行 或者 平台创建的定时 experiment run
            experiment = experiment_pb2.Experiment(
                id=experiment_id,
                context_id=int(experiment_id) if experiment_id else 0,
            )

        execution = execution_pb2.Execution()
        execution.name = execution_name or (
            pipeline.meta.name + self._gen_random_suffix(8)
        )
        execution.description = execution_desc or pipeline.meta.description
        execution.state = execution_pb2.State.RUNNING
        execution.experiment_id = experiment.id
        if pipeline.meta.id:
            execution.pipeline_id = pipeline.meta.id
        return execution

    def get_or_create_pipeline_execution(
        self,
        pipeline: Pipeline,
        experiment_id: Text = "",
        parameters: Dict[Text, Any] = {},
        execution_name: Optional[Text] = None,
        execution_desc: Optional[Text] = None,
    ) -> execution_pb2.Execution:
        execution = self.build_execution_obj(
            pipeline, experiment_id, parameters, execution_name, execution_desc,
        )
        return self.store.get_or_create_pipeline_execution(execution)

    def update_pipeline_execution(
        self, execution: execution_pb2.Execution
    ) -> bool:
        return self.store.update_pipeline_execution(execution)

    def get_pipeline_execution_by_id(self, id: int) -> execution_pb2.Execution:
        return self.store.get_pipeline_execution_by_id(id)

    def get_component_execution(
        self, pipeline_execution: execution_pb2.Execution, component_id: Text,
    ) -> execution_pb2.ComponentExecution:
        return self.store.get_component_execution(
            pipeline_execution, component_id
        )

    def register_component_execution(
        self,
        pipeline: Pipeline,
        pipeline_execution: execution_pb2.Execution,
        component: Component,
        input_dict: Dict[Text, List[Artifact]] = {},
        output_dict: Dict[Text, List[Artifact]] = {},
        exec_properties: Dict[Text, Any] = {},
    ) -> Tuple[
        execution_pb2.Execution,
        List[artifact_pb2.Artifact],
        List[artifact_pb2.Artifact],
    ]:
        component_execution = execution_pb2.ComponentExecution()
        component_execution.name = f"{pipeline.meta.name}_{pipeline_execution.context_id}_{component.id}"
        component_execution.type = component.id
        component_execution.start_time = int(datetime.now().timestamp())
        component_execution.context_id = pipeline_execution.id
        component_execution.state = execution_pb2.State.RUNNING

        (
            execution_meta,
            inputs,
            outputs,
        ) = self.store.create_or_update_component_execution(
            pipeline_execution=pipeline_execution,
            component_execution=component_execution,
            pipeline_name=pipeline_execution.name,
        )

        logging.debug(
            "MetaData: registered component_execution: id:%s"
            % execution_meta.id
        )
        return execution_meta, inputs, outputs

    def update_component_exec_context(self, pipeilne: Pipeline):
        pass

    def update_component_execution(
        self,
        pipeline: Pipeline,
        pipeline_execution: execution_pb2.Execution,
        component: Component,
        input_dict: Dict[Text, List[Artifact]] = {},
        output_dict: Dict[Text, List[Artifact]] = {},
        exec_properties: Dict[Text, Any] = {},
        state=execution_pb2.State.SUCCEEDED,
    ) -> Tuple[
        execution_pb2.Execution,
        List[artifact_pb2.Artifact],
        List[artifact_pb2.Artifact],
    ]:
        component_execution = self.store.get_component_execution(
            pipeline_execution=pipeline_execution, component_id=component.id,
        )
        component_execution.finish_time = int(datetime.now().timestamp())
        component_execution.state = state
        # input artifacts
        input_artifacts = []
        for name, artifacts in input_dict.items():
            input_artifacts.extend([ar.meta for ar in artifacts])

        # generate fingerprint
        output_artifacts = []
        for name, artifacts in output_dict.items():
            for ar in artifacts:
                ar.meta.state = artifact_pb2.Artifact.State.LIVE
                ar.meta.execution_id = str(pipeline_execution.id)
                ar.meta.producer_component = component.id
                ar.meta.fingerprint = self.generate_artifact_fingerprint(
                    input_artifacts=input_dict,
                    exec_properties=exec_properties,
                    component=component,
                )
                logging.info(
                    "update_component_execution, generate artifact "
                    "fingerprint: %s",
                    ar.meta.fingerprint,
                )
                output_artifacts.append(ar.meta)
        return self.store.create_or_update_component_execution(
            pipeline_execution=pipeline_execution,
            component_execution=component_execution,
            input_artifacts=input_artifacts,
            output_artifacts=output_artifacts,
            pipeline_name=pipeline.meta.name,
        )

    def update_component_execution_run_context(
        self,
        pipeline_execution: execution_pb2.Execution,
        component: Component,
        run_context: Dict[Text, Text] = {},
    ):
        component_execution = self.store.get_component_execution(
            pipeline_execution=pipeline_execution, component_id=component.id,
        )
        return self.store.update_component_execution_run_context(
            component_execution=component_execution, run_context=run_context
        )

    def get_artifacts_by_uri(self, uri: Text):
        return self.store.get_artifacts_by_uri(uri)

    def get_artifacts(
        self, page_size, page_token="", filters={}
    ) -> Tuple[List[artifact_pb2.Artifact], Text]:
        return self.store.get_artifacts(page_size, page_token, filters)

    def get_artifacts_by_types(self, types=[]):
        return self.store.get_artifacts_by_types(types)

    def get_pipelines(
        self, page_size, page_token="", filters={}
    ) -> Tuple[List[pipeline_pb2.Pipeline], Text]:
        return self.store.get_pipelines(page_size, page_token, filters)

    def get_pipeline_versions(
        self, page_size, page_token="", filters={}
    ) -> Tuple[List[pipeline_pb2.PipelineVersion], Text]:
        return self.store.get_pipeline_versions(page_size, page_token, filters)

    def get_pipeline_executions(
        self, page_size, page_token="", filters={}
    ) -> Tuple[List[execution_pb2.Execution], Text]:
        return self.store.get_pipeline_executions(
            page_size, page_token, filters
        )

    def get_component_executions(
        self, page_size, page_token="", filters={}
    ) -> Tuple[List[execution_pb2.ComponentExecution], Text]:
        return self.store.get_component_executions(
            page_size, page_token, filters
        )

    def get_experiments(
        self, page_size, page_token="", filters={}
    ) -> Tuple[List[experiment_pb2.Experiment], Text]:
        return self.store.get_experiments(page_size, page_token, filters)

    def publish_artifacts(
        self,
        component_execution: execution_pb2.ComponentExecution,
        pipeline_execution: execution_pb2.Execution,
        artifacts: List[Artifact],
    ) -> int:
        metas = []
        for artifact in artifacts:
            artifact.meta.create_time = int(datetime.now().timestamp())
            artifact.meta.state = artifact_pb2.Artifact.State.LIVE
            metas.append(metas)

        return self.store.create_artifacts(
            component_execution=component_execution,
            pipeline_execution=pipeline_execution,
            artifacts=artifacts,
        )

    def get_previous_artifacts(
        self, pipeline_execution: execution_pb2.Execution
    ) -> Dict[Text, List[artifact_pb2.Artifact]]:
        return self.store.get_previous_artifacts(pipeline_execution)

    def generate_artifact_fingerprint(
        self,
        input_artifacts: Dict[Text, List[Artifact]],
        exec_properties: Dict[Text, Any],
        component: Component,
    ) -> Text:
        input_artifacts_arr = sorted(
            [(k, v) for (k, v) in input_artifacts.items()],
            key=lambda ele: ele[0],
        )
        exec_props_arr = sorted(
            [(k, v) for (k, v) in exec_properties.items()],
            key=lambda ele: ele[0],
        )

        return "component: {}#inputs: {}#exec_properties: {}".format(
            component.id,
            ",".join(
                ["{}={}".format(k, repr(v)) for (k, v) in input_artifacts_arr]
            ),
            ",".join(["{}={}".format(k, repr(v)) for (k, v) in exec_props_arr]),
        )

    def get_cached_outputs(
        self,
        input_artifacts: Dict[Text, List[Artifact]],
        exec_properties: Dict[Text, Any],
        component: Component,
        expected_outputs: Dict[Text, Channel],
    ):
        fingerprint = self.generate_artifact_fingerprint(
            input_artifacts, exec_properties, component
        )
        founded_outputs = {}

        for out_name, channel in expected_outputs.items():
            published_artifacts = [
                Artifact(type_name=channel.type_name, meta=artifact)
                for artifact in self.store.get_artifacts(
                    types=[channel.type_name]
                )
                if artifact.fingerprint == fingerprint
            ]
            if published_artifacts:
                founded_outputs[out_name] = published_artifacts

        def compare_outputs(expected_outputs, founded_outputs):
            for k, v in expected_outputs.items():
                if k not in founded_outputs:
                    return False
            return True

        if compare_outputs(expected_outputs, founded_outputs):
            return founded_outputs
        else:
            return {}

    _METRICS_PATH = "{base_metrics_path}/{experiment_id}/{component_run_id}"

    @classmethod
    def upload_metrics(
        cls,
        base_metrics_path: Text,
        experiment_id: Text,
        component_run_id: Text,
        local_path: Text,
    ):
        output_path = cls._METRICS_PATH.format(
            base_metrics_path=base_metrics_path,
            experiment_id=experiment_id,
            component_run_id=component_run_id,
        )
        io_utils.copytree(src=local_path, dst=output_path)
        logging.info(
            "copy local metrics dir %s to %s" % (local_path, output_path)
        )

    _PKG_PATH = (
        "{pipeline_storage_path}/{package_name}/{checksum}/{package_name}.zip"
    )

    @classmethod
    def upload_package(
        cls, pipeline_storage_path: Text, local_path: Text, checksum: Text,
    ):
        package_name = os.path.splitext(os.path.basename(local_path))[0]
        output_fs, output_path = io_utils.resolve_filesystem_and_path(
            pipeline_storage_path
        )
        output_path = cls._PKG_PATH.format(
            pipeline_storage_path=output_path,
            package_name=package_name,
            checksum=checksum,
        )
        if output_fs.exists(output_path):
            logging.info(
                f"pipeline package {output_path} with checksum {checksum} already exists"
            )
            return output_path

        with output_fs.open(output_path, "wb") as o:
            with open(local_path, "rb") as i:
                o.write(i.read())

        if not output_fs.exists(output_path):
            raise RuntimeError(
                f"Failed to upload package {local_path} to {output_path}"
            )
        return output_path

    @classmethod
    def _download_package(
        cls, input_path, output_path,
    ):
        input_fs, input_path = io_utils.resolve_filesystem_and_path(input_path)

        if not input_fs.exists(input_path):
            raise RuntimeError(
                f"Package file {input_path} does not exist on {input_fs}"
            )

        output_fs, output_path = io_utils.resolve_filesystem_and_path(
            output_path
        )
        if not output_fs.exists(os.path.dirname(output_path)):
            output_fs.mkdir(os.path.dirname(output_path), create_parents=True)
        with output_fs.open(output_path, "wb") as o:
            with input_fs.open(input_path, "rb") as i:
                o.write(i.read())

        return output_fs.exists(output_path)

    @classmethod
    def download_package(
        cls,
        pipeline_storage_path: Text,
        package_name: Text,
        checksum: Text,
        local_dir: Text,
    ):
        input_path = cls._PKG_PATH.format(
            pipeline_storage_path=pipeline_storage_path,
            package_name=package_name,
            checksum=checksum,
        )

        output_path = f"{local_dir}/{package_name}.zip"

        return cls._download_package(input_path, output_path)

    def _gen_random_suffix(self, N: int):
        return "".join(
            random.choice(string.ascii_uppercase + string.digits)
            for _ in range(N)
        )
