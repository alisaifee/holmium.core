"""
implementation of element enhancer base
"""


from selenium.webdriver.support.ui import Select


class ElementEnhancer(object):
    """
    base class for implementing custom element enhancers to
    add functionality to located webelements based on the
    element type (tag name)
    """
    # pylint: disable=too-few-public-methods
    __TAG__ = ""
    def __init__(self, element):
        self.element = element
        super(ElementEnhancer, self).__init__()

    @classmethod
    def matches(cls, element):
        """
        class method to verify that this enhancer is appropriate
        for the provided webelement
        """
        return cls.__TAG__.lower() == element.tag_name.lower()

    def __getattribute__(self, key):
        element = object.__getattribute__(self, "element")
        try:
            try:
                return super(ElementEnhancer, self).__getattribute__(key)
            except AttributeError:
                return element.__getattribute__(key)
        except:
            raise AttributeError(
                "neither %s, nor %s object has an attribute %s" % (
                self.__class__.__name__, element.__class__.__name__, key))


class _SelectMixin(Select, object):
    """
    cooperative super version of Select
    """
    def __init__(self):
        super(_SelectMixin, self).__init__(self.element)
        Select.__init__(self, self.element)

class SelectEnhancer(ElementEnhancer, _SelectMixin):
    """
    Enhancer for the select tag
    """
    __TAG__ = "select"


REGISTERED_ENHANCERS = [SelectEnhancer]

def register_enhancer(enhancer):
    """
    registers a :class:`ElementEnhancer` with the internal
    lookup
    """
    if not issubclass(enhancer, ElementEnhancer):
        raise TypeError(
            "Only subclasses of holmium.core.ElementEnhancer can be registered")
    if not hasattr(enhancer, "__TAG__") or not enhancer.__TAG__:
        raise AttributeError(
            "ElementEnhancer implementations must declare a __TAG__"
            "property to match against"
        )

    REGISTERED_ENHANCERS.insert(0, enhancer)

def reset_enhancers():
    """
    resets the state so that any :class:`ElementEnhancer` that was registered
    via a call to :func:`register_enhancer` is removed.
    """
    global REGISTERED_ENHANCERS
    REGISTERED_ENHANCERS = [SelectEnhancer]

def get_enhancers():
    """
    returns the global registered enhancers
    """
    return REGISTERED_ENHANCERS


