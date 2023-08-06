import abc
import logging
import sys
from typing import Text, Dict, Any, Optional
from six import with_metaclass
from datetime import datetime
import types

from bmlx.context import BmlxContext
from bmlx.flow import Pipeline, Component, Hook, Node
from bmlx.execution.driver import DriverArgs
from bmlx.execution.launcher import Launcher
from bmlx.proto.metadata import execution_pb2


class Runner(with_metaclass(abc.ABCMeta)):
    """
    pipeline runner is abstract of pipeline execution
    the main purpose is to resolve topo logic order for components
    and set proper launcher to launcher each component
    """

    def __init__(self, pipeline: Pipeline, ctx: BmlxContext):
        if not pipeline:
            raise ValueError("PipelineRunner must set pipeline!")
        self._pipeline = pipeline
        self._ctx = ctx

    @classmethod
    def get_launcher(
        cls,
        context: BmlxContext,
        pipeline_execution: execution_pb2.Execution,
        component: Component,
        pipeline: Pipeline,
        extra_parameters: Dict[Text, Any] = None,
    ):
        driver_args = DriverArgs(
            artifact_storage_base=context.project.artifact_storage_base,
            pipeline_execution=pipeline_execution,
            enable_cache=pipeline.enable_cache,
            prepare_output_uri=True,
            local_mode=context.local_mode,
            project_name=context.project.name,
            owner=context.user,
        )

        launcher_class = Launcher
        if isinstance(component, Node):
            if hasattr(component, "get_launcher_class"):
                launcher_class = component.get_launcher_class(context)
                logging.info(
                    "component %s use launcher: %s"
                    % (component, launcher_class)
                )

        launcher = launcher_class(
            context=context,
            driver_args=driver_args,
            pipeline=pipeline,
            component=component,
            extra_parameters=extra_parameters,
        )
        return launcher

    @classmethod
    def launch_component(
        cls,
        context: BmlxContext,
        pipeline_execution: execution_pb2.Execution,
        component: Component,
        pipeline: Pipeline,
        extra_parameters: Dict[Text, Any] = None,
        sub_component: bool = False,
    ):
        logging.info(
            "Launch Component %s, try limit: %d", component, component.try_limit
        )

        launcher = Runner.get_launcher(
            context=context,
            pipeline_execution=pipeline_execution,
            component=component,
            pipeline=pipeline,
            extra_parameters=extra_parameters,
        )
        try_cnt = 0
        while try_cnt < component.try_limit:
            try:
                launcher.launch()
                if (
                    not sub_component
                ):  # bmlx-component 分散出的子节点(比如xdl worker)没必要执行hook
                    for hook in context.hooks:
                        hook.onComponentDone(
                            context,
                            pipeline,
                            pipeline_execution,
                            component,
                            Hook.HookResult(Hook.Status.SUCCESS, ""),
                        )
                break
            except Exception as e:
                if not sub_component:  # bmlx-component 分散出的子节点没必要执行hook
                    for hook in context.hooks:
                        hook.onComponentDone(
                            context,
                            pipeline,
                            pipeline_execution,
                            component,
                            Hook.HookResult(Hook.Status.FAIL, str(e)),
                        )
                try_cnt += 1
                if try_cnt >= component.try_limit:
                    raise RuntimeError(e)

    def run(
        self,
        execution_name: Text,
        execution_description: Text,
        experiment_id: Optional[Text] = None,
    ) -> None:
        """
        local runner, this would run in topo sort order
        subclass should override this method
        """
        self._pipeline_execution = self._ctx.metadata.get_or_create_pipeline_execution(
            pipeline=self._pipeline,
            execution_name=execution_name,
            # bmlx flow 和api server通信时候需要 experiment id. 如果experiment_id != 0 则说明是使用 argo调度的 bmlx flow experiment run
            experiment_id=experiment_id,
            execution_desc=execution_description,
        )

        logging.info(
            "[LocalRuner] pipeline {} start (id: {})".format(
                self._pipeline.meta.name,
                self._pipeline_execution.id,
            )
        )

        for component in self._pipeline.components:
            Runner.launch_component(
                context=self._ctx,
                pipeline_execution=self._pipeline_execution,
                component=component,
                pipeline=self._pipeline,
            )

    def cleanup_component(
        self,
        component: Component,
        component_execution_state: execution_pb2.State,
    ) -> Text:
        logging.info("Cleanup Component %s" % component)

        launcher = Runner.get_launcher(
            self._ctx, self._pipeline_execution, component, self._pipeline
        )
        return launcher.cleanup(component_execution_state)

    def cleanup(
        self, execution_name: Text, experiment_id: Text, workflow_status: Text
    ):
        self._pipeline_execution = (
            self._ctx.metadata.get_or_create_pipeline_execution(
                pipeline=self._pipeline,
                execution_name=execution_name,
                experiment_id=experiment_id,
            )
        )
        self._pipeline_execution.finish_time = int(datetime.now().timestamp())

        if workflow_status == "Succeeded":
            hook_result = Hook.HookResult(Hook.Status.SUCCESS, "")
            self._pipeline_execution.state = execution_pb2.State.SUCCEEDED
        else:
            hook_result = Hook.HookResult(Hook.Status.FAIL, "")
            self._pipeline_execution.state = execution_pb2.State.FAILED

        self._ctx.metadata.update_pipeline_execution(self._pipeline_execution)

        for hook in self._ctx.hooks:
            hook.onPipelineDone(
                self._ctx, self._pipeline, self._pipeline_execution, hook_result
            )

        logging.info(
            "[LocalRuner] pipeline {} start to cleanup (id: {}, workflow status: {})".format(
                self._pipeline.meta.name,
                self._pipeline_execution.id,
                workflow_status,
            )
        )
        for component in self._pipeline.components:
            component_execution = self._ctx.metadata.get_component_execution(
                self._pipeline_execution, component.id
            )
            state = (
                component_execution.state
                if component_execution
                else execution_pb2.State.FAILED
            )
            # 如果任务结束的时候仍然处于 running状态，则一定是 TERMINATED 了
            if state == execution_pb2.State.RUNNING:
                # 更新状态到 metadata
                self._ctx.metadata.update_component_execution(
                    pipeline=self._pipeline,
                    pipeline_execution=self._pipeline_execution,
                    component=component,
                    state=execution_pb2.State.TERMINATED,
                )

            cleanup_msg = self.cleanup_component(
                component=component,
                component_execution_state=state,
            )
            logging.info(
                "clean up component %s, result message: %s",
                component.id,
                cleanup_msg,
            )
