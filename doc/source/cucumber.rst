.. _fresher: https://github.com/lddubeau/fresher

.. _testing-cucumber:

***********************
Cucumber style Features
***********************
.. automodule:: holmium.core

If cucumber style feature definitions are your cup of tea, holmium provides integration
with `fresher`_. The following features are enabled if both nose plugins are in use
at the same time.

 * Automatic provisioning of webdriver
 * Common :ref:`testing-cucumber-steps` for accessing page objects and page elements
 * Access to holmium config (:class:`holmium.core.Config`) variables via jinja2 templates in scenario steps.


Setup
=====
Before reading this section, I would strongly recommend browsing through the documentation
for `fresher`_. If you're already familiar - read on..

Holmium+Fresher features require the same structure as regular fresher features, i.e.

.. code-block:: bash

    my_feature/
    |- config.py
    |- awesome.feature
    |- lame.feature
    |- steps.py

steps.py
--------
To enable the scenario step expressions that are bundled with holmium, your `steps` module will require
registration of these steps via the following snippet

.. code-block:: python


    from holmium.core.cucumber import init_steps
    init_steps()



Subsequently, you will also have to ensure that the :class:`Page` objects that you want to drive in the
scenarios have been imported in the scope of your `steps` module. Once that is done, you can move on to writing
your features.


.. _testing-cucumber-steps:

Step definitions
================

Browser control
---------------
.. code-block:: cucumber

    When I access the {{url}}
    When I go back
    And I go forward
    Then I should see the title {{title}}


Page access
-----------
.. code-block:: cucumber

    When I access the {{PageObject}} at {{url}}

Element visibility/content
--------------------------

.. code-block:: cucumber

    Then the element {{Element}} should be visible
    Then the element {{Element}} should have text {{text}}
    Then the {{key/attr/index}} in {{Elements/ElementMap/Section}} should be visible
    Then the {{key/attr/index}} in {{Elements/ElementMap/Section}} should have text {{text}}
    Then the {{key/attr/index}} item for the {{key/index}} item in {{Sections}} should be visible
    Then the {{key/attr/index}} item for the {{index}} item in {{Sections}} should have text {{text}}

Element interaction
-------------------

.. code-block:: cucumber

    When I type {{text}} in element {{Element}}
    When I type {{text}} in the {{key/attr/index}} item in {{Elements/ElementMap/Section}}
    When I press enter in element {{Element}}
    When I press enter in the {{key/attr/index} item in element {{Element}}
    When I click element {{Element}}
    When I click the {{key/attr/index}} item in {{Elements/ElementMap/Section}}
    When I wait for {{seconds}} second(s)

Page method execution
---------------------

.. code-block:: cucumber

    When I perform {{method_name}} on the page {{PageObject}}
    When I perform {{method_name}} on the page {{PageObject}} with arguments {{comma_separated_args}}



Full example
============

With the following directory structure and content

.. code-block:: bash

    google_feature
    |- page.py
    |- search.feature
    |- steps.py

page.py
-------

.. code-block:: python



    from holmium.core import Page, Sections, Locators, Element
    from selenium.webdriver.common.keys import Keys

    class Results(Sections):
        link = Element(Locators.CSS_SELECTOR, "h3.r")
        description = Element(Locators.CLASS_NAME, "st")

    class GooglePage(Page):
        search_box = Element(Locators.NAME, "q")
        search_results = Results(Locators.CSS_SELECTOR, "li.g", timeout=5)
        next = Element(Locators.LINK_TEXT, "Next")
        def search(self, text):
            self.search_box.send_keys(text)
            self.search_box.send_keys(Keys.ENTER)



steps.py
--------

.. code-block:: python


    from holmium.core.cucumber import init_steps
    from page import GooglePage
    init_steps()

google.feature
--------------

.. code-block:: cucumber

    Feature: Google search
        Scenario: Search for selenium
            When I access the page GooglePage at url http://www.google.com
            Then I should see the title Google
            When I perform search with arguments selenium python documentation
            Then the element search_results should be visible
            And the element search_results should have 10 items
            And the link of the first item in search_results should have the text Selenium with Python — Selenium Python Bindings 2 documentation
            And the element next should have the text Next
            When I click the element next
            And I go back
            Then the link of the first item in search_results should have the text Selenium with Python — Selenium Python Bindings 2 documentation


Execution
---------
All the nose plugin options defined at :ref:`testing-nose` can be used here.


.. code-block:: bash

    nosetests --with-fresher --with-holmium --holmium-browser=firefox google_feature




