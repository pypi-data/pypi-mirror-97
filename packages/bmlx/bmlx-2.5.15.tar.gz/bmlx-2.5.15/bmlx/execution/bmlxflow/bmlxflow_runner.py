import os
import sys
import logging
from typing import Text, Optional, List
import tempfile
import yaml
import socket

from bmlx.flow import Pipeline, Component
from bmlx.context import BmlxContext

from bmlx.execution.runner import Runner
from bmlx.execution.bmlxflow import ArgoNode
from bmlx.execution.bmlxflow import Workflow
from bmlx.utils import naming_utils


class BmlxflowRunner(Runner):
    def __init__(self, ctx: BmlxContext, pipeline: Pipeline):
        if not pipeline:
            raise ValueError("Runner must set pipeline!")

        self._pipeline = pipeline
        self._ctx = ctx

    def gen_argo_node(
        self,
        bmlx_component: Component,
    ):
        arguments = self._ctx.generate_component_run_command(
            component_id=bmlx_component.id,
            execution_name="{{workflow.name}}",
            # 先产生workflow.spec.yml，后上传 package 以及 创建 experiment。
            # 因此这里的 experiment_id 填占位符，在 server端创建experiment的时候，将 experiment_id, package_checksum
            # 设置到argo 的 workflow parameters中.
            # argo 执行时候替换 experiment_id 占位符为实际值
            experiment_id="{{workflow.parameters.experiment_id}}",
            collect_log=True,
            checksum="{{workflow.parameters.package_checksum}}",
            package_uri="{{workflow.parameters.package_uri}}",
        )

        command = arguments[0]
        arguments = arguments[1:]

        bmlx_image, _, policy = self._ctx.image()
        node = ArgoNode(
            name=bmlx_component.id.replace(".", "-").replace(
                "_", "-"
            ),  # k8s 名字有要求
            image=bmlx_image,
            command=command,
            args=arguments,
            # 将 component id 注入到 label中，用于应对如下场景：
            # argo workflow 启动之后，在 bmlx 的 node 去create_pipeline_execution 和 register_component_execution 之前就跪掉
            # ==> 从而无法将meta信息写入到数据库 ==> 前端无法获取失败日志，状态等信息。
            #
            # 这里注入 component_id 信息，则bmlx api server 监听到 workflow 失败的event的时候，
            # 就可以用component_id 信息主动在数据库创建 component_run 并记录argo pod。
            # 从而前端可以查到失败信息
            # bmlx_workflow_id, bmlx_component 用于ES 建索引
            labels={
                "component_id": bmlx_component.id,
                "bmlx_workflow_id": "{{workflow.name}}",
                "bmlx_component": bmlx_component.id,
            },
        )
        node.set_metrics(
            ArgoNode.gen_template_metrics(
                self._pipeline.meta.name, type(bmlx_component).__name__
            )
        )
        node.container["imagePullPolicy"] = policy
        node.add_volume(
            {
                "name": "podinfo",
                "downwardApi": {
                    "items": [
                        {
                            "path": "labels",
                            "fieldRef": {"fieldPath": "metadata.labels"},
                        },
                        {
                            "path": "name",
                            "fieldRef": {"fieldPath": "metadata.name"},
                        },
                    ]
                },
            }
        )
        node.add_volume_mount({"name": "podinfo", "mountPath": "/etc/podinfo"})
        return node

    def gen_exit_node(self):
        arguments = self._ctx.generate_pipeline_cleanup_command(
            execution_name="{{workflow.name}}",
            checksum="{{workflow.parameters.package_checksum}}",
            experiment_id="{{workflow.parameters.experiment_id}}",
            package_uri="{{workflow.parameters.package_uri}}",
        )
        command = arguments[0]
        arguments = arguments[1:]

        bmlx_image, _, policy = self._ctx.image()
        node = ArgoNode(
            name="clean-up",
            image=bmlx_image,
            command=command,
            args=arguments,
        )
        node.container["imagePullPolicy"] = policy
        return node

    def compile_pipeline(self, workflow_name: Text, use_host_network: bool):
        # generate argo workflow spec yml file
        _, secrets, _ = self._ctx.image()
        component_to_node = {}
        workflow = Workflow(name=workflow_name)
        workflow.set_image_pull_secrets(secrets)
        workflow.set_host_network(use_host_network)
        workflow.set_exit_handler(self.gen_exit_node())
        workflow.set_metrics(
            Workflow.gen_workflow_metrics(self._pipeline.meta.name)
        )
        for component in self._pipeline.components:
            node = self.gen_argo_node(component)
            for upstream_component in sorted(
                component.preorders, key=lambda x: x.id
            ):
                node.add_dependency(component_to_node[upstream_component])

            workflow.add_node(node)
            component_to_node[component] = node
        return workflow.compile()

    def gen_workflow_spec(
        self, workflow_name: Text, use_host_network: bool = True
    ):
        workflow_name = workflow_name.replace("_", "-")  # argo 命名要求
        if not naming_utils.is_valid_argo_name(workflow_name):
            raise ValueError(
                "Invalid argo workflow name %s, argo name pattern: %s",
                workflow_name,
                naming_utils.argo_name_pattern(),
            )

        spec = self.compile_pipeline(workflow_name, use_host_network)
        path = os.path.join(self._ctx.project.base_path, ".workflow_spec.json")
        with open(path, "w") as f:
            f.write(spec)

    # 创建 轻量级 experiment, 这条分支只会出现在 本地run 提交一个bmlx flow pipeline 到 argo workflow
    def run(
        self,
        package_uri: Text,
        package_checksum: Text,
        execution_description: Text,
    ) -> None:
        pipeline_name = self._pipeline.meta.name.replace("_", "-")
        experiment_name = f"light-weight-{pipeline_name}"
        if not naming_utils.is_valid_argo_name(experiment_name):
            raise ValueError(
                "Invalid argo name %s for experiment, name should be match with pattern %s",
                experiment_name,
                naming_utils._ARGO_NAMING_RE,
            )
        # 轻量级的experiment 会立即执行

        def get_parameter_value(v):
            if isinstance(v, dict):
                return str(v["value"])
            else:
                return str(v)

        # 构造参数信息，用于前端显示
        parameters = {
            k: get_parameter_value(v)
            for (k, v) in self._ctx.project.configurables()
        }
        exp = self._ctx.metadata.create_light_weight_experiment(
            name=experiment_name,
            package_uri=package_uri,
            package_checksum=package_checksum,
            dag=self._pipeline.get_pipeline_dag(),  # 填充dag 信息，用于前端显示
            parameters=parameters,
        )
        logging.info(
            "[BmlxflowRunner] created experiment, name: %s, id: %s",
            exp.name,
            exp.id,
        )
