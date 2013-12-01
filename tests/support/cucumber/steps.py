from holmium.core import Page, Element, Locators, Elements, ElementMap, Section, Sections
from holmium.core.cucumber import init_steps
init_steps()

class TestSection(Section):
    el = Element(Locators.NAME, "el")
    els = Elements(Locators.NAME, "els")
    elmap = ElementMap(Locators.NAME, "elmap")

class TestSections(Sections):
    el = Element(Locators.NAME, "el")


class TestPage(Page):
    el = Element(Locators.NAME, "el")
    els = Elements(Locators.NAME, "els")
    elmap = ElementMap(Locators.NAME, "elmap")
    sections = TestSections(Locators.NAME, "sections")
    section  = TestSection(Locators.NAME, "section")
    def do_stuff(self, a, b):
        return a+b

    def do_stuff_no_args(self):
        return True

    def do_stuff_var_args(self, *args, **kwargs):
        return args, kwargs
