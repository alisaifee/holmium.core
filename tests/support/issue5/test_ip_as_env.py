import unittest


class NoseConfigTest(unittest.TestCase):
    def test_config_available(self):
        self.assertTrue(self.config != None)
    def test_config_env_value(self):
        self.assertEqual(self.config["var"], 1)
    def test_config_default_value(self):
        self.assertEqual(self.config["foo"], 2)
