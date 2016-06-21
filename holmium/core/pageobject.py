"""
implementation of page objects, element(s) and sections
"""

import inspect
import traceback
import weakref
import types
import threading
import tempfile
from random import random
import os
import contextlib
import collections
from functools import wraps
import appium

import selenium.webdriver.common.by
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, WebDriverException
from selenium.common.exceptions import TimeoutException, NoSuchFrameException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from six import add_metaclass
import time
from .enhancers import get_enhancers
from holmium.core.conditions import BaseCondition

if hasattr(collections, "OrderedDict"):
    OrderedDict = collections.OrderedDict  # pragma: no cover
else:
    from ordereddict import OrderedDict  # pragma: no cover

from .facets import Faceted, ElementFacet, CopyOnCreateFacetCollectionMeta
from .logger import log


def _get_with_stale_element_retry(get_fn):
    stale_ref_or_first_try = True
    MAX_TRIES = 10
    tries=0
    return_value = None

    while stale_ref_or_first_try and tries < MAX_TRIES:
        stale_ref_or_first_try = False
        try:
            return_value = get_fn()
        except StaleElementReferenceException as sere:
            tries+=1
            log.warn("Stale Element Reference Exception -- going to refetch element.")
            time.sleep(.2)
            stale_ref_or_first_try = True
    return return_value

def switch_to_iframe(iframe_or_frames, driver ):
    driver.switch_to.default_content()
    if type(iframe_or_frames) is list:
        for f in iframe_or_frames:
            driver.switch_to.frame(f)
    else:
        driver.switch_to.frame(iframe_or_frames)

# pylint: disable=unnecessary-lambda,too-few-public-methods,too-many-arguments
class Locators(appium.webdriver.common.mobileby.MobileBy):
    """
    proxy class to access locator types
    """
    pass


class ElementList(list):
    """
    proxy to a standard list which would be stored in
    a :class:`holmium.core.Page`.
    """

    def __init__(self, instance, *args, **kwargs):
        self.instance = weakref.ref(instance)
        list.__init__(self, *args, **kwargs)

    def __getitem__(self, index):
        return list.__getitem__(self, index).__get__(self.instance(),
                                                     self.instance().__class__)

    def __iter__(self):
        for idx in range(len(self)):
            yield self[idx]


class ElementDict(dict):
    """
    proxy to a standard dict which would be stored in
    a :class:`holmium.core.Page`.
    """

    def __init__(self, instance, *args, **kwargs):
        self.instance = weakref.ref(instance)
        dict.__init__(self, *args, **kwargs)

    def __getitem__(self, key):
        return dict.__getitem__(self, key).__get__(self.instance(),
                                                   self.instance().__class__)

    def values(self):
        return [self[key] for key in self]

    def items(self):
        return [(key, self[key]) for key in self.keys()]


class Registry(CopyOnCreateFacetCollectionMeta):
    """
    simple meta class to keep track of all page objects registered
    """
    pages = {}

    def __new__(mcs, *args, **kwargs):
        page = super(Registry, mcs).__new__(mcs, *args, **kwargs)
        Registry.pages[args[0]] = page
        return page


@add_metaclass(Registry)
class Page(Faceted):
    """
    Base class for all page objects to extend from.
    void Instance methods implemented by subclasses are provisioned
    with fluent wrappers to facilitate with writing code such as::

        class Google(Page):
            def query(self):
                ....

            def submit(self):
                ....

            def get_results(self):
                ....

        assert len(Google().query("page objects").submit().get_results()) > 0

    """
    local = threading.local()

    def __init__(self, driver, url=None, iframe=None):
        # pylint: disable=too-many-branches
        super(Page, self).__init__()
        self.driver = driver
        self.touched = False
        self.initialized = False
        if url:
            self.home = url
        else:
            try:
                if driver.current_url:
                    self.home = driver.current_url
                else:
                    self.home = None
            except WebDriverException: # not supported for mobile
                self.home = None

        self.iframe = iframe

        def update_element(element, name):
            """
            check if the element is a facet
            and register it.
            """
            if issubclass(element.__class__, ElementGetter):
                element.iframe = self.iframe
                if element.is_facet:
                    facet = ElementFacet(element,
                                         name,
                                         debug=element.is_debug_facet
                    )
                    facet.register(self)
                return True
            return False

        for element in inspect.getmembers(self.__class__):
            if issubclass(element[1].__class__, list):
                hit = True
                for item in element[1]:
                    hit &= update_element(item, element[0])
                if hit:
                    self.__setattr__(element[0], ElementList(self, element[1]))
            elif issubclass(element[1].__class__, dict):
                hit = True
                for item in element[1].values():
                    hit &= update_element(item, element[0])
                if hit:
                    self.__setattr__(element[0], ElementDict(self, element[1]))
            else:
                update_element(element[1], element[0])

        if url:
            self.driver.get(url)
        self.initialized = True

    @contextlib.contextmanager
    def scope(self):
        """
        context manager to manage the current webdriver
        in use.
        """
        Page.local.driver = object.__getattribute__(self, "driver")
        yield

    @classmethod
    def get_driver(cls):
        """
        returns the thread local driver
        """
        return cls.local.driver

    def go_home(self):
        """
        returns the page object to the url it was initialized with
        """
        self.driver.get(self.home)

    def __getattribute__(self, key):
        """
        to enable fluent access to page objects, instance methods that
        don't return a value, instead return the page object instance.
        """

        attr_getter = lambda key: object.__getattribute__(self, key)
        attr_setter = lambda key, value: object.__setattr__(self, key, value)

        with attr_getter("scope")():
            if not attr_getter("touched") and attr_getter("initialized"):
                attr_getter("evaluate")()
                attr_setter("touched", True)
            attr = attr_getter(key)
            # check if home url is set, else update.
            if not attr_getter("home"):
                log.debug(
                    "home url not set, attempting to update.")
                try:
                    attr_setter("home", attr_getter("driver").current_url)
                except WebDriverException:
                    self.home = NonexistentElement()

            if isinstance(attr, types.MethodType):
                @wraps(attr)
                def wrap(*args, **kwargs):
                    get_fn = lambda : attr(*args, **kwargs)
                    """
                    fluent wrapper
                    """
                    resp = NonexistentElement()
                    try:
                        resp = _get_with_stale_element_retry(get_fn)
                    except WebDriverException as wde:
                        traceback.print_exc()
                        file = save_screenshot(attr_getter("driver"))
                        log.error("Error trying to execute {0}".format(attr))
                        log.error("Screenshot saved to {0}".format(file))
                        raise wde
                    if issubclass(resp.__class__, WebElement):
                        return resp
                    elif resp is NonexistentElement():
                        resp = self
                    return resp
                return wrap
            return attr


class ElementGetter(object):
    """
    internal class to encapsulate the logic used by
    :class:`holmium.core.Element`
    & :class:`holmium.core.Elements`
    """

    # pylint: disable=too-many-instance-attributes
    def __init__(self, locator_type,
                 query_string,
                 base_element=None,
                 timeout=0,
                 value=lambda el: el,
                 only_if=lambda el: el is not None,
                 facet=False):
        """
        :param holmium.core.Locators locator_type: selenium locator to use when
         locating the element
        :param str query_string: the value to pass to the locator
        :param holmium.core.Element base_element: a reference to another element
         under which to locate this element.
        :param int timeout: time to implicitely wait for the element
        :param lambda value: transform function for the value of the element.
         The located :class:`selenium.webdriver.remote.webelement.WebElement`
         instance is passed as the only argument to the function.
        :param function only_if: extra validation function that is called
         repeatedly until :attr:`timeout` has elapsed. If not provided the
         default function used checks that the element is present.
         The located :class:`selenium.webdriver.remote.webelement.WebElement`
         instance is passed as the only argument to the function.
        :param bool facet: flag to  treat this element as a facet.
        """
        self.query_string = query_string
        self.locator_type = locator_type
        self.timeout = timeout
        self.driver = None
        self.iframe = None
        self.base_element = base_element
        self.value_mapper = value
        self.root_fn = lambda: Page.get_driver()
        self.only_if = only_if
        log.debug("locator:%s, query_string:%s, timeout:%d" %
                  (locator_type, query_string, timeout))
        self.is_facet = facet
        self.is_debug_facet = False

    @property
    def root(self):
        "returns the root webelement"
        return self.root_fn()

    @root.setter
    def root(self, root_fn):
        "sets the root element extraction function"
        self.root_fn = root_fn

    def _get_element(self, method=None):
        """
        extracts the webelement(s)
        :param function method: the method used to query the webdriver
        """
        if self.base_element:
            if isinstance(self.base_element, types.LambdaType):
                _ = self.base_element()
                _meth = getattr(_, method.__name__)
            elif isinstance(self.base_element, Element):
                _meth = getattr(self.base_element.__get__(self, self.__class__),
                                method.__name__)
            elif isinstance(self.base_element, WebElement):
                _meth = getattr(self.base_element, "find_element")
            else:
                raise TypeError("invalid base_element type (%s) used" % (
                    type(self.base_element)))
        else:
            _meth = method
        log.debug(
            "looking up locator:%s, query_string:%s, timeout:%d" %
            (self.locator_type, self.query_string, self.timeout))

        if self.iframe is not None:
            switch_to_iframe(self.iframe, Page.local.driver)

        if self.timeout:
            try:
                def callback(_):
                    """
                    timeout & only_if explicit wait.
                    """
                    return _meth(self.locator_type, self.query_string) and \
                           (BaseCondition.get_current() or self.only_if)(
                               _meth(self.locator_type, self.query_string)
                           )

                WebDriverWait(self.root, self.timeout,
                              ignored_exceptions=[StaleElementReferenceException,]
                ).until(callback)
            except TimeoutException:
                log.debug(
                    "unable to find element %s after waiting for %d seconds" % (
                        self.query_string, self.timeout)
                )
                raise
        return _meth(self.locator_type, self.query_string)

    @classmethod
    def enhance(cls, element):
        """
        incase a higher level abstraction for a WebElement is available
        we will use that in Pages. (e.g. a select element is converted into
        :class:`selenium.webdriver.support.ui.Select`)
        """
        for enhancer in get_enhancers():
            if enhancer.matches(element):
                return enhancer(element)
        return element


def save_screenshot(driver):
    random_str = str(random()).replace('.', '')
    #FIXME: change to configurable destination dir!
    snapfile = os.path.join("logs", "screenshot_{0}.png".format(random_str))
    driver.save_screenshot(snapfile)
    return snapfile


class NonexistentElement(object):
    """
    A null-object representing an element that was not found.
    This allows us to know what the selector was that was ineffective
    rather than just returning None.
    """
    def __init__(self, exception_class_name=None, locator_type=None, query_string=None):
        """To properly instantiate a NonexistentElement, pass in the exception_class_name,
        locator_type, and query_string.  Although no parameters can be passed for an easy comparison
        against Nonexistentelement()
        """

        self.name = "NonexistentElement"
        ## Self.id is necessary to allow comparisons againt webElement objects, otherwise
        ## our custom Exception gets raised when a webElement tests for equivalence
        self.id = None
        self.webdriver_exception = exception_class_name
        self.locator_type = locator_type
        self.query_string = query_string


    def __eq__(self, other):
        if type(self) is type(other):
            return True
        else:
            return False

    def __ne__(self, other):
        if type(self) is not type(other):
            return True
        else:
            return False


    def __str__(self):
        return "{}(webdriver_exception={}, locator_type='{}' query_string='{}')".format(type(self).__name__,
                                                                                        self.webdriver_exception,
                                                                                        self.locator_type, self.query_string)

    def __repr__(self):
        return "holmium.core.pageobject."+str(self)

    def __getattr__(self, key):
        raise Exception("{}".format(self))

class Element(ElementGetter):
    """
    Utility to get a :class:`selenium.webdriver.remote.webelement.WebElement`
    by querying via one of :class:`holmium.core.Locators`

    :param holmium.core.Locators locator_type: selenium locator to use when
     locating the element
    :param str query_string: the value to pass to the locator
    :param holmium.core.Element base_element: a reference to another element
     under which to locate this element.
    :param int timeout: time to implicitely wait for the element
    :param lambda value: transform function for the value of the element.
     The located :class:`selenium.webdriver.remote.webelement.WebElement`
     instance is passed as the only argument to the function.
    :param function only_if: extra validation function that is called repeatedly
     until :attr:`timeout` elapases. If not provided the default function used
     checks that the element is present. The located
     :class:`selenium.webdriver.remote.webelement.WebElement`
     instance is passed as the only argument to the function.
    :param bool facet: flag to  treat this element as a facet.
    """

    def __get__(self, instance, owner):
        try:
            if not instance:
                return_value = self
            else:
                def get_fn():
                    return self.value_mapper(
                        self.enhance(self._get_element(self.root.find_element))
                        ) if self.root else NonexistentElement(self.locator_type, self.query_string)
                return_value = _get_with_stale_element_retry(get_fn)
        except (NoSuchElementException, TimeoutException) as e:
            return_value = NonexistentElement(type(e).__name__, self.locator_type, self.query_string)
        except NoSuchFrameException as e:
            snapfile = save_screenshot(Page.get_driver())
            raise Exception("NoSuchFrameException ({0}):  Snapshot saved as {1}".format(str(e), snapfile))
        return return_value


class Elements(ElementGetter):
    """
    Utility to get a collection of
    :class:`selenium.webdriver.remote.webelement.WebElement` objects by
    querying via one of :class:`holmium.core.Locators`

    :param holmium.core.Locators locator_type: selenium locator to use when
     locating the element
    :param str query_string: the value to pass to the locator
    :param holmium.core.Element base_element: a reference to another element
     under which to locate this element.
    :param int timeout: time to implicitely wait for the element
    :param lambda value: transform function for each element in the collection.
     The located :class:`selenium.webdriver.remote.webelement.WebElement`
     instance is passed as the only argument to the function.
    :param function only_if: extra validation function that is called repeatedly
     until :attr:`timeout` elapses. If not provided the default function used
     checks that all the elements are present. The list of located
     :class:`selenium.webdriver.remote.webelement.WebElement`
     instances is passed as the only argument to the function.
    :param bool facet: flag to  treat this element as a facet.
    """
    # pylint: disable=incomplete-protocol,line-too-long
    def __init__(self, locator_type,
                 query_string=None,
                 base_element=None,
                 timeout=0,
                 value=lambda el: el,
                 only_if=lambda el: el is not None,
                 facet=False):
        super(Elements, self).__init__(locator_type, query_string,
                                       base_element=base_element,
                                       timeout=timeout,
                                       facet=facet, value=value,
                                       only_if=only_if)

    def __getitem__(self, idx):
        return lambda: self.__get__(self, self.__class__)[idx]

    def __get__(self, instance, owner):
        if not instance:
            return self
        try:
            return [self.value_mapper(self.enhance(el)) for el in
                    self._get_element(self.root.find_elements)] if self.root else []
        except (NoSuchElementException, TimeoutException):
            return []


class ElementMap(Elements):
    """
    Used to create dynamic dictionaries based on an element locator specified by
    one of :class:`holmium.core.Locators`.

    The wrapped dictionary is an :class:`collections.OrderedDict` instance.

    :param holmium.core.Locators locator_type: selenium locator to use when
     locating the element
    :param str query_string: the value to pass to the locator
    :param holmium.core.Element base_element: a reference to another element
     under which to locate this element.
    :param int timeout: time to implicitely wait for the element
    :param bool facet: flag to  treat this element as a facet.
    :param lambda key: transform function for mapping a key to a WebElement in
     the collection. The located
     :class:`selenium.webdriver.remote.webelement.WebElement` instance is passed
     as the only argument to the function.
    :param lambda value: transform function for the value when accessed via the
     key. The located :class:`selenium.webdriver.remote.webelement.WebElement`
     instance is passed as the only argument to the function.
    :param function only_if: extra validation function that is called repeatedly
     until :attr:`timeout`. If not provided the default function used checks
     that all the elements are present. The list of located
     :class:`selenium.webdriver.remote.webelement.WebElement` instances is
     passed as the only argument to the function.
    """
    # pylint: disable=incomplete-protocol,line-too-long
    def __init__(self, locator_type,
                 query_string=None,
                 base_element=None,
                 timeout=0,
                 key=lambda el: el.text,
                 value=lambda el: el,
                 only_if=lambda el: el is not None,
                 facet=False):
        super(ElementMap, self).__init__(locator_type, query_string,
                                         base_element,
                                         timeout, facet, only_if=only_if)
        self.key_mapper = key
        self.value_mapper = value

    def __get__(self, instance, owner):
        if not instance:
            return self
        try:
            return OrderedDict(
                (self.key_mapper(el), self.value_mapper(self.enhance(el))) for el in
                self._get_element(self.root.find_elements)) if self.root else {}
        except (NoSuchElementException, TimeoutException):
            return {}

    def __getitem__(self, key):
        return lambda: self.__get__(self, self.__class__)[key]


class Section(Faceted):
    """
    Base class to encapsulate reusable page sections::

        class MySection(Section):
            things = Elements( .... )

        class MyPage(Page):
            section_1 =  MySection(Locators.CLASS_NAME, "section")
            section_2 =  MySection(Locators.ID, "unique_section")

    """

    def __init__(self, locator_type, query_string, iframe=None, timeout=0):

        super(Section, self).__init__()
        self.touched = False
        self.locator_type = locator_type
        self.query_string = query_string
        self.iframe = iframe
        self.timeout = timeout
        self.__root_val = None
        self.element_members = {}
        for element in inspect.getmembers(self.__class__):
            if issubclass(element[1].__class__, ElementGetter):
                self.element_members[element[0]] = element[1]
                if element[1].is_facet:
                    facet = ElementFacet(element[1],
                                         element[0],
                                         debug=element[1].is_debug_facet
                    )
                    facet.register(self)

    def __get__(self, instance, owner):
        for element in self.element_members.values():
            element.root = lambda: self.root
        return self

    def __getattribute__(self, item):
        attr_getter = lambda key: super(Section, self).__getattribute__(key)
        attr_setter = lambda key, value: super(Section, self).__setattr__(key,
                                                                          value)
        members = attr_getter("element_members")
        touched = attr_getter("touched")
        if not touched and item in members:
            attr_getter("evaluate")()
            attr_setter("touched", True)
        return attr_getter(item)


    @property
    def root(self):
        """
        returns the element the section is rooted at
        """
        if self.iframe:
            try:
                switch_to_iframe(self.iframe, Page.get_driver())
            except NoSuchFrameException:
                log.error(
                    "unable to switch to iframe %s" % self.iframe)
        try:
            if not self.__root_val:
                WebDriverWait(Page.get_driver(), self.timeout).until(
                    lambda _: Page.get_driver().find_element(self.locator_type,
                                                             self.query_string)
                )
            return self.__root_val or Page.get_driver().find_element(
                self.locator_type, self.query_string
            )
        except (NoSuchElementException, TimeoutException):
            return NonexistentElement(
                self.locator_type, self.query_string
            )

    @root.setter
    def root(self, val):
        """
        sets the root of the section
        """
        self.__root_val = val


class Sections(Section, collections.Sequence):
    """
    Base class for an Iterable view of a collection of
    :class:`holmium.core.Section` objects.
    """

    def __init__(self, locator_type, query_string, iframe=None, timeout=0):
        super(Sections, self).__init__(locator_type, query_string, iframe, timeout)

    def __getelements__(self):
        if self.timeout:
            try:
                WebDriverWait(Page.get_driver(), self.timeout).until(
                    lambda _: Page.get_driver().find_elements(self.locator_type,
                                                              self.query_string)
                )
            except TimeoutException:
                log.debug(
                    "unable to find element %s after waiting for %d seconds" % (
                        self.query_string, self.timeout)
                )
        return Page.get_driver().find_elements(self.locator_type,
                                               self.query_string)

    def __iter__(self):
        for element in self.__getelements__():
            self.root = element
            yield self

    def __len__(self):
        return len(self.__getelements__())

    def __getitem__(self, idx):
        if idx < 0 or idx >= len(self):
            raise IndexError("Sections index (%d) out of range" % idx)
        for i, _ in enumerate(self):
            if i == idx:
                break
        return self

