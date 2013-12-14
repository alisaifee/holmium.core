"""
holmium.core

"""
from .config import Config
from .logger import log
from .testcase import TestCase
from .pageobject import Locators, Page, Section, Sections, Element, Elements
from .pageobject import ElementMap
from .noseplugin import HolmiumNose
from .deprecated import PageObject, PageElement, PageElements, PageElementMap \
    , HolmiumTestCase
from .enhancers import register_enhancer, get_enhancers, reset_enhancers, \
    ElementEnhancer

