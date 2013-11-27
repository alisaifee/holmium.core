***************
Holmium Classes
***************

Page Objects & Friends
======================
.. automodule:: holmium.core 
    :members:

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
==================
.. deprecated:: 0.3

.. warning::
  
  Earlier versions of :mod:`holmium.core` used rather verbose names for Page objects and elements. 
  They have been removed and accessing them will raise a :exc:`exceptions.SyntaxError`.

.. autoclass:: PageObject
.. autoclass:: PageElement
.. autoclass:: PageElements 
.. autoclass:: PageElementMap
.. autoclass:: HolmiumTestCase 

Utilities
=========
.. autoclass:: TestCase
