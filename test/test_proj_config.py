## Add MIT License
# -*- coding: utf-8 -*-
# File: test_proj_config.py
"""Test the ProjConfig class."""
import unittest
from unittest.mock import patch
import py_proj_config.config as pcfg

TEST_TOML = """
[cfg1]
key1 = "value1"
key2 = "value2"
[cfg2]
key1 = "value1"
key2 = "value2"
num = 1
[cfg3]
row1.key1 = "11"
row1.key2 = "12"
row2.key1 = "21"
row2.key2 = "22"
"""


class ProjConfigCreateTests(unittest.TestCase):

    def test_create(self):
        cfg = pcfg.ProjConfig()
        self.assertIsNone(cfg.config_file)
        self.assertIsNone(cfg.config)
        self.assertEqual(cfg.data, {})


class ProjConfigTests(unittest.TestCase):

    @patch("builtins.open")
    def setUp(self, mock_open) -> None:
        """Set up the test case by loading the config. from the TEST_TOML string."""
        mock_open.return_value.__enter__.return_value.read.return_value = bytes(TEST_TOML, "utf-8")
        pcfg.ProjConfig.load_from_toml("test.toml")

    def test_load(self):
        """Test the config loading."""
        cfg = pcfg.ProjConfig()
        self.assertEqual(cfg.config_file, "test.toml")
        # load the config
        cfg.config = "cfg1"
        cfg1_data = cfg.config
        # check the config data
        self.assertEqual(cfg1_data.get_name(), "cfg1")
        self.assertEqual(cfg1_data.key1, "value1")
        self.assertEqual(cfg1_data.key2, "value2")
        # check the second config
        with self.assertWarns(pcfg.ProjConfigChangedWarning) as cm:
            cfg.config = "cfg2"
        cfg2_data = cfg.config
        # check the second config data
        self.assertEqual(cfg.config.get_name(), "cfg2")
        self.assertEqual(cfg2_data.key1, "value1")
        self.assertEqual(cfg2_data.key2, "value2")
        self.assertEqual(cfg2_data.num, 1)
        # check the third config
        with self.assertWarns(pcfg.ProjConfigChangedWarning) as cm:
            cfg.config = "cfg3"
        cfg3_data = cfg.config
        # check the third config data
        self.assertEqual(cfg.config.get_name(), "cfg3")
        self.assertEqual(cfg3_data.row1.key1, "11")
        self.assertEqual(cfg3_data.row1.key2, "12")
        self.assertEqual(cfg3_data.row2.key1, "21")
        self.assertEqual(cfg3_data.row2.key2, "22")

    def test_get_config(self):
        cfg = pcfg.ProjConfig()
        self.assertIsNone(cfg.config)
        cfg.config = "cfg1"
        self.assertIsNotNone(cfg.config)
        self.assertEqual(pcfg.get_config(), cfg.config)
