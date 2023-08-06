import unittest
import yaml
from string import Template
from bmlx import config


class ConfigTest(unittest.TestCase):
    def testRender(self):
        d = {"a": "b", "c": "d"}
        tpl = Template("${a}_${c}")
        conf = config.RootView([d])
        ret = conf.render(tpl)
        self.assertEqual(ret, "b_d")

    def testOrderedYaml(self):
        d = '{"c": "1", "b": "2", "d": 3}'
        m = yaml.load(d, Loader=config.Loader)
        raw_test = yaml.dump(data=m, Dumper=config.Dumper)
        self.assertEqual(raw_test, "c: '1'\nb: '2'\nd: 3\n")

    def testAsDict(self):
        val = {
            "a": None,
            "b": 0,  # logic error not as nil
            "c": False,
            "d": ["hello", "world"],
            "e": {"a": "c"},
        }
        conf = config.RootView([val])
        self.assertTrue(conf["e"].exists())
        dct = conf["e"].get(dict)
        self.assertEqual(dct["a"], "c")

    def testAsList(self):
        val = {
            "students": [
                {"name": "jason", "age": 15},
                {"name": "tom", "age": 12},
            ]
        }
        conf = config.RootView([val])
        self.assertTrue(conf["students"].exists())
        sts = conf["students"].get(list)
        self.assertEqual(len(sts), 2)
        self.assertEqual(sts[0]["name"], "jason")

    def testNoneAsExists(self):
        a = {
            "a": None,
            "b": 0,  # logic error not as nil
            "c": False,
            "d": [],
            "e": {},
        }
        conf = config.RootView([a])
        self.assertTrue(conf["a"].exists())
        self.assertTrue(conf["b"].exists())
        self.assertTrue(conf["c"].exists())
        self.assertTrue(conf["d"].exists())

    def testRelativeTo(self):
        a = {"rel": "./foo", "abs": "/bar", "remote_rel": "hdfs://bigo-rt/foo"}
        conf = config.RootView([a])
        conf.relatives = {
            "base_path": "/base/root",
        }

        self.assertEqual(
            conf["rel"].as_filename(relative_to="base_path"), "/base/root/foo"
        )
        self.assertEqual(
            conf["abs"].as_filename(relative_to="base_path"), "/bar"
        )
        self.assertEqual(
            conf["remote_rel"].as_filename(relative_to="base_path"),
            "hdfs://bigo-rt/foo",
        )
        self.assertRaises(
            KeyError, conf["rel"].as_filename, relative_to="non_exists"
        )

    def testSetArgs(self):
        a = {"ref": {"a", "b"}, "refb": "hello"}
        conf = config.RootView([a])

        conf.set_args({"ref.a": "c", "refb": "world"})
        self.assertEqual(conf["ref"]["a"].as_str(), "c")
        self.assertEqual(conf["refb"].as_str(), "world")

    def testSetArgs2(self):
        a = {"ref": {"a", "b"}, "refb": "hello", "refc": "hello-world"}
        conf = config.RootView([a])
        conf["ref"]["a"] = "c"
        conf["refb"] = "world"
        self.assertEqual(conf["ref"]["a"].as_str(), "c")
        self.assertEqual(conf["refb"].as_str(), "world")
        self.assertEqual(conf["refc"].as_str(), "hello-world")

    def testConfigurationWithSpecificValueConverter(self):
        a = {
            "ref": {"a", "b"},
            "refb": "hello",
            "refc": {
                "description": "this is refc",
                "validator": {},
                "value": "hello-world",
            },
            "refd": 10,
            "refe": {
                "refee": {
                    "description": "this is refc",
                    "validator": {},
                    "value": 20,
                }
            },
        }
        conf = config.RootView(
            [a],
            value_converter=lambda x: x["value"]
            if isinstance(x, dict) and "value" in x
            else x,
        )
        conf["ref"]["a"] = "c"
        conf["refb"] = "world"
        self.assertEqual(conf["ref"]["a"].as_str(), "c")
        self.assertEqual(conf["refb"].as_str(), "world")
        self.assertEqual(conf["refc"].as_str(), "hello-world")
        self.assertEqual(conf["refd"].as_number(), 10)
        self.assertEqual(conf["refe"]["refee"].as_number(), 20)
