import unittest
import json
from bmlx.execution.bmlxflow import Workflow, ArgoNode


class FlowTest(unittest.TestCase):
    def setUp(self):
        pass

    def testCompileWorkflow(self):
        flow = Workflow(name="test-workflow")
        flow.set_image_pull_secrets(["secret1", "secret2"])
        node_a = ArgoNode(
            name="node_a",
            image="ubuntu16.04",
            command="bash",
            args=["-c", "echo", "hello node_a!"],
        )
        flow.add_node(node_a)
        node_b = ArgoNode(
            name="node_b",
            image="ubuntu16.04",
            command="bash",
            args=["-c", "echo", "hello node_b!"],
        )
        flow.add_node(node_b)
        node_b.add_dependency(node_a)
        node_c = ArgoNode(
            name="node_c",
            image="ubuntu16.04",
            command="bash",
            args=["-c", "echo", "hello node_c!"],
        )
        flow.add_node(node_c)
        node_c.add_dependency(node_a)
        node_c.add_dependency(node_b)

        spec = flow.compile()
        dct = json.loads(spec)
        self.assertTrue(dct["kind"], "Workflow")
        self.assertTrue(dct["metadata"]["name"], "test-workflow")
        self.assertTrue(dct["spec"]["entrypoint"], "test-workflow-entrypoint")
        self.assertTrue(dct["spec"]["imagePullSecrets"] == [{"name": "secret1"}, {"name": "secret2"}])
