import logging

import os

from typing import Dict, Text, Any, Optional
from bmlx.flow import Driver, DriverArgs, Channel, Pipeline, Component, Artifact
from bmlx.metadata.metadata import Metadata
from bmlx.utils import io_utils
from bmlx.execution.execution import ExecutionInfo


class BaseDriver(Driver):
    def __init__(self, metadata: Metadata):
        self._metadata = metadata

    def resolve_input_artifacts(
        self,
        input_dict: Dict[Text, Channel],
        component: Component,
        driver_args: DriverArgs,
    ):
        previous_outputs = self._metadata.get_previous_artifacts(
            driver_args.pipeline_execution
        )

        input_artifacts = {}
        for name, channel in input_dict.items():
            artifacts = list(channel.get())
            if not artifacts:
                raise RuntimeError(
                    "required channel '%s' is empty" % channel.type_name
                )

            input_artifacts[name] = []
            if artifacts[0].meta.producer_component not in previous_outputs:
                if artifacts[0].meta.uri and artifacts[0].meta.type:
                    input_artifacts[name] = artifacts
                else:
                    raise RuntimeError(
                        "unfound component execution %s"
                        % artifacts[0].meta.producer_component
                    )
            else:
                for input_meta in previous_outputs[
                    artifacts[0].meta.producer_component
                ]:
                    # this is bmlx Artifact
                    if input_meta.type == channel.type_name:
                        input_artifact = Artifact(type_name=input_meta.type)
                        input_artifact.meta.CopyFrom(input_meta)
                        input_artifacts[name].append(input_artifact)

            if len(input_artifacts) == 0 and not channel.optional:
                raise RuntimeError(
                    "didn't find any input from metaserver from %s"
                    % artifacts[0].meta.producer_component
                )
        return input_artifacts

    def pre_execution(
        self,
        input_dict: Dict[Text, Channel],
        output_dict: Dict[Text, Channel],
        exec_properties: Dict[Text, Any],
        pipeline: Pipeline,
        component: Component,
        driver_args: DriverArgs,
    ) -> ExecutionInfo:
        skip_execution = component.skip_execution(
            driver_args.pipeline_execution, exec_properties
        )
        if skip_execution:
            logging.info(
                "skip execution of component %s in pipeline execution %s",
                component.id,
                driver_args.pipeline_execution,
            )
            return ExecutionInfo(
                input_dict={},
                output_dict={},
                exec_properties=exec_properties,
                use_cached_result=False,
                skip_execution=True,
            )
        else:
            input_artifacts = self.resolve_input_artifacts(
                input_dict, component, driver_args
            )

            output_artifacts = {}
            use_cached_result = False
            if driver_args.enable_cache:
                output_artifacts = self._metadata.get_cached_outputs(
                    input_artifacts=input_artifacts,
                    exec_properties=exec_properties,
                    component=component,
                    expected_outputs=output_dict,
                )

            if output_artifacts:
                use_cached_result = True
            else:
                for name, channel in output_dict.items():
                    output_artifacts[name] = []

                    for artifact in channel.get():
                        logging.info(
                            "prepare execution, output artifact: %s", artifact
                        )
                        if driver_args.prepare_output_uri:
                            uri = "{}/exp_{}/run_{}/{}".format(
                                driver_args.artifact_storage_base,
                                str(driver_args.pipeline_execution.context_id),
                                str(driver_args.pipeline_execution.id),
                                str(component.id),
                            )
                            logging.debug(
                                "creating new artifact output dir '%s' for '%s'"
                                % (uri, component.id)
                            )
                            if not io_utils.exists(uri):
                                logging.info("create directory for uri %s", uri)
                                io_utils.mkdirs(uri)
                            artifact.meta.uri = uri
                            artifact.meta.type = channel.type_name

                        output_artifacts[name].append(artifact)

                use_cached_result = False

            return ExecutionInfo(
                input_dict=input_artifacts,
                output_dict=output_artifacts,
                exec_properties=exec_properties,
                use_cached_result=use_cached_result,
                skip_execution=False,
            )
