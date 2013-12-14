"""
implementation of cucumber steps for use with fresher/n
"""
from functools import wraps
import inspect
import re
import time

from selenium.webdriver.common.keys import Keys
# pylint: disable=E0611
from nose.tools import assert_equals, assert_true

from fresher import Transform, When, scc, Then, NamedTransform, ftc
from .pageobject import Registry, Section, Sections


def paramfromconfig(function):
    """
    decorator for internal use. maps arguments from ftc.config
    """
    @wraps(function)
    def __inner(*args):
        """
        wrapper
        """
        # pylint: disable=star-args
        def get_and_set(value):
            """
            lol.
            """
            ftc.config["_holmium_cucumber_temp_var"] = value
            return ftc.config["_holmium_cucumber_temp_var"]
        _args = []
        for arg in args:
            _args.append(get_and_set(arg))
        return function(*_args)
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
            first = ones_rev[i // 10]
            second = anomolies[i % 10]
            rest["%s %s" % (first, second)] = i
    easy = re.compile(r"(\d+)(st|rd|th)")

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
    fresher_types = (StepImpl, TransformImpl, NamedTransformImpl)
    for key, value in globals().items():
        if any(((value, _type) for _type in fresher_types)):
            setattr(mod, key, value)


@Transform(r"^the page (\w+)$")
def transform_page(name):
    """
    looks up the page in the Registry
    """
    if name not in Registry.pages:
        raise AttributeError(
            "page object %s not found. did you import it?" % name)
    return Registry.pages[name]


@NamedTransform(r"{element}", r"(element (\w+))", r"element (\w+)")
def transform_element(name):
    """
    looks up the element in the page currently registered on the context
    """
    if not hasattr(scc.page, name):
        raise AttributeError(
            "page object %s does not contain an element named %s" % (
                scc.page.__class__.__name__, name
            )
        )
    element = getattr(scc.page, name)
    return element


@NamedTransform(r"{item_in_elements}", r"((.*?)\s+item\s+in\s+(\w+))",
                r"(.*?)\s+item\s+in\s+(\w+)")
def transform_sub_element(key, name):
    """
    looks up a subelement (either index, key or section memeber)
    """
    if not hasattr(scc.page, name):
        raise AttributeError(
            "page object %s does not contain an element named %s" % (
                scc.page.__class__.__name__, name
            )
        )
    sub_expr = re.compile(r"(\w+)(?:\s* item)? (?:of|for) the (.*)$")
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


@When(r"^I?\s*access (the page .*?) at url (.*?)$")
@paramfromconfig
def access_page(page, url):
    """
    loads the pageobject with the given url
    into the scenario context
    """
    scc.page = page(ftc.driver, url)

@When(r"^I?\s*access the url (.*?)$")
@paramfromconfig
def access_url(url):
    """
    switch the driver to the provided url
    """
    ftc.driver.get(url)

@When(r"^I?\s*perform (\w+) with (?:arguments)?\s*(.*?)$")
@paramfromconfig
def page_action_with_args(action, args):
    """
    execute a method of the page with arguments
    """
    if not hasattr(scc.page, action):
        raise AttributeError("page object %s does not contain a method %s" % (
            scc.page.__class__.__name__, action)
        )
    arg_list = [k for k in args.split(",") if k.strip()]
    # pylint: disable=star-args
    getattr(scc.page, action)(*arg_list)

@When(r"^I?\s*perform (\w+)\s*$")
@paramfromconfig
def page_action(action):
    """
    execute a method of the page
    """
    if not hasattr(scc.page, action):
        raise AttributeError("page object %s does not contain a method %s" % (
            scc.page.__class__.__name__, action)
        )
    getattr(scc.page, action)()

@Then(r"(?:the)?\s*{element} should be visible\s*$")
@paramfromconfig
def element_visible(element, *_):
    """
    assert element is visible
    """
    assert_true(element is not None)


@Then(r"(?:the)?\s*{item_in_elements} should be visible\s*$")
@paramfromconfig
def item_in_element_visible(element, *_):
    """
    assert sub element is visible
    """
    assert_true(element is not None)


@Then(r"(?:the)?\s*{element} should have (\d+) items")
@paramfromconfig
def element_count(element, _, count):
    """
    assert number of subelements
    """
    assert_equals(int(count), len(element))


@When(r"^I?\s*type (.*?) in {element}\s*$")
@paramfromconfig
def element_type(text, element, *_):
    """
    type inside the element
    """
    element.send_keys(text)

@When(r"^I?\s*type (.*?) in {item_in_elements}\s*$")
@paramfromconfig
def item_in_elements_type(text, element, *_):
    """
    type inside the sub element
    """
    element.send_keys(text)

@When(r"^I?\s*(?:press|pressed)\s*(?:enter|Enter) in (?:.*?){element}\s*$")
@paramfromconfig
def press_enter(element, *_):
    """
    press the enter key in the element
    """
    element.send_keys(Keys.ENTER)


@When(r"^I?\s*(?:press|pressed)\s*(?:enter|Enter) in {item_in_elements}\s*$")
@paramfromconfig
def press_enter_in_item_in_element(element, *_):
    """
    press the enter key in the sub element
    """
    element.send_keys(Keys.ENTER)


@When(r"^I?\s*click the {element}\s*$")
@paramfromconfig
def element_click(element, *_):
    """
    click the element
    """
    element.click()


@When(r"^I?\s*click the {item_in_elements}\s*$")
@paramfromconfig
def item_in_element_click(element, *_):
    """
    click the sub element
    """
    element.click()


@Then(r"^I?\s*should see the title (.*?)\s*$")
@paramfromconfig
def assert_title(title):
    """
    assert the title of the page
    """
    assert_equals(ftc.driver.title, title)

@Then(r"(?:the)?\s*{element} should have (?:the)?\s*text (.*?)\s*$")
@paramfromconfig
def text_in_element(*args):
    """
    assert the text of the element
    """
    # pylint: disable=unbalanced-tuple-unpacking
    element, _, text = args
    assert_equals(element.text, text)

@Then(r"(?:the)?\s*{item_in_elements} should have (?:the)?\s*text (.*?)\s*$")
@paramfromconfig
def text_in_elements_item(*args):
    """
    assert the text of the sub element
    """
    element, text = args[0], args[-1]
    assert_equals(element.text, text)


@When(r"^I?\s*wait for (\d+) (second|seconds)")
@paramfromconfig
def wait(seconds, *_):
    """
    sleep if you must...
    """
    time.sleep(int(seconds))


@When(r"^I?\s*go (back|forward)")
@paramfromconfig
def back_or_forward(direction):
    """
    move the browser back/forward
    """
    if direction.strip() == "back":
        ftc.driver.back()
    else:
        ftc.driver.forward()

