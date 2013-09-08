Holmium Classes
===============

Page Objects
-------------
.. automodule:: holmium.core 
    :members:

.. autoclass:: Page
.. autoclass:: Element
.. autoclass:: Elements 
.. autoclass:: ElementMap
.. autoclass:: Locators
    :undoc-members:
    :inherited-members:

Deprecated Classes 
------------------
Earlier versions of :mod:`holmium.core` used rather verbose names for Page objects and elements. 
As of version 0.2 the classes have been renamed but the older names have been retained as aliases 
to the new classes for backward compatibility (an annoying warning will however, be emitted everytime 
the old names are used to hopefully convince test authors to update their test code :D ).

.. autoclass:: PageObject
.. autoclass:: PageElement
.. autoclass:: PageElements 
.. autoclass:: PageElementMap
.. autoclass:: HolmiumTestCase 

Utilities
---------
.. autoclass:: TestCase
.. autofunction:: repeat 
