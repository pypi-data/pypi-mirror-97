import unittest
import json
from bmlx.flow import Artifact
from bmlx.proto.metadata import artifact_pb2
from bmlx.execution.execution import ExecutionInfo
from bmlx.utils import json_utils


class Artifact_A(Artifact):
    TYPE_NAME = "artifact_a"


class Artifact_B(Artifact):
    TYPE_NAME = "artifact_b"


class Artifact_C(Artifact):
    TYPE_NAME = "artifact_c"


class ExecutionInfoTest(unittest.TestCase):
    def setUp(self):
        input_a = Artifact_A(
            meta=artifact_pb2.Artifact(
                id=10,
                name="input-a",
                type="artifact_a",
                state=artifact_pb2.Artifact.State.LIVE,
            )
        )

        input_b = Artifact_B(
            meta=artifact_pb2.Artifact(
                id=12,
                name="input-b",
                type="artifact_b",
                state=artifact_pb2.Artifact.State.LIVE,
            )
        )

        output_c = Artifact_C(
            meta=artifact_pb2.Artifact(
                id=14,
                name="output-c",
                type="artifact_c",
                state=artifact_pb2.Artifact.State.LIVE,
            )
        )
        self.input_dict = {"input_a": input_a, "input_b": input_b}
        self.output_dict = {"output_c": output_c}
        self.exec_properties = {"job_id": "this-is-a-test-job-id"}
        self.use_cached_result = True

    def testJsonifyExecutionInfo(self):
        execution_info = ExecutionInfo(
            input_dict=self.input_dict,
            output_dict=self.output_dict,
            exec_properties=self.exec_properties,
            use_cached_result=self.use_cached_result,
        )
        json_text = json_utils.dumps(execution_info)
        info = json_utils.loads(json_text)
        self.assertEqual(info.use_cached_result, True)
        self.assertEqual(info.input_dict["input_a"].meta.type, "artifact_a")
        # self.assertDictEqual(info.exec_properties, self.exec_properties)
