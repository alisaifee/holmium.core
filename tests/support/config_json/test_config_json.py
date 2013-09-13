import unittest

class TestConfigJson(unittest.TestCase):
    def test_config_json(self):
        self.assertTrue(self.config["tvar"], 1)
