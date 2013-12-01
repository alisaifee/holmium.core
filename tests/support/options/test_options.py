import unittest
import holmium.core

class TestOptions(unittest.TestCase):
    def test_browser_set(self):
        self.assertEqual(self.driver.name, "remote")
    def test_remote_set(self):
        self.config["remote"] = "{{holmium.remote}}"
        self.assertEqual(self.config["remote"], 'http://nowhere.org')

    def test_useragent_set(self):
        self.config["user_agent"] = "{{holmium.user_agent}}"
        self.assertEqual(self.config["user_agent"], '"test useragent"')

