import unittest

import mock
from selenium.webdriver.support.ui import Select

from holmium.core import Element, ElementEnhancer, Locators, Page, register_enhancer


class ElementEnhancerTest(unittest.TestCase):
    def setUp(self):
        self.driver = mock.Mock()

    def test_builtin_enhancer(self):
        class SimplePage(Page):
            id_el = Element(Locators.ID, "simple_id")

        self.driver.find_element.return_value.tag_name = "select"
        self.driver.find_element.return_value.text = "foo"
        self.driver.find_element.return_value.is_displayed = lambda: True
        p = SimplePage(self.driver)
        self.assertTrue(isinstance(p.id_el, Select))
        self.assertTrue(isinstance(p.id_el, ElementEnhancer))
        self.assertRaises(AttributeError, lambda: p.id_el.jump)
        self.assertEqual(p.id_el.text, "foo")
        self.assertTrue(p.id_el.is_displayed())

    def test_custom_enhancer(self):
        class DivEnhancer(ElementEnhancer):
            __TAG__ = "div"

            def get_class(self):
                return self.element.get_attribute("class")

        register_enhancer(DivEnhancer)

        class SimplePage(Page):
            id_el = Element(Locators.ID, "simple_id")

        find_element = self.driver.find_element
        find_element.return_value.tag_name = "div"
        find_element.return_value.text = "foo"
        find_element.return_value.get_attribute.return_value = "div-class"

        p = SimplePage(self.driver)

        self.assertEqual(p.id_el.get_class(), "div-class")

    def test_register(self):
        class BadCls:
            pass

        class Almost(ElementEnhancer):
            pass

        self.assertRaises(TypeError, register_enhancer, "test")
        self.assertRaises(TypeError, register_enhancer, BadCls)
        self.assertRaises(AttributeError, register_enhancer, Almost)
