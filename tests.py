import decimal
import os
from unittest import TestCase

from envanter import env


class TestEnvironmentParser(TestCase):
    def test_parser(self):
        os.environ["string"] = "Hello"
        os.environ["int"] = "6"
        os.environ["float"] = "3.14"
        os.environ["decimal"] = "2.71"
        os.environ["json"] = '{"hello": "world"}'

        self.assertEqual("Hello", env.str("string"))
        self.assertEqual(6, env.int("int"))
        self.assertEqual(3.14, env.float("float"))
        self.assertEqual(decimal.Decimal("2.71"), env.decimal("decimal"))
        self.assertEqual({"hello": "world"}, env.json("json"))

    def test_parse_list(self):
        os.environ["list1"] = "hi,hello,whatsup"
        os.environ["list2"] = "hi?hello?whatsup"

        lst = ["hi", "hello", "whatsup"]
        self.assertEqual(lst, env.list("list1"))
        self.assertEqual(lst, env.list("list2", delimiter="?"))

    def test_parse_bool(self):
        os.environ["bool_1"] = "1"
        os.environ["bool_0"] = "0"

        os.environ["bool_true"] = "true"
        os.environ["bool_false"] = "false"

        os.environ["bool_true_2"] = "True"
        os.environ["bool_false_2"] = "False"

        self.assertTrue(env.bool("bool_1"))
        self.assertTrue(env.bool("bool_true"))
        self.assertTrue(env.bool("bool_true_2"))

        self.assertFalse(env.bool("bool_0"))
        self.assertFalse(env.bool("bool_false"))
        self.assertFalse(env.bool("bool_false_2"))

        os.environ["bad_bool"] = "nope"
        with self.assertRaises(AssertionError):
            env.bool("bad_bool")

    def test_required(self):
        with self.assertRaises(KeyError):
            env.str("envanter_test_with_default")

        self.assertTrue(env.bool("envanter_test_with_default", True))
        self.assertFalse(env.bool("envanter_test_with_default", False))

        self.assertEqual(
            "hello",
            env.str("envanter_test_with_default", "hello"),
        )
        self.assertEqual(True, env.str("envanter_test_with_default", True))

    def test_parse_custom(self):
        os.environ["number_2"] = "2"
        self.assertEqual(3, env.parse("number_2", parser=lambda i: int(i) + 1))
