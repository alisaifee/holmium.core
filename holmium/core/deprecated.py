import types
import pageobject
import ut_helper
import warnings
class Deprecated(object):
    def __new__(cls, *args, **kwargs):
        warnings.warn("The use of %s is deprecated. Use %s instead" % ( cls.cur, cls.alt.__name__)
                , DeprecationWarning
                , stacklevel=2 )
        return super(Deprecated, cls).__new__(cls)

def construct_deprecated(name, alt):
    doc  = """Deprecated alias for :class:`%s`""" % alt.__name__
    cls = types.ClassType(name, (Deprecated, alt), dict(cur=name,alt=alt, __doc__ = doc))
    return cls

PageObject = construct_deprecated("PageObject", pageobject.Page)
PageElement = construct_deprecated("PageElement", pageobject.Element)
PageElements = construct_deprecated("PageElements", pageobject.Elements)
PageElementMap = construct_deprecated("PageElementMap", pageobject.ElementMap)
HolmiumTestCase = construct_deprecated("HolmiumTestCase", ut_helper.TestCase)

warnings.simplefilter("always")
