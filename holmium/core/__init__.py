"""
holmium.core

"""
from .config import Config
from .logger import log
from .testcase import TestCase
from .pageobject import Locators, Page, Section, Sections, Element, Elements
from .pageobject import ElementMap
from .noseplugin import HolmiumNose
from .deprecated import PageObject, PageElement, PageElements
from .deprecated import PageElementMap, HolmiumTestCase
from .enhancers import register_enhancer, get_enhancers
from .enhancers import reset_enhancers, ElementEnhancer


from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
