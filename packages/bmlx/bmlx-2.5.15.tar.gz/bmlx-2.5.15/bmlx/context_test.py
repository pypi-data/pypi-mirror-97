import unittest
from bmlx.context import BmlxContext
from bmlx import config as bmlx_config


class BmlxContextTest(unittest.TestCase):
    def testRewriteCustomParameters(self):
        ctx = BmlxContext()

        ctx.custom_parameters = bmlx_config.Configuration()
        ctx.custom_parameters.set_args(
            {
                "model.learning_rate.decay_type": "sin",
                "model.keep_hour": 200,
                "model.arch": "before_valid",
                "model.arch_options.nextvald.gating_resu": 8,
            }
        )
        params = {
            "bmlx.parameters.model.learning_rate.decay_type": "cosine",
            "bmlx.parameters.sample-selector.max-sample-hours": 100,
            "model.keep_hour": 10,
            "model.arch": "nextvald",
        }
        self.assertEqual(
            ctx.custom_parameters["model"]["arch"].as_str(), "before_valid"
        )
        ctx.rewrite_custom_parameters(params)
        self.assertTrue(
            ctx.custom_parameters["model"]["learning_rate"][
                "decay_type"
            ].exists()
        )
        self.assertEqual(
            ctx.custom_parameters["model"]["learning_rate"][
                "decay_type"
            ].as_str(),
            "cosine",
        )
        self.assertEqual(
            ctx.custom_parameters["model"]["keep_hour"].as_number(), 10
        )
        self.assertEqual(
            ctx.custom_parameters["model"]["arch"].as_str(), "nextvald"
        )
