from functools import wraps
import inspect
import re
import time

from selenium.webdriver.common.keys import Keys
from nose.tools import assert_equals, assert_true

from fresher import Transform, When, scc, Then, NamedTransform, ftc
from .pageobject import Registry, Section, Sections


def paramfromconfig(fn):
    @wraps(fn)
    def __inner(*args):
        def get_and_set(v):
            ftc.config["_holmium_cucumber_temp_var"] = v
            return ftc.config["_holmium_cucumber_temp_var"]
        _a = []
        _k = {}
        for arg in args:
            _a.append(get_and_set(arg))
        return fn(*_a)
    return __inner


def word_to_index(word):
    """
    convert an index in english (1st, first, 20th, twenty first etc..)
    into a number. I'm sure someone out there has a much cleaner implementation.
    """

    ones = {
        'twenty': 2,
        'thirty': 3,
        'fourty': 4,
        'fifty': 5,
        'sixty': 6,
        'seventy': 7,
        'eighty': 8,
        'ninety': 9}
    ones_rev = dict((v, k) for k, v in ones.items())

    anomolies = {1: "first", 2: "second", 3: "third", 4: "fourth", 5: "fifth",
                 6: "sixth", 7: "seventh", 8: "eighth", 9: "ninth", 10: "tenth",
                 11: "eleventh", 12: "twelvth", 13: "thirteenth",
                 14: "fourteenth", 15: "fifteenth",
                 16: "sixteenth", 17: "seventeenth", 18: "eighteenth",
                 19: "nineteenth"}
    anomolies_rev = dict((v, k) for k, v in anomolies.items())
    rest = {}
    for i in range(20, 99):
        if i % 10 == 0:
            rest[i] = ones_rev[i // 10]
        else:
            _f = ones_rev[i // 10]
            _s = anomolies[i % 10]
            rest["%s %s" % (_f, _s)] = i
    easy = re.compile("(\d+)(st|rd|th)")

    if easy.match(word):
        return int(easy.findall(word)[0][0]) - 1
    elif word in anomolies_rev:
        return anomolies_rev[word] - 1
    elif word in rest:
        return rest[word] - 1
    else:
        return word

def init_steps():
    """
    required to inject holmium steps into the callers' step module.
    """
    frm = inspect.stack()[1]
    mod = inspect.getmodule(frm[0])
    from fresher.stepregistry import StepImpl, TransformImpl, NamedTransformImpl
    for k,v in globals().items():
        if any(((v, t) for t in (StepImpl, TransformImpl, NamedTransformImpl))):
            setattr(mod, k, v )


@Transform("^the page (\w+)$")
def transform_page(name):
    if name not in Registry.pages:
        raise AttributeError(
            "page object %s not found. did you import it?" % name)
    return Registry.pages[name]


@NamedTransform("{element}", "(element (\w+))", "element (\w+)")
def transform_element(name):
    if not hasattr(scc.page, name):
        raise AttributeError(
            "page object %s does not contain an element named %s" % (
                scc.page.__class__.__name__, name
            )
        )
    element = getattr(scc.page, name)
    return element


@NamedTransform("{item_in_elements}", "((.*?)\s+item\s+in\s+(\w+))",
                "(.*?)\s+item\s+in\s+(\w+)")
def transform_sub_element(key, name):
    if not hasattr(scc.page, name):
        raise AttributeError(
            "page object %s does not contain an element named %s" % (
                scc.page.__class__.__name__, name
            )
        )
    sub_expr = re.compile("(\w+)(?:\s* item)? (?:of|for) the (.*)$")
    element = getattr(scc.page, name)
    sub = None
    if sub_expr.match(key):
        sub, key = sub_expr.findall(key)[0]
        sub = word_to_index(sub)
    key = word_to_index(key)
    if isinstance(element, dict):
        sub_element = element[key]
    elif isinstance(element, Section) and not isinstance(element, Sections):
        sub_element = getattr(element, key)
    else:
        sub_element = element[int(key)]
    if sub != None:
        if isinstance(sub_element, (list, dict)):
            return sub_element[sub]
        return getattr(sub_element, sub)
    return sub_element


@When("^I?\s*access (the page .*?) at url (.*?)$")
@paramfromconfig
def access_page(page, url):
    scc.page = page(ftc.driver, url)

@When("^I?\s*access the url (.*?)$")
@paramfromconfig
def access_url(url):
    ftc.driver.get(url)

@When("^I?\s*perform (\w+) with (?:arguments)?\s*(.*?)$")
@paramfromconfig
def page_action_with_args(action, args):
    if not hasattr(scc.page, action):
        raise AttributeError("page object %s does not contain a method %s" % (
            scc.page.__class__.__name__, action)
        )
    arg_list = [k for k in args.split(",") if k.strip()]
    getattr(scc.page, action)(*arg_list)

@When("^I?\s*perform (\w+)\s*$")
@paramfromconfig
def page_action(action):
    if not hasattr(scc.page, action):
        raise AttributeError("page object %s does not contain a method %s" % (
            scc.page.__class__.__name__, action)
        )
    getattr(scc.page, action)()

@Then("(?:the)?\s*{element} should be visible\s*$")
@paramfromconfig
def element_visible(element, *args):
    assert_true(element is not None)


@Then("(?:the)?\s*{item_in_elements} should be visible\s*$")
@paramfromconfig
def item_in_element_visible(element, *args):
    assert_true(element is not None)


@Then("(?:the)?\s*{element} should have (\d+) items")
@paramfromconfig
def element_count(element, name, count):
    assert_equals(int(count), len(element))


@When("^I?\s*type (.*?) in {element}\s*$")
@paramfromconfig
def element_type(text, element, *args):
    element.send_keys(text)

@When("^I?\s*type (.*?) in {item_in_elements}\s*$")
@paramfromconfig
def item_in_elements_type(text, element, *args):
    element.send_keys(text)

@When("^I?\s*(?:press|pressed)\s*(?:enter|Enter) in (?:.*?){element}\s*$")
@paramfromconfig
def press_enter(element, *args):
    element.send_keys(Keys.ENTER)


@When("^I?\s*(?:press|pressed)\s*(?:enter|Enter) in {item_in_elements}\s*$")
@paramfromconfig
def press_enter_in_item_in_element(element, *args):
    element.send_keys(Keys.ENTER)


@When("^I?\s*click the {element}\s*$")
@paramfromconfig
def element_click(element, *args):
    element.click()


@When("^I?\s*click the {item_in_elements}\s*$")
@paramfromconfig
def item_in_element_click(element, *args):
    element.click()


@Then("^I?\s*should see the title (.*?)\s*$")
@paramfromconfig
def assert_title(title):
    assert_equals(ftc.driver.title, title)

@Then("(?:the)?\s*{element} should have (?:the)?\s*text (.*?)\s*$")
@paramfromconfig
def text_in_element(*args):
    element, _, text = args
    assert_equals(element.text, text)

@Then("(?:the)?\s*{item_in_elements} should have (?:the)?\s*text (.*?)\s*$")
@paramfromconfig
def text_in_elements_item(*args):
    element, text = args[0], args[-1]
    assert_equals(element.text, text)


@When("^I?\s*wait for (\d+) (second|seconds)")
@paramfromconfig
def wait(seconds, *args):
    time.sleep(int(seconds))


@When("^I?\s*go (back|forward)")
@paramfromconfig
def back_or_forward(direction):
    if direction.strip() == "back":
        ftc.driver.back()
    else:
        ftc.driver.forward()

