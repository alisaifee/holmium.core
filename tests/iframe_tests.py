import mock
import unittest
from  holmium.core import Page, Element, Locators
import selenium.webdriver


class IFrameTest(unittest.TestCase):
    class BasicPageIframe(Page):
        element = Element( Locators.ID, "test_id" )
        element2 = Element( Locators.ID, "test_id" )
    def test_basic_po(self):
        with mock.patch('selenium.webdriver.Firefox') as driver:
            with mock.patch('selenium.webdriver.remote.webelement.WebElement') as element:
                element.tag_name = "div"
                element.text = "test_text"
                driver.find_element.return_value = element
                po = IFrameTest.BasicPageIframe( driver , iframe='frame')
                self.assertEquals( "test_text",  po.element.text)
                self.assertEquals( "test_text",  po.element2.text)
                driver.switch_to_frame.assert_called_with("frame")
                self.assertEquals(driver.switch_to_frame.call_count, 3)
                self.assertEquals(driver.switch_to_default_content.call_count, 2)
