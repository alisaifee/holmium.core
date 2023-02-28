.. :changelog:
.. _Deprecated old class names: http://holmiumcore.readthedocs.org/en/latest/core.html#deprecated-classes
.. _Config object: http://holmiumcore.readthedocs.org/en/latest/internals.html#holmium.core.Config
.. _Section object: https://holmiumcore.readthedocs.org/en/latest/usage.html#sections
.. _Facets: http://holmiumcore.readthedocs.org/en/latest/usage.html#page-facets
.. _Cucumber Features: http://holmiumcore.readthedocs.org/en/latest/cucumber.html
.. _fresher: https://github.com/lddubeau/fresher
.. _ElementEnhancer: http://holmiumcore.readthedocs.org/en/latest/usage.html#customizing-page-elements
.. _conditions: http://holmiumcore.readthedocs.org/en/latest/usage.html#conditions

Changelog
=========

v1.1.0
------
Release Date: 2023-02-28

* Chores

  * Remove dependency on six & ordereddict
  * Upgrade syntax to python 3.7+
  * Automate pypi release process

v1.0.0
------
Release Date: 2023-02-27

* Breaking Changes

  * Remove support for python < 3
  * Remove support for nose plugin
  * Remove support for cucumber tests


v0.8.5
------
Release Date: 2016-09-06

* Extra options for assertConditionWithWait `#42 <https://github.com/alisaifee/holmium.core/issues/42>`_

v0.8.4
------
Release Date: 2016-09-01

* Bug fix: assertConditionWithWait `#40 <https://github.com/alisaifee/holmium.core/issues/40>`_

v0.8.3
------
Release Date: 2016-08-12

* Bug fix: Fix for IE with remote `#38 <https://github.com/alisaifee/holmium.core/issues/38>`_
* Bug fix: StaleElementReferenceException handling `#33 <https://github.com/alisaifee/holmium.core/issues/33>`_

v0.8.2
------
Release Date: 2015-12-22

* New filter_by argument that accepts conditions

v0.8.1
------
Release Date: 2015-10-30

* Bug fix: Fix setup requirements for python 3.x #30

v0.8
====
Release Date: 2015-06-07

* No functional Change

v0.7.9
------
Release Date: 2015-05-30

* Bug fix: Support for phantom 1.9.x `#29 <https://github.com/alisaifee/holmium.core/issues/29>`_

v0.7.8
------
Release Date: 2014-11-02

* Bug fix: AttributeError when comparing with None `#26 <https://github.com/alisaifee/holmium.core/issues/26>`_
* Bug fix: Negative indexing in sections `#27 <https://github.com/alisaifee/holmium.core/issues/27>`_

v0.7.7
------
Release Date: 2014-09-05

* Bug fix: IE Driver initialization `#24 <https://github.com/alisaifee/holmium.core/issues/24>`_

v0.7.6
------
Release Date: 2014-07-14

* Hot fix: broken installation due to missing requirements

v0.7.5
------
Release Date: 2014-07-14

* Bug fix for ``StaleElementReferenceException`` in WebDriverWait
* Support for using ``holmium.core.coniditions`` objects as
  `context managers
  <http://holmiumcore.readthedocs.org/en/latest/usage.html#context-managers>`_
* Additional conditions ``ANY`` and ``ALL`` for element collections.

v0.7.4
------
Release Date: 2014-04-24

* Bug fix: Sections weren't working for index > 1 `#22 <https://github.com/alisaifee/holmium.core/issues/22>`_

v0.7.3
------
Release Date: 2014-03-14

* Add missing timeout from Section

v0.7.2
------
Release Date: 2014-02-22

* exclude packaging tests

v0.7.1
------
Release Date: 2014-02-18

* Fix packaging problem with versioneer

v0.7
====
Release Date: 2014-02-10

* Built-in `conditions`_ for explicit waits
* New assertion ``assertConditionWithWait``
* Change behavior of ``only_if`` to not check ``is_displayed`` by default.
* Tweaks

 * Allow passing a filename for nose argument ``--holmium-capabilities``
 * Change versioning to use versioneer
 * Explicit py3k support with six
 * Make primitive lists and maps wrapped in pageobjects behave.

v0.6.2
------
Release Date: 2014-01-15

* Bug fix `issue 19 <https://github.com/alisaifee/holmium.core/issues/19>`_

v0.6.1
------
Release Date: 2013-12-23

* Bug fix `issue 18 <https://github.com/alisaifee/holmium.core/issues/18>`_ for facet
  clobbering when page inheritance was involved
* Bug fix
  `issue 17 <https://github.com/alisaifee/holmium.core/commit/issues/17>`_
  for case of no browser specified
* new assertion for TestCase class : ``assertElementAttributeEqual``

v0.6
====
Release Date: 2013-12-14

* Lazy driver initialization. The webdriver is created
  when the test first accesses it.
* Support for using multiple browsers (drivers) in test cases. The original
  self.driver is still available along with a self.drivers list which lazily
  initializes new drivers as they are accessed via index. drivers[0] == driver.
* New environment variable / nose option to force browser(s) to be shutdown and
  restarted between tests. (it is disabled by default, but cookies are still
  always cleared between tests)
* New assertions added to the TestCase base class
* Documentation cleanups
* Bug fixes for default timeout/only_if arugment for Element/Elements/ElementMap

v0.5.2
------
Release Date: 2013-12-09

* PyPy support
* Allow customization of WebElements by exposing `ElementEnhancer`_

v0.5.1
------
Release Date: 2013-12-01

* Re-added python 2.6 support

v0.5.0
------
Release Date: 2013-12-01

* Python 3.3 now supported and tested.

v0.4.2
------
Release Date: 2013-12-01

* New parameter **only_if** (callable that accepts the webelement that was
  found) accepted by Element, Elements, ElementMap that allows for waiting
  for an element to become valid according to the response of **only_if**. The callable will be checked uptil the timeout parameter set
  on the Element.

v0.4.1
------
Release Date: 2013-11-29

* Bug fix for config module being reused between test runs.

v0.4
====
Release Date: 2013-11-28

* Old style class names removed (`Deprecated old class names`_)
* Introduced `Facets`_
* Introduced `Cucumber Features`_ integration with `fresher`_.
* General refactoring and code cleanup.

v0.3.4
------
Release Date: 2013-11-21

* Added support to ignore ssl certificate errors on chrome, firefox & phantomjs
* code cleanup
* improved test coverage


v0.3.3
------
Release Date: 2013-10-29

* Improved back reference access in Config object by allowing variable references
  without requiring a prefix of `default` or the environment name. The resolution
  order is current environment and then default.

  For example, the following config will resolve `login_url` as **http://mysite.com/login**
  and `profile_url` as **http://mysite.com/profile/prod_user** respectively, when `holmium.environment`
  is set to **production**

  .. code-block:: python

    config = { "default" : {
                    "login_url" : "{{url}}/login"
                    , "profile_url":"{{url}}/profiles/{{username}}"}
              , "production": {
                    "url": "http://mysite.com"
                    , "username":"prod_user"}
            }


v0.3.2
------
Release Date: 2013-10-10

* Fluent response from page objects only when page method returns None

v0.3.1
------
Release Date: 2013-09-17

* Allow indexing of Sections objects

v0.3
====
Release Date: 2013-09-16

* Bug Fix for instantiating multiple instances of the same the Page object
  (https://github.com/alisaifee/holmium.core/issues/4)
* `Section object`_ introduced

v0.2
====
Release Date: 2013-09-11

* `Deprecated old class names`_ (PageObject, PageElement, PageElements, PageElementMap & HolmiumTestCase)
* Added more tests for holmium.core.TestCase
* New `Config object`_.

v0.1.8.4
--------
Release Date: 2013-09-04


* Bug Fix : installation via pip was failing due to missing HISTORY.rst file.

v0.1.8.3
--------
Release Date: 2013-08-12


* Bug fix

  - improved error handling and logging for missing/malformed config file.

v0.1.8
------
Release Date: 2013-03-18


* Added iphone/android/phantomjs to supported browsers
* Bug fix

  - fixed phantomjs build in travis


































