*************************
Holmium API documentation
*************************

Public classes 
==============

Page Objects & Friends
----------------------
.. currentmodule:: holmium.core 

.. autoclass:: Page
.. autoclass:: Section
.. autoclass:: Sections
.. autoclass:: Element
.. autoclass:: Elements 
.. autoclass:: ElementMap
.. autoclass:: Locators
    :undoc-members:
    :inherited-members:


Deprecated Classes 
------------------
.. deprecated:: 0.3

.. warning::
  
  Earlier versions of :mod:`holmium.core` used rather verbose names for Page objects and elements. 
  They have been removed as of version 0.4 and accessing them will raise a :exc:`exceptions.SyntaxError`.

.. autoclass:: PageObject
.. autoclass:: PageElement
.. autoclass:: PageElements 
.. autoclass:: PageElementMap
.. autoclass:: HolmiumTestCase 

Utilities
---------
.. autoclass:: TestCase
    :members:
.. autoclass:: Config
    :members:
.. autoclass:: ElementEnhancer
    :members:
.. autofunction:: register_enhancer
.. autofunction:: reset_enhancers


Internal Classes
================ 

Page Object Helpers
-------------------
.. currentmodule:: holmium.core.pageobject 

.. autoclass:: ElementDict
    :members:

.. autoclass:: ElementList
    :members:

.. autoclass:: ElementGetter
    :members:

.. currentmodule:: holmium.core.facets

.. autoclass:: FacetCollection
    :members:
.. autoclass:: Facet
    :members:
.. autoclass:: Faceted
    :members:
.. autoexception:: FacetError

.. currentmodule:: holmium.core.conditions

.. autoclass:: BaseCondition
    :members:




Test configuration / execution
------------------------------
.. currentmodule:: holmium.core 

.. autoclass:: HolmiumNose
    :members:
.. currentmodule:: holmium.core.config 
.. autoclass:: HolmiumConfig
    :members:



