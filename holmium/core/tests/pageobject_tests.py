import unittest
import holmium.core
import mock
import selenium.webdriver
class PageObjectTest(unittest.TestCase):
    class BasicPage(holmium.core.PageObject):
        element = holmium.core.PageElement( holmium.core.Locators.ID, "test_id" )
    def test_basic_po(self):
        with mock.patch('selenium.webdriver.Firefox') as driver:
            with mock.patch('selenium.webdriver.remote.webelement.WebElement') as element:
                element.tag_name = "div"
                element.text = "test_text"
                driver.find_element.return_value = element
                po = PageObjectTest.BasicPage( driver , iframe = 'some_frame')
                self.assertEquals( "test_text",  po.element.text)

    def test_basic_po_real(self):
        driver = selenium.webdriver.PhantomJS()
        driver.execute_script('document.write("%s");' % """<body><div id='test_id'>test_text</div></body>""")
        po = PageObjectTest.BasicPage(driver)
        self.assertEquals(po.element.text, "test_text")
