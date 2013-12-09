from selenium.webdriver.support.ui import Select


class ElementEnhancer(object):
    """
    base class for implementing custom element enhancers to
    add functionality to located webelements based on the
    element type (tag name)
    """

    def __init__(self, element):
        self.element = element
        super(ElementEnhancer, self).__init__()

    @classmethod
    def matches(self, element):
        """
        class method to verify that this enhancer is appropriate
        for the provided webelement
        """
        return self.__TAG__.lower() == element.tag_name.lower()

    def __getattribute__(self, key):
        element = object.__getattribute__(self, "element")
        try:
            try:
                return super(ElementEnhancer, self).__getattribute__(key)
            except Exception, e:
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
    __TAG__ = "select"


registered_enhancers = [SelectEnhancer]

def register_enhancer(enhancer):
    """
    registers a :class:`ElementEnhancer` with the internal
    lookup
    """
    if not issubclass(enhancer, ElementEnhancer):
        raise TypeError(
            "Only subclasses of holmium.core.ElementEnhancer can be registered")
    if not hasattr(enhancer, "__TAG__"):
        raise AttributeError("ElementEnhancer implementations must declare a __TAG__ property to match against")

    registered_enhancers.insert(0, enhancer)

def reset_enhancers():
    """
    resets the state so that any :class:`ElementEnhancer` that was registered
    via a call to :func:`register_enhancer` is removed.
    """
    global registered_enhancers
    registered_enhancers = [SelectEnhancer]

def get_enhancers():
    return registered_enhancers