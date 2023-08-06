import yaml
import json
from typing import Text, List, Dict, Any
from bmlx.utils import yaml_utils, naming_utils
from bmlx.execution.bmlxflow import ArgoNode


class Dag(object):
    def __init__(self, name: Text):
        if not naming_utils.is_valid_argo_name(name):
            raise ValueError(
                "Invalid argo name %s for template, name should be match with pattern %s",
                name,
                naming_utils._ARGO_NAMING_RE,
            )
        self._name = name
        self._template = {"tasks": []}

    @property
    def name(self):
        return self._name

    def add_task(self, task):
        self._template["tasks"].append(task)

    @property
    def template(self):
        return self._template


class Workflow(object):
    def __init__(self, name: Text):
        if not naming_utils.is_valid_argo_name(name):
            raise ValueError(
                "Invalid argo name %s for template, name should be match with pattern %s",
                name,
                naming_utils.argo_name_pattern(),
            )
        self._name = name
        self._spec = {"entrypoint": f"{name}-entrypoint", "templates": []}
        self._exit_node = None
        self._metrics = None
        self._nodes = []

    def add_node(self, t: ArgoNode):
        if not isinstance(t, ArgoNode):
            raise ValueError("add_node should input Node parameter")
        self._nodes.append(t)

    def set_host_network(self, host_network):
        self._spec["hostNetwork"] = host_network

    def set_dns_policy(self, policy):
        self._spec["dnsPolicy"] = policy

    def set_dns_config(self, config):
        self._spec["dnsConfig"] = config

    def set_image_pull_secrets(self, secrets):
        if isinstance(secrets, str):
            secrets = [secrets]
        self._spec["imagePullSecrets"] = [
            {"name": secret} for secret in secrets or []
        ]

    def set_node_selector(self, selectors):
        self._sepc["nodeSelectors"] = selectors

    def set_exit_handler(self, t: ArgoNode):
        self._exit_node = t

    def set_metrics(self, m):
        self._metrics = m

    def arrange_nodes(self):
        if not self._nodes:
            raise RuntimeError("Should add_node before calling arrange_nodes")
        self._spec["templates"] = []
        dag = Dag(name=self._name)
        for node in self._nodes:
            self._spec["templates"].append(node.template)
            dag.add_task(node.dag_task)
        # generate entry point template
        tmplt = {"name": f"{dag.name}-entrypoint", "dag": dag.template}
        self._spec["templates"].append(tmplt)

        if self._exit_node:
            self._spec["templates"].append(self._exit_node.template)
            self._spec["onExit"] = self._exit_node.name
        if self._metrics:
            self._spec["metrics"] = self._metrics

    @classmethod
    def gen_workflow_metrics(cls, pipeline_name):
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
            ]

        return {
            "prometheus": [
                {
                    "name": "bmlx_exp_run_duration",
                    "help": "execution time of bmlx pipeline",
                    "labels": _gen_labels(),
                    "gauge": {
                        "value": "{{workflow.duration}}",
                        "realtime": True,
                    },
                },
                {
                    "name": "bmlx_exp_run_fail",
                    "help": "bmlx pipeline execution fail counter",
                    "labels": _gen_labels(),
                    "when": "{{workflow.status}} == Failed",
                    "counter": {"value": "1"},
                },
                {
                    "name": "bmlx_exp_run_success",
                    "help": "bmlx pipeline execution success counter",
                    "labels": _gen_labels(),
                    "when": "{{workflow.status}} == Succeeded",
                    "counter": {"value": "1"},
                },
                {
                    "name": "bmlx_exp_run_error",
                    "help": "bmlx pipeline execution error counter",
                    "labels": _gen_labels(),
                    "when": "{{workflow.status}} == Error",
                    "counter": {"value": "1"},
                },
            ]
        }

    @property
    def workflow(self):
        self.arrange_nodes()
        workflow = {
            "apiVersion": "argoproj.io/v1alpha1",
            "kind": "Workflow",
            "metadata": {"name": self._name},
            "spec": self._spec,
        }
        return workflow

    def compile(self):
        return self.to_json()

    def to_json(self, omitempty=True, **kwargs) -> str:
        """Returns the Workflow manifest as a YAML."""
        opts = dict(default_flow_style=False)
        opts.update(kwargs)
        serialized = json.dumps(self.workflow, indent=2, sort_keys=True)
        return serialized
