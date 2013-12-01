import atexit
import tempfile
import sys
import mock
from selenium import webdriver
import os

def build_mock_mapping(name):
    mock_driver = mock.Mock()
    browser_mapping = {name:mock_driver}
    mock_driver.return_value.name = name
    return browser_mapping

phantom = None
def get_driver():
    global phantom
    if not phantom:
        phantom = webdriver.PhantomJS()
        atexit.register(phantom.quit)
    phantom.delete_all_cookies()
    phantom.switch_to_default_content()
    return phantom


def make_temp_page(src):
    f = tempfile.mktemp(".html")
    fh = open(f, "w")
    fh.write(src.replace("\n",""))
    fh.close()
    atexit.register( lambda: os.remove(f) )
    return "file://%s" % f

def mock_open():
    if sys.version_info >= (3,0,0):
        return mock.patch("builtins.open")
    return mock.patch("__builtin__.open")
