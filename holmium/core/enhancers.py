from selenium.webdriver.support.ui import Select


class ElementEnhancer(object):
    """
    base class for implementing custom element enhancers to
    add functionality to located webelements based on the
    element type (tag name)
    """
    __TAG__ = ""

    def __init__(self, element):
        self.element = element

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
            return object.__getattribute__(self, key)
        except:
            return element.__getattribute__(key)


class _Select(Select, object):
    """
    cooperative super version of Select
    """
    def __init__(self, webelement):
        super(_Select, self).__init__(webelement)
        Select.__init__(self, webelement)

class SelectEnhancer(ElementEnhancer, _Select):
    __TAG__ = "select"
    def __init__(self, element):
        super(SelectEnhancer, self).__init__(element)


registered_enhancers = [SelectEnhancer]

def register_enhancer(enhancer):
    """
    registers a :class:`ElementEnhancer` with the internal
    lookup
    """
    if not issubclass(enhancer, ElementEnhancer):
        raise TypeError(
            "Only subclasses of holmium.core.ElementEnhancer can be registered")
    registered_enhancers.insert(0, enhancer)

def reset_enhancers():
    """
    resets the state so that any :class:`ElementEnhancer` that was registered
    via a call to :func:`register_enhancer` is removed.
    """
    global registered_enhancers
    registered_enhancers = [SelectEnhancer]

def get_enhancers():
    global registered_enhancers
    return registered_enhancers