"""
tests for facets
"""
import unittest
from flask_testing import LiveServerTestCase
import mock

from holmium.core import Page, Element, Locators, Elements, Section, ElementMap
from holmium.core.facets import FacetError, defer, title, cookie, strict
from holmium.core.pageobject import NonexistentElement

from . import webapp
from tests.utils import get_driver


class LiveTest(LiveServerTestCase):
    def create_app(self):
        return webapp.create_app()
    def setUp(self):
        super(LiveTest, self).setUp()
        webapp.db.create_db()

@strict()
class NavSection(Section):
    links = Elements(Locators.CSS_SELECTOR, "ul>li")

@strict()
class BadNavSectionStrict(Section):
    links = Elements(Locators.CSS_SELECTOR, "ul>li")
    junk = Element(Locators.CLASS_NAME, "junk")

@strict(debug=True)
class BadNavSectionStrictDebug(Section):
    links = Elements(Locators.CSS_SELECTOR, "ul>li")
    junk = Element(Locators.CLASS_NAME, "junk")

class BadNavSection(Section):
    links = Elements(Locators.CSS_SELECTOR, "ul>bi", facet=True)

class JumboTron(Section):
    callout = Element(Locators.TAG_NAME, "h1")
    link = Element(Locators.CLASS_NAME, "btn")

class BasePage(Page):
    nav = NavSection(Locators.CLASS_NAME, "nav")
    jumbo = JumboTron(Locators.CLASS_NAME, "jumbotron")


@title(title="login")
class LoginPage(BasePage):
    email = Element(Locators.NAME, "email", facet=True)
    password = Element(Locators.NAME, "password", facet=True)
    submit = Element(Locators.ID, "login-submit", facet=True)

    def login(self, email, password):
        self.email.send_keys(email)
        self.password.send_keys(password)
        self.submit.click()


@title(title="main page")
@cookie(name="uid")
@defer(page=LoginPage,
                    action=LoginPage.login,
                    action_arguments={"email": "john@doe.com",
                                      "password": "sekret"},
                    required=False)
class MainPage(BasePage):
    references = ElementMap ( Locators.CLASS_NAME, "reference-link")
    reference_content = Element(Locators.ID, "reference-content")
    selenium = Element(Locators.LINK_TEXT, "Selenium", timeout=5)


def do_login(page, email, password):
   page.login(email, password)

@title(title="main page")
@cookie(name="uid")
@defer(page=LoginPage,
                    action=do_login,
                    action_arguments={"email": "john@doe.com",
                                      "password": "sekret"},
                    required=True)
class MainPageWithCallable(BasePage):
    references = ElementMap ( Locators.CLASS_NAME, "reference-link")
    reference_content = Element(Locators.ID, "reference-content")
    selenium = Element(Locators.LINK_TEXT, "Selenium", timeout=5)

class MainPageBadElement(BasePage):
    bad_element = Element(Locators.NAME, "bad_element", facet=True)

class MainPageBadSectionElement(BasePage):
    nav = BadNavSection(Locators.CLASS_NAME, "nav")

class MainPageMixedSection(BasePage):
    bad_nav = BadNavSection(Locators.CLASS_NAME, "nav")


class FacetsTests(LiveTest):
    def setUp(self):
        super(FacetsTests, self).setUp()
        self.driver = get_driver()
        self.base_url = self.get_server_url()

    def test_main_page_callout(self):
        main = MainPage(self.driver, self.base_url)
        self.assertEqual(main.jumbo.callout.text, "Here's a few ways it can be good")

    def test_main_page_with_callable_callout(self):
        main = MainPageWithCallable(self.driver, self.base_url)
        self.assertEqual(main.jumbo.callout.text, "Here's a few ways it can be good")

    def test_main_click_selenium(self):
        main = MainPage(self.driver, self.base_url)
        main.selenium.click()
        self.assertTrue("Selenium automates browsers." in main.reference_content.text)

    def test_main_page_login_first(self):
        login = LoginPage(self.driver, self.base_url + "/login")
        login.login("john@doe.com", "sekret")
        main = MainPage(self.driver, self.base_url)
        self.assertEqual(main.jumbo.callout.text, "Here's a few ways it can be good")

    def test_main_page_bad_trait_element(self):
        main = MainPageBadElement(self.driver, self.base_url)
        self.assertRaises(FacetError, lambda:main.jumbo)

    def test_main_page_bad_section_element(self):
        main = MainPageBadSectionElement(self.driver, self.base_url)
        self.assertRaises(FacetError, lambda: main.nav.links)

    def test_main_page_bad_section_strict(self):
        class _P(MainPage):
            bad_nav = BadNavSectionStrict(Locators.CLASS_NAME, "nav")
        main = _P(self.driver, self.base_url)
        self.assertRaises(FacetError, lambda: main.bad_nav.links)
        self.assertTrue( main.nav.links is not None)

    def test_main_page_bad_section_strict_debug(self):
        class _P(MainPage):
            bad_nav = BadNavSectionStrictDebug(Locators.CLASS_NAME, "nav")
        main = _P(self.driver, self.base_url)
        with mock.patch("holmium.core.facets.log") as log:
            self.assertTrue( main.bad_nav.links is not None)
            self.assertTrue( main.bad_nav.junk is NonexistentElement())
            self.assertTrue( main.nav.links is not None)
            self.assertTrue(log.warn.call_count == 1)
            self.assertTrue("failed to exhibit facet junk" in str(log.warn.call_args))

    def test_main_page_good_and_bad_section_element(self):
        main = MainPageMixedSection(self.driver, self.base_url)
        self.assertRaises(FacetError, lambda: main.bad_nav.links)
        self.assertTrue( main.nav.links is not None)

    def tearDown(self):
        super(FacetsTests, self).tearDown()

class GoodFacetsTest(unittest.TestCase):
    def test_all(self):

        class Other(Page):
            def do(self):
                return

        @title(title="title")
        @cookie(name="cookie", value="yum")
        @cookie(name="cookie", value=lambda c:c=="yum")
        @defer(page=Other, action=Other.do)
        class P(Page):
            el = Element(Locators.CLASS_NAME, "null")

        driver = mock.Mock()
        driver.find_element.return_value.text = "null"
        driver.get_cookie.return_value = "yum"
        driver.title = "title"
        p = P(driver)
        self.assertEqual(p.el.text, "null")

class BadFacetTests(unittest.TestCase):
    def test_missing_title(self):
        @title(title="foo")
        class P(Page):
            el = Element(Locators.CLASS_NAME, "null")

        driver = mock.Mock()
        p = P(driver)
        self.assertRaises(FacetError, lambda: p.el)

    def test_failed_callable(self):
        @cookie(name="foo", value=lambda c:c==1)
        class P(Page):
            el = Element(Locators.CLASS_NAME, "null")

        driver = mock.Mock()
        driver.get_cookie.return_value = 2
        p = P(driver)
        self.assertRaises(FacetError, lambda: p.el)

class BadReactionTests(unittest.TestCase):
    def test_failed_reaction_required(self):

        class Other(Page):
            def do(self):
                raise Exception("can't")
        @defer(page=Other, action=Other.do)
        class P(Page):
            el = Element(Locators.CLASS_NAME, "null")

        driver = mock.Mock()
        p = P(driver)
        self.assertRaises(FacetError, lambda: p.el)
    def test_passed_reaction_notrequired(self):

        class Other(Page):
            def do(self):
                raise Exception("can't")
        @defer(page=Other, action=Other.do, required=False)
        class P(Page):
            el = Element(Locators.CLASS_NAME, "null")

        driver = mock.Mock()
        driver.find_element.return_value.text = "null"
        p = P(driver)
        self.assertEqual(p.el.text, "null")


def test_missing_arguments():
    for args in [{}, {"page":1}, {"page":1, "action":1, "foobar":1}]:
        yield check_arguments, args

def check_arguments(args):
    def create(**kw):
        @defer(**kw)
        class P(Page):
            pass
    try:
        create(**args)
        raise Exception("exception not raised")
    except AttributeError as e:
        pass

