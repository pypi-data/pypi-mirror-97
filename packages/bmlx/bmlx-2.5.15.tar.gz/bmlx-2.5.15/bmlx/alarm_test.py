import unittest
from bmlx.config import Configuration, ConfigSource
from bmlx.alarm import Alarm, AlarmManager, Level
from bmlx.flow import Hook


class MockAlert(Hook):
    pass


class MockMeta(object):
    id = "56baa084-24b9-427a-b0a7-f8824080b9e4"
    name = "test_meta"


class MockPipeline(object):
    meta = MockMeta()


class MockPipelineExecution(object):
    id = 100


class MockContext(object):
    workflow_id = "1a8e08cb-ffe0-4441-ba4e-a025591995a6"
    env = "prod"


class MockProject(object):
    def resolve_project_path(self, path):
        return path


class AlarmManagerTest(unittest.TestCase):
    def setUp(self):
        self.mock_config = Configuration()
        self.mock_config.add(
            ConfigSource(
                {
                    "entry": "alarm_test.MockAlert",
                    "receipts": [
                        {
                            "type": "wxwork",
                            "receivers": [
                                {
                                    "url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=08c44667-d5e0-4b61-aec0-f39216c5fd57",
                                    "mentioned_list": ["00279"],
                                }
                            ],
                        },
                        {
                            "type": "mail",
                            "receivers": ["someone-not-in-bigo@bigo.sg"],
                        },
                    ],
                    "notifications": [
                        {"level": "warning", "receipts": ["mail"]},  #
                    ],
                }
            )
        )

    def testConfigParse(self):
        am = AlarmManager.load_from_config(MockProject(), self.mock_config)
        mock_pipeline = MockPipeline()
        mock_context = MockContext()
        mock_pipeline_execution = MockPipelineExecution()
        am.emit_alarms(
            [
                Alarm(
                    Level.WARNING,
                    {
                        "context": mock_context,
                        "pipeline": mock_pipeline,
                        "pipeline_execution": mock_pipeline_execution,
                        "message": "test alert with newline\nnewline\nnewline",
                    },
                )
            ]
        )
