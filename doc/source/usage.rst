####################
Building PageObjects
####################

********
Overview
********
.. automodule:: holmium.core 

A typical PageObject built with :mod:`holmium.core` has the following composition:

* :class:`Page`
    * :class:`Element` 
    * :class:`Elements` 
    * :class:`ElementMap` 

A Page is initalized with a :class:`selenium.webdriver.remote.webdriver.WebDriver` 
instance and can take some optional arguments.

.. code-block:: python

    class MyPage(Page):
        pass 

    driver = selenium.webdriver.Firefox()
    p = MyPage(driver)
    p = MyPage(driver, url = "http://www.google.com")
    p = MyPage(driver, url = "http://www.google.com", iframe = "#frame")

Providing the ``url`` argument will result in the driver navigating to the ``url`` 
when the :class:`Page` is initialized. The ``iframe`` argument forces an 
invocation of :meth:`selenium.webdriver.remote.webdriver.WebDriver.switch_to_frame` 
everytime an element in the :class:`Page` is accessed.

The ``webdriver`` that is supplied to a :class:`Page` is used when looking up any 
:class:`Element`, :class:`Elements` or :class:`ElementMap` 
that is declared as a static member. 

To understand the wiring between a :class:`Page` and its elements try out 
the example below in a python repl.

.. code-block:: python

    from holmium.core import Page, Element, Elements, ElementMap, Locators 
    import selenium.webdriver 
    driver = selenium.webdriver.Firefox()
    class GooglePage(Page):
        search_box = Element( Locators.NAME, "q", timeout = 1)
        google_footer = ElementMap ( Locators.CSS_SELECTOR, "#fll>div>a" , timeout = 1 ) 

    g = GooglePage(driver, url="http://www.google.com")
    g.search_box 
    # <selenium.webdriver.remote.webelement.WebElement object at 0x10b50e450>
    g.google_footer 
    # OrderedDict([(u'Advertising Programs', <selenium.webdriver.remote.webelement.WebElement object at 0x10b35f250>), .....
    g.google_footer["Advertising Programs"]
    # <selenium.webdriver.remote.webelement.WebElement object at 0x10b35f450> 
    g.google_footer["Advertising Programs"].get_attribute("href")
    # u'http://www.google.com/intl/en/ads/
    driver.get("http://www.google.tw")
    g.google_footer[u"廣告服務"].get_attribute("href")
    # u'http://www.google.com.tw/intl/zh-TW/ads/'


Both the element ``search_box`` and the collection of footer links ``google_footer`` are looked up using the driver that was 
passed into the ``GooglePage`` instance.

***********
Collections
***********
To keep the interaction with collections of elements in a Page readable and logically grouped - it is useful to represent 
and access such elements in a page the same way as one would a python list or dictionary. The :class:`Elements` and :class:`ElementMap` 
(which is used in the previous example) can be used to organize elements with either relationship.

Using the table defined in ``snippet`` below, a Page can be constructed that allows you to access the ``value`` or ``title`` of each 
row either as a list or a dictionary keyed by the ``title``. 

Take note of the differences in construction of ``element_values`` and ``element_titles``.
Since ``element_values`` does not provide a lookup function via the ``value`` argument, the element returned is a 
pure selenium :class:`selenium.webdriver.remote.webelement.WebElement`. In the case of ``element_titles`` the lookup function extracts 
the text attribute of the element. The same type of lookup functions are used in ``element_map`` to create the key/value pairs. 

.. code-block:: python 

    snippet = """
    <html>
    <body>
    <table>
        <tr> 
            <td class='title'>title 1</td>
            <td class='value'>value one</td>
        </tr>
        <tr> 
            <td class='title'>title 2</td>
            <td class='value'>value two</td>
        </tr>
    </table>
    <body>
    </page>
    """

    from holmium.core import Page,Elements,ElementMap,Locators 
    import selenium.webdriver 

    class Trivial(Page):
        element_values = Elements(Locators.CSS_SELECTOR
                                , "tr>td[class='value']" )
        element_titles = Elements(Locators.CSS_SELECTOR
                                , "tr"
                                , value=lambda el: el.find_element_by_css_selector("td[class='value']").text)
        element_map = ElementMap(Locators.CSS_SELECTOR
                                , "tr" 
                                , key=lambda el: el.find_element_by_css_selector("td[class='title']").text
                                , value=lambda el: el.find_element_by_css_selector("td[class='value']").text)

    driver = selenium.webdriver.Firefox()
    t = Trivial(driver)
    open("/var/tmp/test.html","w").write(snippet)
    driver.get("file:///var/tmp/test.html")
    t.element_values[0].text 
    # u'one' 
    t.element_titles[0] 
    # u'1' 
    t.element_map.keys()
    # [u'1', u'2']
    t.element_map["1"]
    # u'one' 


*************
More Examples
*************

google search 
=============
.. literalinclude:: ../../examples/google/test_search_text.py 

Wikipedia text search example 
============================= 
.. literalinclude:: ../../examples/wikipedia/test_search_article.py

