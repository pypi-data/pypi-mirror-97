import unittest
from bmlx.flow import Artifact
from bmlx.proto.metadata import artifact_pb2
from bmlx.utils import json_utils


class FakeArtifact(Artifact):
    TYPE_NAME = "Fake"


class IllegalArtifact(Artifact):
    pass


class ArtifactTest(unittest.TestCase):
    def testNormalInit(self):
        self.assertIsInstance(FakeArtifact(), Artifact)

    def testArtifactCouldNotIntialize(self):
        self.assertRaises(ValueError, Artifact)

    def testNoTypeNameArtifactShouldNotCreate(self):
        self.assertRaises(ValueError, IllegalArtifact)

    def testInitializeSubclassWithTypeName(self):
        self.assertRaises(ValueError, FakeArtifact, type_name="self_def")

    def testJsonifyArtifact(self):
        fake_artifact = FakeArtifact(
            meta=artifact_pb2.Artifact(
                id=10, type="test-type", state=artifact_pb2.Artifact.State.LIVE
            )
        )
        json_text = json_utils.dumps(fake_artifact)
        actual_obj = json_utils.loads(json_text)
        self.assertEqual("Fake", actual_obj.type_name)
        self.assertEqual(10, actual_obj.meta.id)
        self.assertEqual("test-type", actual_obj.meta.type)
        self.assertEqual(
            artifact_pb2.Artifact.State.LIVE, actual_obj.meta.state
        )

    def testJsonifyBaseArtifact(self):
        test_artifact = Artifact(
            type_name="test-type",
            meta=artifact_pb2.Artifact(
                id=10,
                type="test-type-1",
                state=artifact_pb2.Artifact.State.LIVE,
            ),
        )
        json_text = json_utils.dumps(test_artifact)
        actual_obj = json_utils.loads(json_text)
        self.assertEqual("test-type", actual_obj.type_name)
        self.assertEqual(10, actual_obj.meta.id)
        self.assertEqual("test-type-1", actual_obj.meta.type)
        self.assertEqual(
            artifact_pb2.Artifact.State.LIVE, actual_obj.meta.state
        )
