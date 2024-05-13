import unittest
from unittest.mock import patch
import config as pcfg

TEST_TOML = """
[cfg1]
key1 = "value1"
key2 = "value2"
[cfg2]
key1 = "value1"
key2 = "value2"
num = 1
"""


class ProjConfigTests(unittest.TestCase):

    @patch("builtins.open")
    def test_load(self, mock_open):
        # mock open to return a file object with the test toml data as bytes
        mock_open.return_value.__enter__.return_value.read.return_value = bytes(TEST_TOML, "utf-8")
        # load the config
        pcfg.load("test.toml")
        cfg1_data = pcfg.get_config("cfg1")
        cfg2_data = pcfg.get_config("cfg2")
        # check the config data
        self.assertEqual(cfg1_data.key1, "value1")
        self.assertEqual(cfg1_data.key2, "value2")
        self.assertEqual(cfg2_data.key1, "value1")
        self.assertEqual(cfg2_data.key2, "value2")
        self.assertEqual(cfg2_data.num, 1)

    @patch("builtins.open")
    def test_get(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = bytes(TEST_TOML, "utf-8")
        pcfg.load("test.toml")
        # check the config data
        self.assertEqual(pcfg.get("cfg1", "key1"), "value1")
        self.assertEqual(pcfg.get("cfg1", "key2"), "value2")
        self.assertEqual(pcfg.get("cfg2", "key1"), "value1")
        self.assertEqual(pcfg.get("cfg2", "key2"), "value2")
        self.assertEqual(pcfg.get("cfg2", "num"), 1)
        self.assertRaises(AttributeError, pcfg.get, "cfg3", "key1")

    @patch("builtins.open")
    def test_get_config_file_name(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = bytes(TEST_TOML, "utf-8")
        pcfg.load("test.toml")
        self.assertEqual(pcfg.get_config_file_name(), "test.toml")
