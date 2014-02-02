"""
utility callables to be passed to holmium.core.Element(s) only_if parameter
"""
from abc import ABCMeta, abstractmethod
import re
from six import add_metaclass


@add_metaclass(ABCMeta)
class BaseCondition(object):
    """
    base class to implement conditions passed
    to the ``only_if`` parameter of :class:`holmium.core.pageobject.ElementGetter`
    subclasses.
    """
    def __call__(self, element):
        return self.evaluate(element)

    @abstractmethod
    def evaluate(self, element):
        """
        abstract method to be implemented by derived classes.
        """
        raise NotImplementedError


# pylint: disable=invalid-name
class VISIBLE(BaseCondition):
    """
    checks if the element is visible
    """
    def evaluate(self, element):
        return element and element.is_displayed()


class INVISIBLE(BaseCondition):
    """
    checks if the element is invisible
    """
    def evaluate(self, element):
        return not element or not element.is_displayed()

class MATCHES_TEXT(BaseCondition):
    """
    checks if the  element's text matches the provided
    regular expression.
    """
    def __init__(self, expr):
        self.expr = expr
    def evaluate(self, element):
        return element and re.compile(self.expr).match(element.text)


