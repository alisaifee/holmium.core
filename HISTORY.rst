.. :changelog:
.. _Deprecated old class names: http://holmiumcore.readthedocs.org/en/latest/core.html#deprecated-classes 
.. _Config object: http://holmiumcore.readthedocs.org/en/latest/internals.html#holmium.core.Config
.. _Section object: https://holmiumcore.readthedocs.org/en/latest/usage.html#sections 
.. _Facets: http://holmiumcore.readthedocs.org/en/latest/usage.html#page-facets 
.. _Cucumber Features: http://holmiumcore.readthedocs.org/en/latest/cucumber.html 
.. _fresher: https://github.com/lddubeau/fresher 
.. _ElementEnhancer: http://holmiumcore.readthedocs.org/en/latest/usage.html#customizing-page-elements

*******
History
*******

0.6 2013-12-14
==============
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

0.5.2 2013-12-09
================
* PyPy support 
* Allow customization of WebElements by exposing `ElementEnhancer`_

0.5.1 2013-12-01
================
* Re-added python 2.6 support 

0.5.0 2013-12-01
================
* Python 3.3 now supported and tested.

0.4.2 2013-12-01
================
* New parameter **only_if** (callable that accepts the webelement that was
  found) accepted by Element, Elements, ElementMap that allows for waiting 
  for an element to become valid according to the response of **only_if**. The callable will be checked uptil the timeout parameter set 
  on the Element.

0.4.1 2013-11-29
================
* Bug fix for config module being reused between test runs. 

0.4 2013-11-28
==============
* Old style class names removed (`Deprecated old class names`_)
* Introduced `Facets`_
* Introduced `Cucumber Features`_ integration with `fresher`_.
* General refactoring and code cleanup.

0.3.4 2013-11-21
================
* Added support to ignore ssl certificate errors on chrome, firefox & phantomjs 
* code cleanup
* improved test coverage 


0.3.3 2013-10-29
================
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


0.3.2 2013-10-10
================
* Fluent response from page objects only when page method returns None

0.3.1 2013-09-17
================
* Allow indexing of Sections objects 

0.3 2013-09-16
==============
* Bug Fix for instantiating multiple instances of the same the Page object
  (https://github.com/alisaifee/holmium.core/issues/4)
* `Section object`_ introduced 

0.2 2013-09-11
==============
* `Deprecated old class names`_ (PageObject, PageElement, PageElements, PageElementMap & HolmiumTestCase) 
* Added more tests for holmium.core.TestCase 
* New `Config object`_. 

0.1.8.4 2013-09-04
==================

* Bug Fix : installation via pip was failing due to missing HISTORY.rst file.

0.1.8.3 2013-08-12
==================

* Bug fix 

  - improved error handling and logging for missing/malformed config file.

0.1.8 2013-03-18
================ 

* Added iphone/android/phantomjs to supported browsers 
* Bug fix 
  
  - fixed phantomjs build in travis

















