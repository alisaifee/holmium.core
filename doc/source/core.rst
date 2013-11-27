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
Earlier versions of :mod:`holmium.core` used rather verbose names for Page objects and elements. 
As of version 0.4 they have been removed and accessing them will raise a :exc:`SyntaxError`.

.. autoclass:: PageObject
.. autoclass:: PageElement
.. autoclass:: PageElements 
.. autoclass:: PageElementMap
.. autoclass:: HolmiumTestCase 

Utilities
=========
.. autoclass:: TestCase
.. autofunction:: repeat 
