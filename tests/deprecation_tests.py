import unittest
import holmium.core


class DeprecatedPageTest(unittest.TestCase):
    def test_basic_po(self):
        self.assertRaises(SyntaxError, holmium.core.PageObject)
        self.assertRaises(SyntaxError, holmium.core.PageElement)
        self.assertRaises(SyntaxError, holmium.core.PageElements)
        self.assertRaises(SyntaxError, holmium.core.PageElementMap)
        self.assertRaises(SyntaxError, holmium.core.HolmiumTestCase)
