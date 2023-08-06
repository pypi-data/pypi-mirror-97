from typing import Text, Optional, List, Dict
from bmlx.flow.component import Component
from bmlx.flow.channel import Channel
from bmlx.flow.hook import Hook
from bmlx.proto.metadata import pipeline_pb2
from bmlx.utils import naming_utils
import json


class Pipeline(object):
    """
    bmlx pipeline object, pipeline contains component, execution and
    other parameter settings
    """

    __slots__ = [
        "id",
        "meta",
        "enable_cache",
        "additional_args",
        "_components",
        "hooks",
    ]

    def __init__(
        self,
        name: Text,
        components: Optional[List[Component]] = None,
        enable_cache: Optional[bool] = False,
        namespace: Optional[Text] = "default",
        description: Optional[Text] = "",
        hooks: Optional[List[Hook]] = [],
        **kwargs
    ) -> None:
        if not naming_utils.is_name_valid(name):
            raise RuntimeError(
                "pipeline name [%s] invalid, please check"
                "https://kubernetes.io/docs/concepts/overview/working-with-objects/names/"
                "for more details" % name
            )
        self.meta = pipeline_pb2.Pipeline()
        self.meta.namespace = namespace
        self.meta.name = name
        self.meta.description = description
        self.enable_cache: bool = enable_cache
        self.hooks = hooks

        self.additional_args: Dict[str, str] = dict(kwargs).get(
            "additional_args", {}
        )
        self.components: List[Component] = components

    @property
    def components(self) -> List[Component]:
        return self._components

    @components.setter
    def components(self, components: List[Component]):
        """
        combine a running DAG map based on component channel parameters
        """
        uniq_components = set(components)  # remove duplicaton
        component_id_map: Dict[str, Component] = {}
        producer_map: Dict[Channel, Component] = {}

        for component in uniq_components:
            if component.id in component_id_map:
                raise RuntimeError(
                    "duplicated component type %s'' " % component.type
                )

            component_id_map[component.id] = component

            for name, output_channel in component.outputs.items():
                assert not producer_map.get(output_channel), (
                    "%s produce multiple times" % output_channel
                )
                producer_map[output_channel] = component

                for artifact in output_channel.get():
                    artifact.meta.name = (
                        artifact.meta.name or name
                    )  # 如果artifact 没有name，则赋予默认值
                    artifact.meta.producer_component = component.id

        for component in uniq_components:
            for i in component.inputs.values():
                if producer_map.get(i):
                    component.add_preorder(producer_map[i])
                    producer_map[i].add_postorder(component)

        self._components = []

        # topo sort, check cycle
        visited = set()
        current_layer = [c for c in components if not c.preorders]
        while current_layer:
            next_layer = []
            current_layer.sort(key=lambda comp: comp.id)
            for component in current_layer:
                self._components.append(component)
                visited.add(component)

                for postorder in component.postorders:
                    if postorder.preorders.issubset(visited):
                        next_layer.append(postorder)
            current_layer = next_layer

        if len(self._components) < len(components):
            raise RuntimeError("cycle exists in pipeline")

    def get_pipeline_dag(self):
        """
        将 pipeline.py 文件定义的 Pipeline 中的节点依赖关系 nodes 结构数组
        """
        nodes = []
        for component in self.components:
            nodes.append(
                {
                    "component": component.id,
                    "children": [child.id for child in component.postorders],
                    "inputs:": [
                        {"name": key, "type": channel.type_name}
                        for key, channel in component.inputs.items()
                    ],
                    "outputs": [
                        {"name": key, "type": channel.type_name}
                        for key, channel in component.outputs.items()
                    ],
                    "exec_properties": {
                        key: str(val)
                        for key, val in component.exec_properties.items()
                    },
                }
            )
        return nodes
