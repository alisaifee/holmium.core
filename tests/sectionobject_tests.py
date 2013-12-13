import unittest
from holmium.core import Locators, Page, Elements, Section, Sections
import mock
from tests.utils import get_driver, make_temp_page


class BasicSection(Section):
    tokens = Elements(Locators.CSS_SELECTOR,
                                   "div.token")


class BasicSectionList(Sections):
    tokens = Elements(Locators.CSS_SELECTOR,
                                   "div.token")


class BasicPage(Page):
    section = BasicSection(Locators.ID, "section")
    section_2 = BasicSection(Locators.ID, "section_2")
    tokens = Elements(Locators.CLASS_NAME, "token")


class BasicPageWithSections(Page):
    sections = BasicSectionList( Locators.CLASS_NAME, "section", timeout=1)
    missing_sections = BasicSectionList( Locators.CLASS_NAME, "missing_section", timeout=1)

class SectionTest(unittest.TestCase):

    def test_basic_po_real(self):
        driver = get_driver()
        page = """
        <body>
            <div id='section'>
                <div class='token'>
                    <div class='el'>
                        section element 1
                    </div>
                </div>
                <div class='token'>
                    <div class='el'>
                        section element 2
                    </div>
                </div>
            </div>
            <div id='section_2'>
                <div class='token'>
                    <div class='el'>
                        section element 3
                    </div>
                </div>
                <div class='token'>
                    <div class='el'>
                        section element 4
                    </div>
                </div>
            </div>
            <span class='token'>
                <div class='el'>
                    element 5
                </div>
            </span>
        </body>
        """
        uri = make_temp_page(page.strip())
        po = BasicPage(driver, uri)
        self.assertEqual(len(po.tokens), 5)
        self.assertEqual(len(po.section.tokens), 2)
        self.assertEqual(len(po.section_2.tokens), 2)
        for i in range(0, 2):
            self.assertEqual(po.section.tokens[i].text,
                              "section element %s" % (i + 1))
        for i in range(0, 2):
            self.assertEqual(po.section_2.tokens[i].text,
                              "section element %s" % (i + 3))
        self.assertEqual(po.tokens[0].text, 'section element 1')
        self.assertEqual(po.tokens[1].text, 'section element 2')
        self.assertEqual(po.tokens[2].text, 'section element 3')
        self.assertEqual(po.tokens[3].text, 'section element 4')

    def test_basic_po_with_sections(self):
        driver = get_driver()
        page = """
        <body>
            <div class='section'>
                <div class='token'>
                    <div class='el'>
                        section element 1
                    </div>
                </div>
                <div class='token'>
                    <div class='el'>
                        section element 2
                    </div>
                </div>
            </div>
            <div class='section'>
                <div class='token'>
                    <div class='el'>
                        section element 3
                    </div>
                </div>
                <div class='token'>
                    <div class='el'>
                        section element 4
                    </div>
                </div>
            </div>
        </body>
        """
        uri = make_temp_page(page.strip())
        po = BasicPageWithSections(driver, uri)
        counter = 1
        for section in po.sections:
            for token in section.tokens:
                self.assertEqual(token.text, "section element %s" % counter)
                counter += 1
        self.assertEqual(len(po.sections), 2)
        self.assertRaises(IndexError, lambda: po.sections[2])
        self.assertRaises(IndexError, lambda: po.missing_sections[0])

    def test_sections_list_behavior(self):
        with mock.patch('selenium.webdriver.Firefox') as driver:
            element1, element2 = mock.Mock(), mock.Mock()
            element1.tag_name = element2.tag_name = "div"
            element1.text = "element 1"
            element2.text = "element 2"
            element3, element4 = mock.Mock(), mock.Mock()
            element3.tag_name = element4.tag_name = "div"
            element3.text = "element 3"
            element4.text = "element 4"
            driver.find_elements.return_value = [element1, element2]
            element1.find_elements.return_value = [element3, element4]
            element2.find_elements.return_value = [element4, element3]
            po = BasicPageWithSections(driver)
            self.assertEqual("element 3", po.sections[0].tokens[0].text)
            self.assertEqual("element 4", po.sections[1].tokens[0].text)
            self.assertEqual("element 4", po.sections[0].tokens[1].text)
            self.assertEqual("element 3", po.sections[1].tokens[1].text)

