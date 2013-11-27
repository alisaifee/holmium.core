import types
import warnings
import pageobject
import testcase


class Deprecated(object):
    def __new__(cls, *args, **kwargs):
        raise SyntaxError("%s has been removed as of version 0.4. Use %s instead" % (
            cls.cur, cls.alt.__name__
            )
        )


def construct_deprecated(name, alt):
    doc = """Deprecated alias for :class:`%s`""" % alt.__name__
    cls = types.ClassType(name, (Deprecated, alt),
                          dict(cur=name, alt=alt, __doc__=doc))
    return cls


PageObject = construct_deprecated("PageObject", pageobject.Page)
PageElement = construct_deprecated("PageElement", pageobject.Element)
PageElements = construct_deprecated("PageElements", pageobject.Elements)
PageElementMap = construct_deprecated("PageElementMap", pageobject.ElementMap)
HolmiumTestCase = construct_deprecated("HolmiumTestCase", testcase.TestCase)

warnings.simplefilter("always")
