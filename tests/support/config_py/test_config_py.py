import unittest
class TestConfigPy(unittest.TestCase):
    def test_config_py(self):
        self.assertTrue(self.config["tvar"], 1)
