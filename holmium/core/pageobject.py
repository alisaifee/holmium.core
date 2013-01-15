from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.remote.webelement import WebElement
import selenium.webdriver.common.by
import holmium
import inspect
import weakref
import types
try:
    from ordereddict import OrderedDict
except ImportError:
    from collections import OrderedDict

from functools import wraps
class Locators(selenium.webdriver.common.by.By):
    """
    proxy class to access locator types
    """
    pass


def enhanced (web_element):
    """
    incase a higher level abstraction for a WebElement is available
    we will use that in PageObjects. (e.g. a select element is converted into
    :class:`selenium.webdriver.support.ui.Select`)
    """
    abstraction_mapping = {'select': Select}
    if web_element.tag_name in abstraction_mapping.keys():
        return abstraction_mapping[web_element.tag_name](web_element)
    return web_element


class PageElementList(list):
    """
    proxy to a standard list which would be stored in
    a :class:`holmium.core.PageObject`.
    """

    def __init__(self, instance, *args, **kwargs):
        self.instance = weakref.ref(instance)
        list.__init__(self, *args, **kwargs)

    def __getitem__(self, index):
        return list.__getitem__(self, index).__get__(self.instance(),
                                                     self.instance().__class__)

class PageElementDict(dict):
    """
    proxy to a standard dict which would be stored in
    a :class:`holmium.core.PageObject`.
    """

    def __init__(self, instance, *args, **kwargs):
        self.instance = weakref.ref(instance)
        dict.__init__(self, *args, **kwargs)

    def __getitem__(self, key):
        return dict.__getitem__(self, key).__get__(self.instance(),
                                                   self.instance().__class__)


class PageObject(object):
    """
    Base class for all page objects to extend from.
    void Instance methods implemented by subclasses are provisioned
    with fluent wrappers to facilitate with writing code such as::

        class Google(PageObject):
            def enter_query(self):
                ....

            def submit_search(self):
                ....

            def get_results(self):
                ....

        assert len(Google().enter_query("page objects").submit_search().get_results() > 0)

    """

    def __init__(self, driver, url=None, iframe=None):
        self.driver = driver
        if url:
            self.home = url
        elif driver.current_url:
            self.home = driver.current_url
        self.iframe = iframe
        def update_element(el):
            if issubclass(el.__class__, ElementGetter):
                el.driver = self.driver
                el.iframe = self.iframe
        for el in inspect.getmembers(self.__class__):
            if issubclass(el[1].__class__, list):
                for item in el[1]:
                    update_element(item)
                self.__setattr__(el[0], PageElementList(self, el[1]))
            elif issubclass(el[1].__class__, dict):
                for item in el[1].values():
                    update_element(item)
                self.__setattr__(el[0], PageElementDict(self, el[1]))
            else:
                update_element(el[1])

        if url:
            self.driver.get(url)
        if iframe:
            self.driver.switch_to_frame(iframe)

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
        attr = object.__getattribute__(self, key)
        # check if home url is set, else update.
        if not object.__getattribute__(self, "home"):
            holmium.core.log.debug("home url not set, attempting to update.")
            object.__setattr__(self, "home", object.__getattribute__(self,"driver").current_url)

        if isinstance(attr, types.MethodType):
            @wraps(attr)
            def wrap(*args, **kwargs):
                resp = attr(*args, **kwargs)
                if not resp:
                    holmium.core.log.debug("method %s returned None, using fluent response" % attr.func_name)
                    resp = self
                return resp
            return wrap
        return attr

class ElementGetter(object):
    """
    internal class to encapsulate the logic used by
    :class:`holmium.core.PageElement`
    & :class:`holmium.core.PageElements`
    """

    def __init__(self, locator_type, query_string, base_element=None, timeout=1, value=lambda el:el):
        self.query_string = query_string
        self.locator_type = locator_type
        self.timeout = timeout
        self.driver = None
        self.iframe = None
        self.base_element = base_element
        self.value_mapper = value
        holmium.core.log.debug("locator:%s, query_string:%s, timeout:%d" %
                              (locator_type, query_string, timeout))

    def get_element(self, method = None):
        if self.base_element:
            if isinstance(self.base_element, types.LambdaType):
                el = self.base_element()
                _meth = getattr(el, method.im_func.func_name)
            elif isinstance(self.base_element, PageElement):
                _meth = getattr(self.base_element.__get__(self, self.__class__), method.im_func.func_name)
            elif isinstance(self.base_element, WebElement):
                _meth = getattr(self.base_element, "find_element")
            else:
                holmium.core.log.error("unknown base_element type used: %s" % type(self.base_element))
        else:
            _meth = method
        holmium.core.log.debug("looking up locator:%s, query_string:%s, timeout:%d" %
                              (self.locator_type, self.query_string, self.timeout))
        if self.timeout:
            try:
                WebDriverWait(self.driver, self.timeout).until(lambda _: _meth(self.locator_type, self.query_string))
            except TimeoutException:
                holmium.core.log.debug("unable to find element %s after waiting for %d seconds" % (self.query_string, self.timeout))

        # if the parent page object specified an iframe, thats the context
        # this element will be queried from. the switch_to_default_content
        # is to ensure a double switch doesn't occur.
        if self.driver and self.iframe:
            self.driver.switch_to_default_content()
            self.driver.switch_to_frame(self.iframe)
        return _meth(self.locator_type, self.query_string)


class PageElement(ElementGetter):
    """
    Utility class to get a :class:`selenium.webdriver.remote.webelement.WebElement`
    by querying via one of :class:`holmium.core.Locators`
    """

    def __get__(self, instance, owner):
        if not instance:
            return self
        try:
            return self.value_mapper(enhanced(self.get_element(self.driver.find_element)))
        except NoSuchElementException:
            return None

class PageElements(ElementGetter):
    """
    Utility class to get a collection of :class:`selenium.webdriver.remote.webelement.WebElement`
    objects by querying via one of :class:`holmium.core.Locators`
    """

    def __getitem__(self, idx):
        return lambda: self.__get__(self, self.__class__)[idx]

    def __get__(self, instance, owner):
        if not instance:
            return self
        try:
            return [self.value_mapper(enhanced(el)) for el in self.get_element(self.driver.find_elements)]
        except NoSuchElementException:
            return []


class PageElementMap(PageElements):
    """
    Used to create dynamic dictionaries based on an element locator specified by one of
    :class:`holmium.core.Locators`.

    The wrapped dictionary is an :class:`collections.OrderedDict` instance.

    :param lambda key: transform function for mapping a key to a WebElement in the collection
    :param lambda value: transform function for the value when accessed via the key.
    """
    def __init__(self, locator_type, query_string=None, base_element=None, timeout =1
            , key  = lambda el:el.text, value = lambda el:el):
        PageElements.__init__(self, locator_type, query_string, base_element, timeout)
        self.key_mapper = key
        self.value_mapper = value

    def __get__(self, instance, owner):
        if not instance:
            return self
        try:
            return OrderedDict((self.key_mapper(el), self.value_mapper(enhanced(el))) for el in self.get_element(self.driver.find_elements))
        except NoSuchElementException:
            return {}


    def __getitem__(self, key):
        return lambda:self.__get__(self, self.__class__)[key]


