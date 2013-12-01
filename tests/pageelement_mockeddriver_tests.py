import unittest
import mock
from  holmium.core import Page, Element, Locators
from selenium.webdriver.support.ui import Select


class ElementWithMockDriverTest(unittest.TestCase):

    def setUp(self):
        self.driver = mock.Mock()

    def test_enhanced_elements(self):
        class SimplePage(Page):
            id_el = Element(Locators.ID, "simple_id")
        self.driver.find_element.return_value.tag_name = "select"
        self.assertTrue(isinstance(SimplePage(self.driver).id_el, Select))


    def test_set_home_after_init(self):
        self.driver.current_url = None
        class SimplePage(Page):
            id_el = Element(Locators.ID, "simple_id")

        page = SimplePage(self.driver)
        self.assertEqual(page.home, None)
        self.driver.current_url = "http://www.google.com"
        self.driver.find_element.return_value.text = "simple"
        # when accessing an element, the home parameter should be updated
        self.assertEqual(page.id_el.text, "simple")
        self.assertEqual(page.home, "http://www.google.com")
        self.assertEqual(self.driver.get.call_count, 0)
        page.go_home()
        self.assertTrue(self.driver.get.call_count, 1)




