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



