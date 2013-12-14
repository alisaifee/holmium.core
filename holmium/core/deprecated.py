"""
aliases so that a real error message is displayed if someone
uses the old class named
"""
from .pageobject import Page, Element, Elements, ElementMap
from .testcase import TestCase

# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods
# pylint: disable=no-member

class Deprecated(object):
    """
    meta class to create an object that throws a Syntax error on
    construction
    """
    def __new__(cls, *_):
        raise SyntaxError(
            "%s has been removed as of version 0.4. Use %s instead" % (
                cls.cur, cls.alt.__name__
            )
        )


def construct_deprecated(name, alt):
    """
    create a type for the alias
    """
    doc = """Deprecated alias for :class:`%s`""" % alt.__name__
    cls = type(name, (Deprecated, alt),
               dict(cur=name, alt=alt, __doc__=doc))
    return cls


PageObject = construct_deprecated("PageObject", Page)
PageElement = construct_deprecated("PageElement", Element)
PageElements = construct_deprecated("PageElements", Elements)
PageElementMap = construct_deprecated("PageElementMap", ElementMap)
HolmiumTestCase = construct_deprecated("HolmiumTestCase", TestCase)

