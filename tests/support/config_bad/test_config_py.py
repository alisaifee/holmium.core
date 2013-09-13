import unittest
class TestConfigBad(unittest.TestCase):
    def test_config_bad(self):
        self.assertTrue(self.config["tvar"], 1)
