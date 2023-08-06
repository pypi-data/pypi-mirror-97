import os
import logging
import urllib
import requests
import json
import datetime
import itertools
import pathlib
import google.protobuf.descriptor as descriptor

from google.protobuf.message import Message
from ml_metadata.metadata_store import metadata_store
from ml_metadata.proto import metadata_store_pb2 as mlpb
import ml_metadata.errors as mlmd_errors
from typing import Text, List, Optional, Tuple, Dict, Any
from pytz import timezone
from bmlx.utils import io_utils, proc_utils
from bmlx.proto.metadata import (
    execution_pb2,
    artifact_pb2,
    pipeline_pb2,
    experiment_pb2,
)


def _retry_handler(f):
    return proc_utils.retry(
        retry_count=3,
        delay=5,
        allowed_exceptions=(mlmd_errors.UnavailableError),
    )(f)


class LocalStore(object):
    def __init__(self, local_storage_path=None):
        if not local_storage_path:
            local_storage_path = pathlib.Path(
                pathlib.Path.home(), ".bmlx", "metadata"
            )
            if not local_storage_path.exists():
                io_utils.mkdirs(local_storage_path.as_posix())

        sqlite_file = pathlib.Path(local_storage_path, "metadata.db")
        self._ml_store = metadata_store.MetadataStore(
            mlpb.ConnectionConfig(
                sqlite=mlpb.SqliteMetadataSourceConfig(
                    filename_uri=sqlite_file.as_uri(),
                    connection_mode=mlpb.SqliteMetadataSourceConfig.READWRITE_OPENCREATE,
                ),
            )
        )

    def get_pipelines(
        self, page_size, page_token="", filters={}
    ) -> Tuple[List[pipeline_pb2.Pipeline], Text]:
        raise NotImplementedError("Local model does not support get pipelines")

    def get_pipeline_versions(
        self, page_size, page_token="", filters={}
    ) -> Tuple[List[pipeline_pb2.PipelineVersion], Text]:
        raise NotImplementedError(
            "Local model does not support get pipeline version"
        )

    def get_experiments(
        self, page_size, page_token="", filters={}
    ) -> Tuple[List[experiment_pb2.Experiment], Text]:
        raise NotImplementedError("Local model does not support get experiment")

    def get_pipeline_executions(
        self, page_size, page_token="", filters={}
    ) -> Tuple[List[execution_pb2.Execution], Text]:
        all_ret = [
            _pipeline_execution_context_m2b(exe)
            for exe in self._ml_store.get_contexts_by_type(
                _PIPELINE_EXECUTION_CONTEXT_TYPE_NAME
            )
        ]

        def convert_filter(k, v):
            if k in ("status", "state"):
                return "state", execution_pb2.State.Value(v)
            elif k == "id":
                return k, v
            elif k == "experiment_id":
                return None, None
            else:
                raise ValueError("Does not support filter key: %s", k)

        ret = []
        for exe in all_ret:
            valid = True
            if str(exe.id) <= page_token:
                continue
            for k, v in filters.items():
                k, v = convert_filter(k, v)
                if k and str(getattr(exe, k)) != str(v):
                    valid = False
                    break
            if valid:
                ret.append(exe)
        if ret:
            return ret, str(ret[-1].id)
        else:
            return ret, ""

    def get_component_executions(
        self, page_size, page_token="", filters={}
    ) -> Tuple[List[execution_pb2.ComponentExecution], Text]:
        all_ret = [
            _component_execution_m2b(exe)
            for exe in self._ml_store.get_contexts_by_type(
                _COMPONENT_EXECUTION_CONTEXT_TYPE_NAME
            )
        ]

        def convert_filter(k, v):
            if k == "component":
                return "type", v
            elif k == "pipeline_execution_id":
                return "context_id", v
            elif k in ("status", "state"):
                return "state", execution_pb2.State.Value(v)
            elif k == "id":
                return k, v
            else:
                raise ValueError("Does not support filter key: %s", k)

        ret = []
        for exe in all_ret:
            if str(exe.id) <= page_token:
                continue
            valid = True

            for k, v in filters.items():
                k, v = convert_filter(k, v)
                if k and str(getattr(exe, k)) != str(v):
                    valid = False
                    break
            if valid:
                ret.append(exe)
        if ret:
            return ret, str(ret[-1].id)
        else:
            return ret, ""

    def get_pipeline_execution_by_id(
        self, pipeline_execution_id: int
    ) -> execution_pb2.Execution:
        ret = self._get_pipeline_execution_context(pipeline_execution_id)
        if not ret:
            return None
        return _pipeline_execution_context_m2b(ret[0])

    def get_previous_artifacts(
        self, pipeline_execution: execution_pb2.Execution
    ) -> Dict[Text, List[artifact_pb2.Artifact]]:
        component_executions = self.get_component_executions_of_pipeline(
            pipeline_execution=pipeline_execution
        )

        _, outputs = self.get_component_executions_artifacts(
            component_executions=component_executions
        )

        ret = {}
        for output in outputs:
            if output.producer_component not in ret:
                ret[output.producer_component] = [output]
            else:
                ret[output.producer_component].append(output)

        return ret

    @_retry_handler
    def get_or_create_pipeline_execution(
        self, execution: execution_pb2.Execution
    ) -> execution_pb2.Execution:
        previous_context = self._ml_store.get_context_by_type_and_name(
            type_name=_PIPELINE_EXECUTION_CONTEXT_TYPE_NAME,
            context_name=execution.name,
        )

        if not previous_context:
            return self.create_pipeline_execution(execution)
        else:
            logging.info(
                "already created execution context id: %s, type: %s"
                % (previous_context.id, previous_context.type_id)
            )
            execution.context_id = previous_context.id
            execution.id = previous_context.id

        return execution

    @_retry_handler
    def create_pipeline_execution(
        self, execution: execution_pb2.Execution
    ) -> execution_pb2.Execution:
        ctx = self._make_mlpb_context(
            context_type=_PIPELINE_EXECUTION_CONTEXT_TYPE_NAME,
            spec=_PIPELINE_EXECUTION_SPEC,
            context_name=execution.name,
            bmlx_pb_msg=execution,
        )
        try:
            [ctx_id] = self._ml_store.put_contexts([ctx])
            execution.context_id = ctx_id
            execution.id = ctx_id
            logging.info(
                "create execution context id: %s, type: %s"
                % (ctx_id, ctx.type_id)
            )
        except mlmd_errors.AlreadyExistsError:
            previous_context = self._ml_store.get_context_by_type_and_name(
                type_name=_PIPELINE_EXECUTION_CONTEXT_TYPE_NAME,
                context_name=execution.name,
            )
            execution.context_id = previous_context.id
            execution.id = previous_context.id
        return execution

    @_retry_handler
    def update_pipeline_execution(
        self, execution: execution_pb2.Execution
    ) -> bool:
        previous_context = self._ml_store.get_context_by_type_and_name(
            type_name=_PIPELINE_EXECUTION_CONTEXT_TYPE_NAME,
            context_name=execution.name,
        )
        ctx = self._make_mlpb_context(
            context_type=_PIPELINE_EXECUTION_CONTEXT_TYPE_NAME,
            spec=_PIPELINE_EXECUTION_SPEC,
            context_name=execution.name,
            bmlx_pb_msg=execution,
        )
        ctx.id = previous_context.id
        try:
            [ctx_id] = self._ml_store.put_contexts([ctx])
            execution.context_id = ctx_id
            logging.info(
                "update pipeline execution context id: %s, type: %s successfully!"
                % (ctx_id, ctx.type_id)
            )
            return True
        except mlmd_errors.AlreadyExistsError:
            logging.warning("update pipeline execution, already exit error!")
            return False

    _PIPELINE_NAME_FORMAT = "{pipeline_name}_{pipeline_context_id}"

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
        component_execution.context_id = pipeline_execution.id
        if not pipeline_execution.context_id:
            raise RuntimeError("pipeline exectuion context_id invalid")
        contexts = []
        contexts.append(
            self._ml_store.get_contexts_by_id([pipeline_execution.context_id])[
                0
            ]
        )
        component_execution.type_id = self._create_or_update_component_execution_type(
            component_id=component_execution.type,
            exec_properties=exec_properties,
        )
        component_execution_context = self._make_mlpb_context(
            context_type=_COMPONENT_EXECUTION_CONTEXT_TYPE_NAME,
            spec=_COMPONENT_EXECUTION_SPEC,
            context_name=self._get_component_execution_context_name(
                pipeline_execution=pipeline_execution,
                component_id=component_execution.type,
            ),
            bmlx_pb_msg=component_execution,
        )
        existed_ctx = self._ml_store.get_context_by_type_and_name(
            _COMPONENT_EXECUTION_CONTEXT_TYPE_NAME,
            component_execution_context.name,
        )
        if existed_ctx:
            component_execution_context.id = existed_ctx.id
        artifact_events = []
        mlpb_execution = _component_execution_b2m(
            component_execution, workspace_name=pipeline_name
        )
        pipeline_name = self._PIPELINE_NAME_FORMAT.format(
            pipeline_name=pipeline_execution.name,
            pipeline_context_id=pipeline_execution.context_id,
        )

        for input_artifact in input_artifacts:
            input_artifact.name = (
                f"{component_execution.type_id}-{input_artifact.name}"
            )
            input_artifact.type_id = self._create_or_update_artifact_type(
                type_name=input_artifact.type
            )
            existed_artifact = self._ml_store.get_artifact_by_type_and_name(
                input_artifact.type, input_artifact.name
            )
            if existed_artifact:
                input_artifact.id = existed_artifact.id

            artifact_event = (
                _artifact_b2m(
                    input_artifact,
                    pipeline_name=pipeline_name,
                    execution_name=component_execution.name,
                ),
                mlpb.Event(type=mlpb.Event.INPUT),
            )
            artifact_events.append(artifact_event)

        for output_artifact in output_artifacts:
            output_artifact.type_id = self._create_or_update_artifact_type(
                type_name=output_artifact.type
            )
            output_artifact.name = (
                f"{component_execution.type_id}-{output_artifact.name}"
            )

            # output_artifact 可能是已经publish过的artifact，则给artifact.id
            # 赋值,不用重新create
            same_uri_artifacts = self.get_artifacts_by_uri(output_artifact.uri)
            if same_uri_artifacts:
                target = max(same_uri_artifacts, key=lambda m: m.id)
                if target.fingerprint == output_artifact.fingerprint:
                    output_artifact.id = target.id
            else:
                existed_artifact = self._ml_store.get_artifact_by_type_and_name(
                    output_artifact.type, output_artifact.name
                )
                if existed_artifact:
                    output_artifact.id = existed_artifact.id

            artifact_event = (
                _artifact_b2m(
                    output_artifact,
                    pipeline_name=pipeline_name,
                    execution_name=component_execution.name,
                ),
                mlpb.Event(type=mlpb.Event.OUTPUT),
            )

            artifact_events.append(artifact_event)

        try:
            exe_id, input_ids, output_ids = self._ml_store.put_execution(
                execution=mlpb_execution,
                artifact_and_events=artifact_events,
                contexts=contexts + [component_execution_context],
            )
        except mlmd_errors.AlreadyExistsError:
            # same execution has executed, so reuse context
            # get former context
            context_name = self._get_component_execution_context_name(
                pipeline_execution=pipeline_execution,
                component_id=component_execution.type,
            )
            former_context = self._ml_store.get_context_by_type_and_name(
                type_name=_COMPONENT_EXECUTION_CONTEXT_TYPE_NAME,
                context_name=context_name,
            )

            [former_execution] = self._ml_store.get_executions_by_context(
                context_id=former_context.id
            )

            mlpb_execution.id = former_execution.id
            exe_id, input_ids, output_ids = self._ml_store.put_execution(
                execution=mlpb_execution,
                artifact_and_events=artifact_events,
                contexts=contexts,
            )

        return self.get_component_execution_by_id(exe_id)

    @_retry_handler
    def create_artifacts(
        self,
        artifacts: List[artifact_pb2.Artifact],
        component_execution: Optional[execution_pb2.ComponentExecution] = None,
        pipeline_execution: Optional[execution_pb2.Execution] = None,
    ) -> List[int]:
        pipeline_name = None
        execution_name = None

        if pipeline_execution:
            pipeline_name = self._PIPELINE_NAME_FORMAT.format(
                pipeline_name=pipeline_execution.name,
                pipeline_context_id=pipeline_execution.context_id,
            )
        if component_execution:
            execution_name = component_execution.name

        pub = []
        for artifact in artifacts:
            artifact.type_id = self._create_or_update_artifact_type(
                artifact.type
            )
            mlpb_artifact = _artifact_b2m(
                execution_name=execution_name,
                artifact=artifact,
                pipeline_name=pipeline_name,
            )
            pub.append(artifact)

        return self._ml_store.put_artifacts([mlpb_artifact])

    @_retry_handler
    def _get_pipeline_execution_context(
        self, ctx_id
    ) -> execution_pb2.Execution:
        ctx = self._ml_store.get_contexts_by_id([ctx_id])
        if not ctx:
            return None
        else:
            return _pipeline_execution_context_m2b(ctx[0])

    @_retry_handler
    def get_artifacts_by_types(
        self, types: List[Text] = [],
    ):
        if not types:
            artifacts = self._ml_store.get_artifacts()
        else:
            artifacts = list(
                itertools.chain(
                    *[self._ml_store.get_artifacts_by_type(t) for t in types]
                )
            )

        return [_artifact_m2b(artifact) for artifact in artifacts]

    @_retry_handler
    def get_artifacts_by_id(
        self, ids: List[int]
    ) -> List[artifact_pb2.Artifact]:
        return [
            _artifact_m2b(artifact)
            for artifact in self._ml_store.get_artifacts_by_id(ids)
        ]

    @_retry_handler
    def get_artifacts_by_uri(
        self, uris: List[Text]
    ) -> List[artifact_pb2.Artifact]:
        return [
            _artifact_m2b(artifact)
            for artifact in self._ml_store.get_artifacts_by_uri(uris)
        ]

    @_retry_handler
    def get_component_executions_artifacts(
        self, component_executions: List[execution_pb2.ComponentExecution]
    ) -> Tuple[List[artifact_pb2.Artifact], List[artifact_pb2.Artifact]]:

        events = self._ml_store.get_events_by_execution_ids(
            [
                component_execution.id
                for component_execution in component_executions
            ]
        )

        artifacts = {
            artifact.id: artifact
            for artifact in self._ml_store.get_artifacts_by_id(
                [event.artifact_id for event in events]
            )
        }

        return (
            [
                _artifact_m2b(artifacts[event.artifact_id])
                for event in events
                if event.type == mlpb.Event.INPUT
            ],
            [
                _artifact_m2b(artifacts[event.artifact_id])
                for event in events
                if event.type == mlpb.Event.OUTPUT
            ],
        )

    @_retry_handler
    def get_component_executions_of_pipeline(
        self, pipeline_execution: execution_pb2.Execution
    ) -> List[execution_pb2.ComponentExecution]:
        if not pipeline_execution.context_id:
            raise RuntimeError("unknown pipeline execution")

        return [
            _component_execution_m2b(o)
            for o in self._ml_store.get_executions_by_context(
                pipeline_execution.context_id
            )
        ]

    @_retry_handler
    def get_component_execution(
        self, pipeline_execution: execution_pb2.Execution, component_id: Text,
    ) -> execution_pb2.ComponentExecution:
        if not pipeline_execution.context_id:
            raise RuntimeError("unknown pipeline execution")

        component_executions = self._ml_store.get_executions_by_context(
            pipeline_execution.context_id
        )
        for component_execution in component_executions:
            bmlx_exe = _component_execution_m2b(component_execution)
            if bmlx_exe.type == component_id:
                return bmlx_exe
        return None

    def update_component_execution_run_context(
        self,
        component_execution: execution_pb2.ComponentExecution,
        run_context: Dict[Text, Text] = {},
    ):
        pass

    @_retry_handler
    def get_component_execution_by_id(
        self, id: int
    ) -> Tuple[
        execution_pb2.Execution,
        List[artifact_pb2.Artifact],
        List[artifact_pb2.Artifact],
    ]:
        ret = self._ml_store.get_executions_by_id([id])
        if not ret:
            return None, None, None
        else:
            r = self.get_component_executions_artifacts(ret)
            return (_component_execution_m2b(ret[0]), r[0], r[1])

    @_retry_handler
    def _make_mlpb_context_type(self, type_name, spec) -> int:
        try:
            context_type = self._ml_store.get_context_type(type_name=type_name)
            # check properties consistency
            if spec != context_type.properties:
                logging.info(
                    "context type %s schema update, try to update to newer one"
                    % type_name
                )
                self._ml_store.put_context_type(
                    mlpb.ContextType(
                        name=type_name, properties=spec, id=context_type.id,
                    ),
                    can_add_fields=True,
                )
            context_type_id = context_type.id

        except mlmd_errors.NotFoundError:
            context_type_id = self._ml_store.put_context_type(
                mlpb.ContextType(name=type_name, properties=spec,),
                can_add_fields=True,
            )
        return context_type_id

    def _make_mlpb_context(
        self,
        context_type: Text,
        spec: Dict[Text, Any],
        context_name: Text,
        bmlx_pb_msg: Message,
    ) -> mlpb.Context:
        context_type_id = self._make_mlpb_context_type(
            type_name=context_type, spec=spec
        )
        ret = mlpb.Context(name=context_name, type_id=context_type_id,)

        _pack_to_properties(msg=bmlx_pb_msg, properties=ret.properties)
        return ret

    def _get_component_execution_context_name(
        self, pipeline_execution: execution_pb2.Execution, component_id: Text
    ):
        return f"{pipeline_execution.context_id}_{component_id}"

    @_retry_handler
    def _create_or_update_component_execution_type(
        self, component_id: Text, exec_properties: Dict[Text, Any]
    ) -> int:
        try:
            ret = self._ml_store.get_execution_type(type_name=component_id)
        except mlmd_errors.NotFoundError:
            nt = mlpb.ExecutionType(
                name=component_id, properties=_COMPONENT_EXECUTION_SPEC,
            )
            self._ml_store.put_execution_type(
                execution_type=nt, can_add_fields=True
            )
            ret = self._ml_store.get_execution_type(type_name=component_id)
        return ret.id

    @_retry_handler
    def _create_or_update_artifact_type(self, type_name: Text) -> int:
        try:
            ret = self._ml_store.get_artifact_type(type_name=type_name)
            if ret.properties != _ARTIFACT_SPEC:
                logging.info(
                    "detect artifact properties update, update to %s"
                    % _ARTIFACT_SPEC
                )
                return self._ml_store.put_artifact_type(
                    mlpb.ArtifactType(
                        id=ret.id, name=type_name, properties=_ARTIFACT_SPEC
                    ),
                    can_add_fields=True,
                    can_delete_fields=True,
                )
            return ret.id
        except mlmd_errors.NotFoundError:
            nt = mlpb.ArtifactType(name=type_name, properties=_ARTIFACT_SPEC)
            return self._ml_store.put_artifact_type(
                artifact_type=nt, can_add_fields=True
            )


def _parse_time(timestr):
    return int(
        datetime.datetime.strptime(timestr, "%Y-%m-%dT%H:%M:%SZ")
        .replace(tzinfo=timezone("utc"))
        .astimezone()
        .timestamp()
    )


def _parse_status(status_str: Text):
    if status_str == "Running":
        return execution_pb2.State.RUNNING
    elif status_str == "Failed":
        return execution_pb2.State.FAILED
    elif status_str == "Completed":
        return execution_pb2.State.SUCCEEDED
    else:
        logging.warning("unrecogonize status: %s" % status_str)
        return execution_pb2.State.UNKNOWN


# 注意，ml-metadata里面实现虽然声明了name/state等字段, 但是很多并没有存，所以最好的方式是优先使用properties里面的数据恢复
def _artifact_m2b(artifact: mlpb.Artifact) -> artifact_pb2.Artifact:
    """
    convert ml-metadata artifact to bmlx artifact
    """
    ret = artifact_pb2.Artifact()
    _unpack_from_properties(msg=ret, properties=artifact.properties)

    ret.id = artifact.id
    ret.uri = artifact.uri
    ret.type_id = artifact.type_id

    return ret


def _artifact_b2m(
    artifact: artifact_pb2.Artifact,
    execution_name: Optional[Text] = None,
    pipeline_name: Optional[Text] = None,
) -> mlpb.Artifact:
    ret = mlpb.Artifact()

    # NOTE, mlmetadata use proto2, so set to zero is not right
    if artifact.id:
        ret.id = artifact.id
    ret.name = artifact.name
    if not ret.name:
        ret.name = artifact.uri
    ret.uri = artifact.uri
    ret.state = artifact.state
    ret.type = artifact.type
    if artifact.type_id:
        ret.type_id = artifact.type_id

    _pack_to_properties(msg=artifact, properties=ret.properties)

    return ret


def _pipeline_execution_context_m2b(
    execution: mlpb.Context,
) -> execution_pb2.Execution:
    ret = execution_pb2.Execution()

    _unpack_from_properties(msg=ret, properties=execution.properties)
    ret.id = execution.id
    ret.context_id = execution.id
    return ret


def _pipeline_execution_k2b(run_obj) -> execution_pb2.Execution:
    execution = execution_pb2.Execution(
        id=run_obj["id"],
        name=run_obj["name"],
        create_time=_parse_time(run_obj["created_at"]),
        schedule_time=_parse_time(run_obj["scheduled_at"]),
        finish_time=_parse_time(run_obj["finished_at"]),
    )
    if "status" in run_obj:
        execution.state = _parse_status(run_obj["status"])

    for ref in run_obj.get("resource_references") or []:
        if ref["key"]["type"] == "EXPERIMENT":
            execution.experiment_id = ref["key"]["id"]
        if ref["key"]["type"] == "PIPELINE_VERSION":
            execution.pipeline_version_id = ref["key"]["id"]
        if (
            ref["key"]["type"] == "UNKNOWN_RESOURCE_TYPE"
            and ref["name"] == "context"
        ):
            execution.context_id = ref["key"]["id"]

    return execution


def _component_execution_m2b(
    execution: mlpb.Execution,
) -> execution_pb2.ComponentExecution:
    ret = execution_pb2.ComponentExecution()

    _unpack_from_properties(msg=ret, properties=execution.properties)

    ret.id = execution.id
    ret.type_id = execution.type_id

    return ret


def _component_execution_b2m(
    component_execution: execution_pb2.ComponentExecution, workspace_name=None
) -> mlpb.Execution:
    ret = mlpb.Execution()

    if component_execution.id:
        ret.id = component_execution.id
    ret.name = component_execution.name
    ret.type_id = component_execution.type_id
    ret.last_known_state = component_execution.state

    _pack_to_properties(msg=component_execution, properties=ret.properties)

    return ret


"""
下面三个方法是把bmlx的proto映射成ml-metadata的元数据
"""


def _unpack_from_properties(msg, properties):
    desc = msg.DESCRIPTOR

    for k in properties:
        v = properties[k]
        field_desc = desc.fields_by_name[k]

        if field_desc.label == descriptor.FieldDescriptor.LABEL_REPEATED:
            raise NotImplementedError(
                "repeated filed not support, consider use string instead"
            )
        else:
            if (
                field_desc.type == descriptor.FieldDescriptor.TYPE_FLOAT
                or field_desc.type == descriptor.FieldDescriptor.TYPE_DOUBLE
            ):
                setattr(msg, field_desc.name, v.double_value)
            elif (
                field_desc.type == descriptor.FieldDescriptor.TYPE_STRING
                or field_desc.type == descriptor.FieldDescriptor.TYPE_BYTES
            ):
                setattr(msg, field_desc.name, v.string_value)
            elif (
                field_desc.type == descriptor.FieldDescriptor.TYPE_FIXED32
                or field_desc.type == descriptor.FieldDescriptor.TYPE_FIXED64
                or field_desc.type == descriptor.FieldDescriptor.TYPE_INT32
                or field_desc.type == descriptor.FieldDescriptor.TYPE_INT64
                or field_desc.type == descriptor.FieldDescriptor.TYPE_SFIXED32
                or field_desc.type == descriptor.FieldDescriptor.TYPE_SFIXED64
                or field_desc.type == descriptor.FieldDescriptor.TYPE_SINT32
                or field_desc.type == descriptor.FieldDescriptor.TYPE_SINT64
                or field_desc.type == descriptor.FieldDescriptor.TYPE_UINT32
                or field_desc.type == descriptor.FieldDescriptor.TYPE_UINT64
                or field_desc.type == descriptor.FieldDescriptor.TYPE_ENUM
                or field_desc.type == descriptor.FieldDescriptor.TYPE_BOOL
            ):
                setattr(msg, field_desc.name, v.int_value)
            elif (
                field_desc.type == descriptor.FieldDescriptor.TYPE_MESSAGE
                or field_desc.type == descriptor.FieldDescriptor.TYPE_GROUP
            ):
                raise NotImplementedError(
                    "submessage or group meta not supported, you could implment as string in app level"
                )


def _pack_to_properties(msg, properties):

    for field_desc in msg.DESCRIPTOR.fields:
        if field_desc.label == descriptor.FieldDescriptor.LABEL_REPEATED:
            pass
            # raise NotImplementedError(
            #     "repeated field not support, use string instead"
            # )
        else:
            if (
                field_desc.type == descriptor.FieldDescriptor.TYPE_FLOAT
                or field_desc.type == descriptor.FieldDescriptor.TYPE_DOUBLE
            ):
                properties[field_desc.name].double_value = getattr(
                    msg, field_desc.name
                )
            elif (
                field_desc.type == descriptor.FieldDescriptor.TYPE_STRING
                or field_desc.type == descriptor.FieldDescriptor.TYPE_BYTES
            ):
                properties[field_desc.name].string_value = getattr(
                    msg, field_desc.name
                )
            elif (
                field_desc.type == descriptor.FieldDescriptor.TYPE_FIXED32
                or field_desc.type == descriptor.FieldDescriptor.TYPE_FIXED64
                or field_desc.type == descriptor.FieldDescriptor.TYPE_INT32
                or field_desc.type == descriptor.FieldDescriptor.TYPE_INT64
                or field_desc.type == descriptor.FieldDescriptor.TYPE_SFIXED32
                or field_desc.type == descriptor.FieldDescriptor.TYPE_SFIXED64
                or field_desc.type == descriptor.FieldDescriptor.TYPE_SINT32
                or field_desc.type == descriptor.FieldDescriptor.TYPE_SINT64
                or field_desc.type == descriptor.FieldDescriptor.TYPE_UINT32
                or field_desc.type == descriptor.FieldDescriptor.TYPE_UINT64
                or field_desc.type == descriptor.FieldDescriptor.TYPE_ENUM
                or field_desc.type == descriptor.FieldDescriptor.TYPE_BOOL
            ):
                properties[field_desc.name].int_value = getattr(
                    msg, field_desc.name
                )
            elif (
                field_desc.type == descriptor.FieldDescriptor.TYPE_MESSAGE
                or field_desc.type == descriptor.FieldDescriptor.TYPE_GROUP
            ):
                raise NotImplementedError(
                    "submessage or group meta not supported, you could implment as string in app level"
                )


def _reflect_properties_from_pb(desc: descriptor.Descriptor):
    ret = {}

    for field_desc in desc.fields:
        if field_desc.label == descriptor.FieldDescriptor.LABEL_REPEATED:
            ret[field_desc.name] = mlpb.STRING
        else:
            if (
                field_desc.type == descriptor.FieldDescriptor.TYPE_FLOAT
                or field_desc.type == descriptor.FieldDescriptor.TYPE_DOUBLE
            ):
                ret[field_desc.name] = mlpb.DOUBLE
            elif (
                field_desc.type == descriptor.FieldDescriptor.TYPE_STRING
                or field_desc.type == descriptor.FieldDescriptor.TYPE_BYTES
            ):
                ret[field_desc.name] = mlpb.STRING
            elif (
                field_desc.type == descriptor.FieldDescriptor.TYPE_FIXED32
                or field_desc.type == descriptor.FieldDescriptor.TYPE_FIXED64
                or field_desc.type == descriptor.FieldDescriptor.TYPE_INT32
                or field_desc.type == descriptor.FieldDescriptor.TYPE_INT64
                or field_desc.type == descriptor.FieldDescriptor.TYPE_SFIXED32
                or field_desc.type == descriptor.FieldDescriptor.TYPE_SFIXED64
                or field_desc.type == descriptor.FieldDescriptor.TYPE_SINT32
                or field_desc.type == descriptor.FieldDescriptor.TYPE_SINT64
                or field_desc.type == descriptor.FieldDescriptor.TYPE_UINT32
                or field_desc.type == descriptor.FieldDescriptor.TYPE_UINT64
                or field_desc.type == descriptor.FieldDescriptor.TYPE_ENUM
                or field_desc.type == descriptor.FieldDescriptor.TYPE_BOOL
            ):
                ret[field_desc.name] = mlpb.INT
            elif field_desc.type == descriptor.FieldDescriptor.TYPE_MESSAGE:
                ret[field_desc.name] = mlpb.STRING
            elif field_desc.type == descriptor.FieldDescriptor.TYPE_GROUP:
                raise NotImplementedError(
                    "submessage or group meta not supported, you could implment as string in app level"
                )

    return ret


_ARTIFACT_SPEC = _reflect_properties_from_pb(artifact_pb2.Artifact.DESCRIPTOR)

_COMPONENT_EXECUTION_SPEC = _reflect_properties_from_pb(
    execution_pb2.ComponentExecution.DESCRIPTOR
)
_PIPELINE_EXECUTION_SPEC = _reflect_properties_from_pb(
    execution_pb2.Execution.DESCRIPTOR
)
_EXPERIMENT_SPEC = _reflect_properties_from_pb(
    experiment_pb2.Experiment.DESCRIPTOR
)

_PIPELINE_EXECUTION_CONTEXT_TYPE_NAME = "bmlx.context.execution"
_COMPONENT_EXECUTION_CONTEXT_TYPE_NAME = "bmlx.context.component_execution"
