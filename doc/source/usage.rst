********************
Building PageObjects
********************

Overview
========
.. automodule:: holmium.core 

A typical PageObject built with :mod:`holmium.core` has the following composition:

* :class:`Page`
    * :class:`Element` 
    * :class:`Elements` 
    * :class:`ElementMap` 
    * :class:`Section` 
        * :class:`Element` 
        * :class:`Elements` 
        * :class:`ElementMap` 
    * :class:`Sections` 
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

    g = GooglePage(driver, url="http://www.google.ca")
    g.search_box 
    # <selenium.webdriver.remote.webelement.WebElement object at 0x10b50e450>
    g.google_footer 
    # OrderedDict([(u'Advertising Programs', <selenium.webdriver.remote.webelement.WebElement object at 0x10b35f250>), .....
    g.google_footer["About Google"]
    # <selenium.webdriver.remote.webelement.WebElement object at 0x10b35f450> 
    g.google_footer["About Google"].get_attribute("href")
    # u'http://www.google.ca/intl/en/about.html
    driver.get("http://www.google.co.tz")
    g.google_footer["Kila Kitu Kuhusu Google"].get_attribute("href")
    # u'https://www.google.co.tz/intl/sw/about.html'


Both the element ``search_box`` and the collection of footer links ``google_footer`` are looked up using the driver that was 
passed into the ``GooglePage`` instance.

Sections
========
:class:`Section` objects can be used to further encapsulate 
blocks of page logic that may either be reusable between different pages or
accessed from within different parts of the page in a similar manner. Examples of 
such usecases are menus, footers and collections that may not follow a standard list or map formation. 

Take for example a page with the following structure.

.. code-block:: python

    from holmium.core import Page, Section, Element, Elements, ElementMap, Locators 
    import selenium.webdriver 
    
    headlines_snippet = """
    <html>
        <body>
            <div class='header'>
                <h1>Headlines</h1>
                <h2>Breaking news!!</h2>
            </div>
            <div class='news_section'>
                <ul>
                    <li>
                        <div class='heading'>Big News!!!</div>
                        <div class='content'>Just kidding</div>
                    </li>
                    <li>
                        <div class='heading'>Other Big News!!!</div>
                        <div class='content'>Again, just kidding</div>
                    </li>
                </ul>
            </div> 
        </body>
    </html>"""
    sports_snippet = """
    <html>
        <body>
            <div class='header'>
                <h1>Sports news</h1>
                <h2>Breaking news!!</h2>
            </div>
            <table class="events">
                <tr> 
                    <td class='sport'>Soccer</td>
                    <td class='status'>World cup</td>
                </tr>
                <tr> 
                    <td class='sport'>Cricket</td>
                    <td class='status'>League matches</td>
                </tr>
            </table>
            <div class='news_section'>
                <ul>
                    <li>
                        <div class='heading'>Soccer worldcup finals!!!</div>
                        <div class='content'>I'm running out of meaningful snippets</div>
                    </li>
                    <li>
                        <div class='heading'>Cricket league matches</div>
                        <div class='content'>I'm definitely out.</div>
                    </li>
                </ul>
            </div> 
        </body>
    </html>"""

    class Heading(Section):
        main = Element( Locators.CSS_SELECTOR, "h1")
        sub = Element( Locators.CSS_SELECTOR, "h2")

    class NewsSection(Section):
        articles = ElementMap( Locators.CSS_SELECTOR, "ul>li"
                                , key=lambda el: el.find_element_by_class_name('heading').text 
                                , value=lambda el: el.find_element_by_class_name('content').text
                                )

    class SportsEventsSection(Section):
        events = ElementMap( Locators.CSS_SELECTOR, "tr"
                                , key=lambda el: el.find_element_by_class_name('sport').text 
                                , value=lambda el: el.find_element_by_class_name('status').text
                                )

    class NewsPage(Page):
        heading = Heading(Locators.CLASS_NAME, "header")
        news_section = NewsSection(Locators.CLASS_NAME, "news_section")

    class HeadlinePage(NewsPage):
        pass

    class SportsPage(NewsPage):
        sports_events = SportsEventsSection(Locators.CLASS_NAME, "events")

    driver = selenium.webdriver.Firefox()
    open("/var/tmp/headlines.html","w").write(headlines_snippet)
    open("/var/tmp/sports.html","w").write(sports_snippet)

    headlines = HeadlinePage(driver, "file:///var/tmp/headlines.html")
    print headlines.news_section.articles["Big News!!!"]
    print headlines.heading.main.text

    sports = SportsPage(driver, "file:///var/tmp/sports.html")
    print sports.heading.main.text
    print sports.news_section.articles["Soccer worldcup finals!!!"]
    print sports.sports_events.events["Cricket"]


Though there are two different pages being accessed, they follow a similar structure 
and the ``news_section`` and ``header`` parts can be encapsulated into a
common :class:`Section`. Though the ``events`` section in the sports page isn't
used anywhere else - it still makes it clearer to define it as a :class:`Section`
to separate its logic from the main ``SportsPage``. 

There may be other usecases where :class:`Section` objects may be used to represent 
complex objects within a page that appear repeatedly in a list like manner. To
reduce the duplication of specifying :class:`Section` objects repeatedly in a
:class:`Page` a :class:`Sections` object may be used to obtain an iterable view
of all matched :class:`Section` objects.

.. code-block:: python

    from holmium.core import Page, Section, Element, Elements, ElementMap, Locators 
    import selenium.webdriver 
    
    page_snippet = """
    <html>
        <body>
            <div class='thought'>
                <div class='author'>
                    <span class='user'>John</span>
                    <span class='reputation'>1000</span>
                </div>
                <div class='details'>
                    <div class='brief'>John's world view</div>
                    <div class='full_text'>Sleeping is important</div>
                </div>
            </div>
            <div class='thought'>
                <div class='author'>
                    <span class='user'>Jane</span>
                    <span class='reputation'>100000000</span>
                </div>
                <div class='details'>
                    <div class='brief'>Jane's world view</div>
                    <div class='full_text'>John's world view is not important...</div>
                </div>
            </div>
        </body>
    </html>"""
   
    class ThoughtSections(Sections):
        author = Element(Locator.CLASS_NAME , "user")
        brief = Element(Locator.CSS_SELECTOR , "div.details div.brief")
        full_text = Element(Locator.CSS_SELECTOR , "div.details div.full_text")

    class MainPage(Page):
        thoughts = ThoughtSections(Locators.CLASS_NAME, "thought")


    driver = selenium.webdriver.Firefox()
    open("/var/tmp/page.html","w").write(page_snippet)

    main_page = MainPage(driver, "file:///var/tmp/page.html")
    for thought in main_page.thoughts:
        print thought.author.text 
        print thought.brief.text
        print thought.full_text.text

Collections
===========
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


More Examples
=============

google search 
-------------
.. literalinclude:: ../../examples/google/test_search_text.py 

Wikipedia text search example 
----------------------------- 
.. literalinclude:: ../../examples/wikipedia/test_search_article.py

