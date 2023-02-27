"""
holmium.core

"""
from ._version import get_versions
from .config import Config
from .enhancers import (
    ElementEnhancer,
    get_enhancers,
    register_enhancer,
    reset_enhancers,
)
from .logger import log
from .pageobject import Element, ElementMap, Elements, Locators, Page, Section, Sections
from .testcase import TestCase

__version__ = get_versions()["version"]
del get_versions


__all__ = [
    "Config",
    "log",
    "TestCase",
    "Locators",
    "Page",
    "Section",
    "Sections",
    "Element",
    "Elements",
    "ElementMap",
    "register_enhancer",
    "get_enhancers",
    "reset_enhancers",
    "ElementEnhancer",
]
