"""Tests for bmlx.utils.json_utils."""

import unittest
from bmlx.utils import json_utils


class _DefaultJsonableObject(json_utils.Jsonable):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c


class JsonUtilsTest(unittest.TestCase):
    def testDumpsJsonableObjectRoundtrip(self):
        obj = _DefaultJsonableObject(1, {"a": "b"}, [True])

        json_text = json_utils.dumps(obj)

        actual_obj = json_utils.loads(json_text)
        self.assertEqual(1, actual_obj.a)
        self.assertDictEqual({"a": "b"}, actual_obj.b)
        self.assertCountEqual([True], actual_obj.c)

    def testDumpsNestedClass(self):
        obj = _DefaultJsonableObject(_DefaultJsonableObject, None, None)

        json_text = json_utils.dumps(obj)

        actual_obj = json_utils.loads(json_text)
        self.assertEqual(_DefaultJsonableObject, actual_obj.a)
        self.assertIsNone(actual_obj.b)
        self.assertIsNone(actual_obj.c)

    def testDumpsClass(self):
        json_text = json_utils.dumps(_DefaultJsonableObject)

        actual_obj = json_utils.loads(json_text)
        self.assertEqual(_DefaultJsonableObject, actual_obj)
