import atexit
import tempfile
import sys
import mock
from selenium import webdriver
import os


def build_mock_mapping(name):
    mock_driver = mock.Mock()
    browser_mapping = {name: mock_driver}
    mock_driver.return_value.name = name
    return browser_mapping


test_driver = None


def get_driver():
    global test_driver
    if not test_driver:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        chrome = webdriver.Chrome(chrome_options=options)
        atexit.register(chrome.quit)
    chrome.delete_all_cookies()
    chrome.switch_to.default_content()
    return chrome


def make_temp_page(src):
    f = tempfile.mktemp(".html")
    fh = open(f, "w")
    fh.write(src.replace("\n", ""))
    fh.close()
    atexit.register(lambda: os.remove(f))
    return "file://%s" % f


def mock_open():
    if sys.version_info >= (3, 0, 0):
        return mock.patch("builtins.open")
    return mock.patch("__builtin__.open")
