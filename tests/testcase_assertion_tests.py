"""

"""
import unittest
import os

import mock

from holmium.core import TestCase, Page, Element, Elements, ElementMap, Locators
from holmium.core.env import ENV
import holmium.core.testcase
from .utils import build_mock_mapping


def runtc(env, validations, validator = lambda c,s:c(s)):
    try:
        _pre_env = dict(os.environ)
        os.environ.update(env)
        class t(TestCase):

            def setUp(self):
                class P(Page):
                    e = Element(Locators.CLASS_NAME, "el")
                    es = Elements(Locators.CLASS_NAME, "el")
                    em = ElementMap(Locators.CLASS_NAME, "el")
                self.page = P(self.driver)
            def runTest(self):
                for validation in validations:
                    validator(validation, self)

        test = t()
        test.setUpClass()
        test.setUp()
        test.runTest()
        test.tearDown()
        test.tearDownClass()
    finally:
        os.environ = _pre_env

class TestCaseTests(unittest.TestCase):
    def setUp(self):
        ENV.clear()

    def test_assert_element_positive(self):
        with mock.patch.dict('holmium.core.testcase.BROWSER_MAPPING', build_mock_mapping("firefox")):
            driver_cls = holmium.core.testcase.BROWSER_MAPPING["firefox"]
            driver_cls.return_value.find_element.return_value = mock.Mock(
                text="foo", size={"width": 1, "height": 1},
                is_displayed=lambda: True, value_of_css_property=lambda p:"test")
            driver_cls.return_value.find_elements.return_value = [
                mock.Mock(text="foo", is_displayed=lambda:True),
                mock.Mock(text="bar", is_displayed=lambda:True)]
            validations = [
                lambda s: s.assertElementTextEqual(s.page.e, "foo"),
                lambda s: s.assertElementSize(s.page.e, 1,1),
                lambda s: s.assertElementCSS(s.page.e, "background-color", "test"),
                lambda s: s.assertElementDisplayed(s.page.e),
                lambda s: s.assertElementsDisplayed(s.page.es),
                lambda s: s.assertElementsDisplayed(s.page.em)
            ]
            runtc({"HO_BROWSER":"firefox"}, validations)

    def test_assert_element_negative(self):
        with mock.patch.dict('holmium.core.testcase.BROWSER_MAPPING', build_mock_mapping("firefox")):
            driver_cls = holmium.core.testcase.BROWSER_MAPPING["firefox"]
            driver_cls.return_value.find_element.return_value = mock.Mock(
                text="foobar", size={"width": 2, "height": 1},
                is_displayed=lambda: False, value_of_css_property=lambda p:"testing")
            driver_cls.return_value.find_elements.return_value = [
                mock.Mock(text="foo", is_displayed=lambda:False),
                mock.Mock(text="bar", is_displayed=lambda:False)]

            validations = [
                lambda s: s.assertElementTextEqual(s.page.e, "foo"),
                lambda s: s.assertElementSize(s.page.e, height=1,width=1),
                lambda s: s.assertElementCSS(s.page.e, "background-color", "test"),
                #lambda s: s.assertElementDisplayed(s.page.e),
                lambda s: s.assertElementsDisplayed(s.page.es),
                lambda s: s.assertElementsDisplayed(s.page.em)
            ]
            runtc({"HO_BROWSER": "firefox"}, validations,
                  validator=lambda c,s: s.assertRaises(AssertionError, c, s ))
