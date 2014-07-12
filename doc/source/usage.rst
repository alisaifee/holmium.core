********************
Building PageObjects
********************

Overview
========
.. currentmodule:: holmium.core 

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
        google_footer = ElementMap ( Locators.CSS_SELECTOR, "#fsl>a" , timeout = 1 )

    g = GooglePage(driver, url="http://www.google.ca")
    g.search_box 
    # <selenium.webdriver.remote.webelement.WebElement object at 0x10b50e450>
    g.google_footer 
    # OrderedDict([(u'Advertising', <selenium.webdriver.remote.webelement.WebElement object at 0x10b35f250>), .....
    g.google_footer["About"]
    # <selenium.webdriver.remote.webelement.WebElement object at 0x10b35f450> 
    g.google_footer["About"].get_attribute("href")
    # u'http://www.google.ca/intl/en/about.html?fg=1'
    driver.get("http://www.google.co.tz")
    g.google_footer["Kuhusu Google"].get_attribute("href")
    # u'https://www.google.co.tz/intl/sw/about.html?fg=1'


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

.. WARNING::
    Though one could be inclined to treat :class:`Sections` as any other collection 
    please only use them as an iterable or do indexed access directly on the
    :class:`Sections` object. Trying to cast a :class:`Sections`
    property into a list is not supported.

.. code-block:: python

    from holmium.core import Page, Sections, Element, Elements, ElementMap, Locators 
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
        author = Element(Locators.CLASS_NAME , "user")
        brief = Element(Locators.CSS_SELECTOR , "div.details div.brief")
        full_text = Element(Locators.CSS_SELECTOR , "div.details div.full_text")

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

.. _usage-conditions

Conditions
==========
For any non-trivial web page, asynchronous changes to the dom are expected. This
requires test authors to often place explicit waits for conditions such as visibility
and content changes. To reduce the effort of describing these conditionals, page elements
:class:`Element`, :class:`Elements` and :class:`ElementMap` accept a keyword argument ``only_if``:
a callable that expects a :class:`selenium.webdriver.remote.webelement.WebElement` and is
expected to return ``True/False``. When coupled with the keyword argument ``timeout``,
access to a page object's element is internally subjected to an explicit wait.

Some common conditions are provided and can be used to further simplify the declaration of pageobject:

.. currentmodule:: holmium.core.conditions
.. autoclass:: VISIBLE
.. autoclass:: INVISIBLE
.. autoclass:: MATCHES_TEXT
.. autoclass:: ANY
.. autoclass:: ALL
.. currentmodule:: holmium.core


You can build your own condition objects by subclassing :class:`conditions.BaseCondition`
and implementing the :meth:`conditions.BaseCondition.evaluate` method.

Sample
------

.. code-block:: python

    from holmium.core import conditions, Page, Element, Locators

    class MyPage(Page):
        required_element = Element(Locators.CLASS_NAME, "main_element",
                                    only_if=conditions.VISIBLE(),
                                    timeout = 5)
        delayed_element = Element(Locators.CLASS_NAME, "text_element",
                                    only_if=conditions.MATCHES_TEXT('^ready.*'),
                                    timeout = 5)



In the above example, ``required_element`` will return ``None`` unless it is displayed. The 5 second
timeout will take effect everytime the element is accessed. Similarly, ``delayed_element`` will return
``None`` until the text of the element matches a string that starts with ``ready``.


Context Managers
----------------
Conditions can also be used as context managers in cases where condition parameters are not known
at page object declaration time. For example::

    from holmium.core import Page, ElementMap
    from holmium.core.conditions import ANY, MATCHES_TEXT

    class MyPage(Page):
        dynamic_element_collection = ElementMap(Locators.CLASS_NAME, "dynamic", timeout = 5)

        def get_element(self, name):
            with ANY(MATCHES_TEXT(name)):
                return self.dynamic_element_collection[name]

.. _usage-facets:

Page Facets
===========
Beyond elements maintained by a page, there are other characteristics that can
define the behavior of a Page or Section. Holmium allows you to decorate a page
with a :class:`facets.Facet` which ensures evaluation of the facet before 
the first access on the Page or Section.

Builtin facets
--------------

.. currentmodule:: holmium.core.facets
.. autoclass:: Title
.. autoclass:: Cookie
.. autoclass:: Strict
.. autoclass:: Defer

For good measure, lowercased aliases are available for builtin facets:

.. autoclass:: title
.. autoclass:: strict
.. autoclass:: cookie
.. autoclass:: defer

.. currentmodule:: holmium.core

Rolling your own
----------------
You can create your own facet decorator by subclassing :class:`facets.Facet` and implementing the
:func:`facets.Facet.evaluate` method. Any additional arguments that you want to access during evaluation
should be declared as the following class members:

    * required arguments as an **__ARGS__** list
    * optional arguments as an **__OPTIONS__** dictionary.


You can also declare an **__ALLOW_MUTLIPLE__** property on your facet which will control
the expectation from multiple decorations of the same facet type. If set to ``False``
the last facet decorator applied will be respected (for example as with the :class:`facets.title`
facet - for which it only makes sense to respect the last decorator applied).

The example facet below would require that `color` as an argument, and would optionally
accept `image`. When the  facet is evaluated it would assert on the `background-color` of the body
element and optionally, the `background-image`.


.. code-block:: python

    class background(Facet):
        __ARGS__ = ["color"]
        __OPTIONS__ = {"image": None}
        def validate(self, driver):
            body = driver.find_element_by_tag_name("body")
            assert_equals( self.arguments["color"], body.value_of_css_property("background-color")
            if self.options["image"]:
                assert_equals( self.options["image"], body.value_of_css_property("background-image")




The decorater could then be applied as follows

.. code-block:: python

    @background(color="rgb(255, 255, 255)", image="none")
    class Google(Page):
        google_button = Element(Locators.NAME, "btnK")


Additionally individual  :class:`Element`, :class:`ElementMap` or :class:`Elements` members of a Page or Section
can be promoted to a facet by adding the `facet=True` keyword argument. This will ensure that the specified element 
is **required** at the time of the containers first access.


Sample
------

.. code-block:: python

    from holmium.core import facets, Page, Element, Section, Locators

    class MySection(Section):
        required_element = Element(Locators.CLASS_NAME, "main_element", facet=True)
        optional_element = Element(Locators.CLASS_NAME, "secondary_element")

    @facets.title(title='login page')
    class LoginPage(Page):
        def do_login(self, username, password):
            .....

    @facets.cookie(name="session")
    @facets.defer(page=LoginPage, action=LoginPage.do_login, action_arguments= {"username":"ali", "password":"sekret"})
    class ContentPage(Page):
        section = MySection(Locators.ID, "main-section")



To understand how the facets are evaluated, consider the following code path


.. code-block:: python

    from selenium import webdriver

    driver = webdriver.Firefox()

    p = ContentPage(driver, "http://localhost/content")
    assert p.section.optional_element != None


The chain of execution when calling `p.section.required_element` is as follows

* check defer to `LoginPage`
* check `title` of `LoginPage`
* perform `do_login`
* check `cookie` of `ContentPage`
* check `required` element exists in `MySection`
* return `optional_element`

Customizing page elements
=========================

To further customize domain / page specific behaviors of certain web elements, the :class:`ElementEnhancer`
base class can be extended to hijack :class:`selenium.webdriver.remote.webelement.WebElement`. The located
web element is made available to the subclass as ``self.element``.


In the sample below, the ``SelectEnhancer`` enhancer will be used to hijack any web element that has the tag name
`select`. All properties and methods exposed by the :class:`selenium.webdriver.remote.webelement.WebElement` object
will still be accessible, and extra methods/properties (such as 'options') will be added on. You can register your own
:class:`ElementEnhancer` via a call to :func:`register_enhancer` and subsequently reset them via a call to
:func:`reset_enhancers`.


By default, holmium only installs a SelectEnhancer that shadows :class:`selenium.webdriver.support.select.Select`.

.. code-block:: python

    class SelectEnhancer(ElementEnhancer):
        __TAG__ = "select"
        @property
        def options(self):
            return self.element.find_elements_by_tag_name("option")
        
        def has_option(self, option_name):
            return any([k.text == option_name for k in self.options])

    holmium.core.register_enhancer(SelectEnhancer)


More Examples
=============

google search 
-------------
.. literalinclude:: ../../examples/google/test_search_text.py 

Wikipedia text search example 
----------------------------- 
.. literalinclude:: ../../examples/wikipedia/test_search_article.py

