from .pageobject import *
from .testcase import *


class Deprecated(object):
    def __new__(cls, *args, **kwargs):
        raise SyntaxError("%s has been removed as of version 0.4. Use %s instead" % (
            cls.cur, cls.alt.__name__
            )
        )


def construct_deprecated(name, alt):
    doc = """Deprecated alias for :class:`%s`""" % alt.__name__
    cls = type(name, (Deprecated, alt),
                    dict(cur=name, alt=alt, __doc__=doc))
    return cls


PageObject = construct_deprecated("PageObject", Page)
PageElement = construct_deprecated("PageElement", Element)
PageElements = construct_deprecated("PageElements", Elements)
PageElementMap = construct_deprecated("PageElementMap", ElementMap)
HolmiumTestCase = construct_deprecated("HolmiumTestCase", TestCase)

