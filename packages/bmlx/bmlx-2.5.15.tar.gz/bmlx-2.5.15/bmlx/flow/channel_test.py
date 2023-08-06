import unittest

from bmlx.flow import Artifact, Channel


class FakeChannelInput(Artifact):
    TYPE_NAME = "ChannelFake"


class FakeChannelNromalInput(Artifact):
    TYPE_NAME = "Fake"


class FakeArtifact(Artifact):
    TYPE_NAME = "Fake"


class ChannelTest(unittest.TestCase):
    def testIllegalInput(self):
        self.assertRaises(
            TypeError,
            Channel,
            type=FakeChannelInput,
            artifacts=[FakeArtifact()],
        )

    def testNormalInputType(self):
        Channel(
            artifact_type=FakeChannelNromalInput, artifacts=[FakeArtifact()]
        )
        Channel(type_name="Fake", artifacts=[FakeArtifact()])
        self.assertRaises(
            TypeError,
            Channel,
            type_name="illegal_name",
            artifacts=[FakeArtifact],
        )
        self.assertRaises(
            TypeError,
            Channel,
            type_name="Fake",
            artifacts=[Artifact(type_name="random_type")],
        )

    def testTypeAndNameShouldOnlySetOne(self):
        self.assertRaises(
            RuntimeError,
            Channel,
            artifact_type=FakeArtifact,
            type_name="type_name",
        )
