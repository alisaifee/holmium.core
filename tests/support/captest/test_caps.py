import unittest

class TestCaps(unittest.TestCase):
    def test_caps_from_file(self):
        self.assertFalse(self.driver.capabilities['javascriptEnabled'])
