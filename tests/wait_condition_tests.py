import unittest
import hiro
import time
from tests.utils import make_temp_page, get_driver
from holmium.core import Page, Element, Elements, Locators, ElementMap
from holmium.core.pageobject import NonexistentElement
from holmium.core.conditions import *

class WaitConditionTests(unittest.TestCase):
    def setUp(self):
        self.driver = get_driver()
        self.uri = make_temp_page("<div id='simple_id'>default text</div>")

    def run_script(self, script, delay=0, sync=False):
        return (hiro.run_sync if sync else hiro.run_async)(1, lambda: time.sleep(delay) or self.driver.execute_script(script))

    def build_page_object(self, condition):
        class P(Page):
            id_el = Element(Locators.ID, "simple_id"
                , only_if=condition
                , timeout=5)
        return P

    @hiro.Timeline(scale=10)
    def test_only_if_matches_text(self):
        page = self.build_page_object(MATCHES_TEXT("changed"))(self.driver, self.uri)
        self.assertTrue(page.id_el == NonexistentElement())
        runner = self.run_script('document.getElementById("simple_id").innerHTML="changed";', 1)
        self.assertEqual(page.id_el.text, "changed")


    @hiro.Timeline(scale=10)
    def test_only_if_displayed(self):
        page = self.build_page_object(VISIBLE())(self.driver, self.uri)
        runner = self.run_script('document.getElementById("simple_id").style.display="none";', sync=True)
        runner = self.run_script('document.getElementById("simple_id").style.display="block";', 1)
        self.assertTrue(page.id_el != NonexistentElement())

    @hiro.Timeline(scale=10)
    def test_only_if_invisible(self):
        page = self.build_page_object(INVISIBLE())(self.driver, self.uri)
        self.assertTrue(page.id_el == NonexistentElement())
        runner = self.run_script('document.getElementById("simple_id").style.display="none";', 1)
        self.assertTrue(page.id_el != NonexistentElement())

    @hiro.Timeline(scale=10)
    def test_context_any_condition(self):
        class P(Page):
            cl_els = ElementMap(Locators.CLASS_NAME , "cls", timeout = 5)

        uri = make_temp_page("<div id='base'><div class='cls'>one</div></div>")
        page = P(self.driver, uri)
        script = """
        var el = document.createElement("div");
        el.setAttribute("class", "cls");
        el.innerHTML = '%s'
        document.getElementById("base").appendChild(el);
        """
        runner = self.run_script(script % 'two', 1)
        with ANY(MATCHES_TEXT('two')):
            self.assertTrue(page.cl_els['two'] != NonexistentElement())

    @hiro.Timeline(scale=10)
    def test_context_all_condition(self):
        class P(Page):
            cl_els = ElementMap(Locators.CLASS_NAME , "cls", timeout = 5)

        uri = make_temp_page("<div id='base'></div>")
        page = P(self.driver, uri)
        script = """
        var el = document.createElement("div");
        el.setAttribute("class", "cls");
        el.innerHTML = '%s'
        document.getElementById("base").appendChild(el);
        """
        runner = self.run_script(script % 'one', 1)
        with ALL(MATCHES_TEXT('one')):
            self.assertTrue(page.cl_els['one'] != NonexistentElement())
            self.assertEqual(len(page.cl_els), 1)
