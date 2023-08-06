from typing import Text, List, Dict
from bmlx.utils import naming_utils


# bmlx 里面 一个 component 对应一个node，一个node 对应一个 argo的template，同时对应一个 dag template 中的dag task
class ArgoNode(object):
    def __init__(
        self,
        name: Text,
        image: Text,
        command: Text,
        args: List[Text] = [],
        labels: Dict[Text, Text] = {},
        metrics=None,
    ):
        if not naming_utils.is_valid_argo_name(name):
            raise ValueError(
                "Invalid argo name %s for template, name should be match with pattern %s",
                name,
                naming_utils.argo_name_pattern(),
            )

        self._container = {"image": image, "command": [command], "args": args}
        self._template = {
            "name": name,
            "metrics": metrics,
            "metadata": {"labels": labels},
            "volumes": [],
            "container": self._container,
        }

        self.add_env_variable(
            {
                "name": "ARGO_POD_NAME",
                "valueFrom": {
                    "fieldRef": {
                        "apiVersion": "v1",
                        "fieldPath": "metadata.name",
                    }
                },
            }
        )

        self._dag_task = {
            "name": name,
            "template": self._template["name"],
            "dependencies": [],
        }

    @property
    def name(self):
        return self._template["name"]

    @property
    def container(self):
        return self._container

    def add_env_variable(self, env_variable):
        if self._container.get("env") is None:
            self._container["env"] = []
        self._container["env"].append(env_variable)

    def add_dependency(self, node):
        if not isinstance(node, ArgoNode):
            raise ValueError("depends_on should input Node parameters")
        if node.name in self._dag_task["dependencies"]:
            raise RuntimeError(
                "Duplicated depends, node %s depends on node %s for multiple times"
                % (self.name, node.name)
            )
        self._dag_task["dependencies"].append(node.name)

    def set_node_selector(self, node_selector):
        self._template["nodeSelector"] = node_selector

    def set_init_containers(self, init_containers):
        self._template["initContainers"] = init_containers

    def set_inputs(self, inputs):
        self._template["inputs"] = inputs

    def set_parallelism(self, parallelism):
        self._template["parallelism"] = parallelism

    def add_volume_mount(self, mnt):
        if self._container.get("volumeMounts") is None:
            self._container["volumeMounts"] = []
        self._container["volumeMounts"].append(mnt)

    def add_volume(self, vol):
        if self._template.get("volumes") is None:
            self._template["volumes"] = []
        self._template["volumes"].append(vol)

    def set_script(self, script):
        self._template["script"] = script

    def set_metrics(self, metrics):
        self._template["metrics"] = metrics

    @classmethod
    def gen_template_metrics(cls, pipeline_name, node_name):
        def _gen_labels():
            return [
                {"key": "bmlx_pipeline", "value": str(pipeline_name)},
                {
                    "key": "bmlx_experiment_name",
                    "value": "{{workflow.parameters.experiment_name}}",
                },
                {
                    "key": "bmlx_experiment_id",
                    "value": "{{workflow.parameters.experiment_id}}",
                },
                {
                    "key": "namespace",
                    "value": "{{workflow.parameters.namespace}}",
                },
                {
                    "key": "node_name",
                    "value": node_name,
                },
            ]

        return {
            "prometheus": [
                {
                    "name": "bmlx_comp_run_duration",
                    "help": "execution time of bmlx component",
                    "labels": _gen_labels(),
                    "gauge": {"value": "{{duration}}", "realtime": True},
                },
                {
                    "name": "bmlx_comp_run_fail",
                    "help": "bmlx component run fail counter",
                    "labels": _gen_labels(),
                    "when": "{{status}} == Failed",
                    "counter": {"value": "1"},
                },
                {
                    "name": "bmlx_comp_run_success",
                    "help": "bmlx component run success counter",
                    "labels": _gen_labels(),
                    "when": "{{status}} == Succeeded",
                    "counter": {"value": "1"},
                },
                {
                    "name": "bmlx_comp_run_error",
                    "help": "bmlx component run error counter",
                    "labels": _gen_labels(),
                    "when": "{{status}} == Error",
                    "counter": {"value": "1"},
                },
            ]
        }

    @property
    def template(self):
        return self._template

    @property
    def dag_task(self):
        return self._dag_task
