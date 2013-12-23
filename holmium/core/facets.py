"""
implementation of facet bases and builtin facets
"""

import inspect
import weakref

from abc import ABCMeta, abstractmethod
import re

# pylint: disable=no-name-in-module,abstract-class-not-used
from nose.tools import assert_equals, assert_true
from .logger import log

class Facet(object):
    """
    base class to implement an attribute of a page
    """
    __ARGS__ = []
    __OPTIONS__ = {}
    __ALLOW_MULTIPLE__ = True
    __metaclass__ = ABCMeta

    def __init__(self, required=True, debug=False, **kwargs):
        self.arguments = {}
        self.options = {}
        self.required = required
        self.debug = debug
        self._parent_class = None
        for arg in self.__ARGS__:
            if arg not in kwargs.keys():
                raise AttributeError("%s is a required argument for %s" % (
                arg, self.__class__.__name__))
            else:
                self.arguments[arg] = kwargs[arg]
                kwargs.pop(arg)
        for arg in self.__OPTIONS__:
            if arg in kwargs.keys():
                self.options[arg] = kwargs[arg]
                kwargs.pop(arg)
            else:
                self.options[arg] = self.__OPTIONS__[arg]
        if kwargs:
            raise AttributeError("unknown argument(s) to %s (%s)" % (
            self.__class__.__name__, ",".join(kwargs.keys())))

    def register(self, obj):
        """
        registers a :class:`Facet` on an object

        :param holmium.core.facets.Faceted obj: the object to register the
         facet on.
        """
        if inspect.isclass(obj):
            obj.get_class_facets().append(self)
            self.parent_class = obj
        else:
            obj.get_instance_facets().append(self)
            self.parent_class = obj.__class__


    def __call__(self, obj):
        self.register(obj)
        return obj

    def get_name(self):
        """
        returns the class name of the facet
        """
        return self.__class__.__name__

    @property
    def parent_class(self):
        """
        returns the parent class
        """
        return self._parent_class()

    @parent_class.setter
    def parent_class(self, parent):
        """
        sets the parent class
        """
        self._parent_class = weakref.ref(parent)

    def get_parent_name(self):
        """
        returns the class name of the parent
        """
        return (self.parent_class and self.parent_class.__name__) or None

    @abstractmethod
    def evaluate(self, driver):
        """
        evaluate whether this facet holds true. Raise an Exception
        if not.

        :param selenium.webdriver.remote.webdriver.WebDriver driver: the
         webdriver
        """


class FacetError(Exception):
    """
    exception raised when a facet has an error
    or can't complete

    :param holmium.core.facets.Facet facet: the facet that failed to evaluate
    :param exceptions.Exception exc: the inner exception that caused the failure
    """

    def __init__(self, facet, exc=None):
        self.message = "%s failed to exhibit facet %s" % (
            facet.get_parent_name(), facet.get_name())
        if exc:
            self.message += " with error %s" % exc
        super(FacetError, self).__init__(self.message)


class FacetCollection(list):
    """
    utility collection class for pageobjects to encapsulate
    facets
    """

    def __init__(self, *a):
        super(FacetCollection, self).__init__(*a)

    @property
    def type_map(self):
        """
        view on the list to help with figuring out
        if a facet of the same type already exists
        """
        type_mmap = {}
        for item in self:
            type_mmap.setdefault(type(item), []).append(item)
        return type_mmap

    def append(self, item):
        """
        overridden add method to pop the last
        item if its type does not support multiple
        facets on the same object.
        """
        if (
            self.type_map.has_key(type(item))
            and not type(item).__ALLOW_MULTIPLE__
        ):
            self.remove(self.type_map[type(item)].pop())
        if item not in self:
            super(FacetCollection, self).append(item)



    def evaluate_all(self, driver):
        """
        iterate over all registered :class:`Facet` objects and validate them

        :param selenium.webdriver.remote.webdriver.WebDriver driver:
         the webdriver
        """
        for facet in self:
            try:
                facet.evaluate(driver)
            # pylint: disable=broad-except
            except Exception as _:
                if facet.debug:
                    log.warn(FacetError(facet, _))
                elif facet.required:
                    raise FacetError(facet, _)

class CopyOnCreateFacetCollectionMeta(ABCMeta):
    """
    makes a new copy of any :class:`FacetCollection`
    instances upon creating the class. This is to ensure
    that different derived classes of :class:`Page`
    do not clobber the class facets of the base class.
    """

    def __init__(cls, *args):
        super(CopyOnCreateFacetCollectionMeta, cls).__init__(*args)
        visited = {}
        for superclass in cls.__mro__:
            for key, value in vars(superclass).items():
                if isinstance(value, (FacetCollection)):
                    visited.setdefault(key, FacetCollection())
                    for facet in value:
                        visited[key].append(facet)
                    setattr(cls, key, FacetCollection(visited[key]))
class Faceted(object):
    """
    mixin for objects that want to have facets registered
    on them.
    """
    __metaclass__ = CopyOnCreateFacetCollectionMeta

    def __init__(self):
        self.instance_facets = FacetCollection()
        super(Faceted, self).__init__()

    @classmethod
    def get_class_facets(cls):
        """
        returns the facets registered on the class (presumably
        via a decorator)
        """
        if not hasattr(cls, "class_facets"):
            cls.class_facets = FacetCollection()
        return cls.class_facets

    def get_instance_facets(self):
        """
        returns the facets registered on the instance
        """
        return object.__getattribute__(self, "instance_facets")


    def evaluate(self):
        """
        evaluates all registered facets (class & instance)
        """
        from .pageobject import Page

        safe_get = lambda e: object.__getattribute__(self, e)
        driver = Page.get_driver()
        instance_facets = safe_get("get_instance_facets")()
        class_facets = safe_get("get_class_facets")()

        class_facets.evaluate_all(driver)
        instance_facets.evaluate_all(driver)


class Defer(Facet):
    """
    :param holmium.core.Page page: the page object that is expected to be
     deferred to
    :param function action: a callable that takes the page object instance as
     the first argument
    :param dict action_arguments: (optional) dictionary of arguments to pass to
     `action`
    :param bool debug: if True a failure to evaluate will not result in an
     exception, only a log warning
    :param bool required: if False a failure to evaluate will be treated as a
     noop.
    """
    __ARGS__ = ["page", "action"]
    __OPTIONS__ = {"action_arguments": {}}

    def evaluate(self, driver):
        page_cls = self.arguments["page"]
        page = page_cls(driver)
        return self.arguments["action"](page,
                                        **self.options["action_arguments"]
        )


class Title(Facet):
    """
    enforces the title of the current page.

    :param str title: a regular expression to match the title.
    :param bool debug: if True a failure to evaluate will not result in an
     exception, only a log warning
    :param bool required: if False a failure to evaluate will be treated as
     a noop.
    """
    __ARGS__ = ["title"]
    __ALLOW_MULTIPLE__ = False
    def evaluate(self, driver):
        assert_true(re.compile(self.arguments["title"]).match(driver.title),
                    "title did not match %s" % self.arguments["title"]
        )


class Cookie(Facet):
    """
    enforces the existence (and optionally the value) of a cookie.

    :param str name: name of the cookie
    :param dict value: (optional) dict (or callable) to validate the value of
     the cookie.
    :param bool debug: if True a failure to evaluate will not result in an
     exception, only a log warning
    :param bool required: if False a failure to evaluate will be treated as
     a noop.

    """
    __ARGS__ = ["name"]
    __OPTIONS__ = {"value": None}

    def evaluate(self, driver):
        cookie_value = driver.get_cookie(self.arguments["name"])
        if cookie_value and self.options["value"]:
            if callable(self.options["value"]):
                assert self.options["value"](cookie_value)
            else:
                assert_equals( cookie_value , self.options["value"] )
        else:
            assert_true(cookie_value != None,
                        "cookie %s does not exist" % self.arguments["name"]
            )


class Strict(Facet):
    """
    enforces that every element declared in the :class:`Page` or
    :class:`Section` be present.

    :param bool debug: if True a failure to evaluate will not result in an
     exception, only a log warning
    :param bool required: if False a failure to evaluate will be treated as a
     noop.
    """

    def evaluate(self, driver):
        pass # pragma: no cover

    def __call__(self, obj):
        from .pageobject import ElementGetter

        for element in inspect.getmembers(obj):
            if isinstance(element[1], ElementGetter):
                element[1].is_facet = True
                element[1].is_debug_facet = self.debug
        return obj


class ElementFacet(Facet):
    """
    utility trait used when validating an
    :class:`holmium.core.pageobject.ElementGetter` subclass
    """

    def __init__(self, element, element_name, **kwargs):
        self.element_name = element_name
        self.element = element
        super(ElementFacet, self).__init__(required=True, **kwargs)

    def evaluate(self, driver):
        assert_true(self.element.__get__(self.parent_class, self.parent_class),
                     "No such element"
        )

    def get_name(self):
        return self.element_name

# pylint: disable=invalid-name
cookie = Cookie
strict = Strict
defer = Defer
title = Title

