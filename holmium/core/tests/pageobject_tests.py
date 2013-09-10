import unittest
import holmium.core
import mock
import selenium.webdriver
class PageTest(unittest.TestCase):
    class BasicPage(holmium.core.Page):
        element = holmium.core.Element( holmium.core.Locators.ID, "test_id" )
        elist = [holmium.core.Element(holmium.core.Locators.ID, "test_id")]
        emap= {"test_id": holmium.core.Element(holmium.core.Locators.ID, "test_id")}
    def test_basic_po(self):
        with mock.patch('selenium.webdriver.Firefox') as driver:
            with mock.patch('selenium.webdriver.remote.webelement.WebElement') as element:
                element.tag_name = "div"
                element.text = "test_text"
                driver.find_element.return_value = element
                po = PageTest.BasicPage( driver , iframe = 'some_frame')
                self.assertEquals( "test_text",  po.element.text)

    def test_basic_po_real(self):
        driver = selenium.webdriver.PhantomJS()
        driver.execute_script('document.write("%s");' % """<body><div id='test_id'>test_text</div></body>""")
        po = PageTest.BasicPage(driver)
        self.assertEquals(po.element.text, "test_text")

    def test_multiple_po_instances(self):
        d1,d2=mock.Mock(), mock.Mock()
        e1,e2=mock.Mock(), mock.Mock()
        e1.tag_name = "div"
        e1.text = "test_text 1"
        e2.tag_name = "div"
        e2.text = "test_text 2"
        d1.find_element.return_value = e1
        d2.find_element.return_value = e2
        p1 = PageTest.BasicPage( d1 , iframe = 'some_frame')
        p2 = PageTest.BasicPage( d2 , iframe = 'some_frame')

        self.assertEquals(p1.element.text, "test_text 1")
        self.assertEquals(p2.element.text, "test_text 2")

        self.assertEquals(p1.elist[0].text, "test_text 1")
        self.assertEquals(p2.elist[0].text, "test_text 2")

        self.assertEquals(p1.emap["test_id"].text, "test_text 1")
        self.assertEquals(p2.emap["test_id"].text, "test_text 2")
