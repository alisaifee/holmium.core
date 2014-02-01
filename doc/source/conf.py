# -*- coding: utf-8 -*-
#

import sys, os
sys.path.insert(0, os.path.abspath('../../'))
import holmium.core

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.autosummary','sphinx.ext.doctest', 'sphinx.ext.intersphinx', 'sphinx.ext.todo', 'sphinx.ext.pngmath', 'sphinx.ext.ifconfig', 'sphinx.ext.viewcode', 'sphinxcontrib.email']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'holmium.core'
copyright = u'2014, Ali-Akber Saifee'
version = release = holmium.core.__version__

exclude_patterns = []
#add_module_names = True
pygments_style = 'sphinx'
#html_theme_options = {}
#html_theme_path = []
html_title = "holmium"
#html_favicon = None
html_static_path = ['_static']
htmlhelp_basename = 'holmiumcoredoc'

latex_documents = [
  ('index', 'holmiumcore.tex', u'holmium.core Documentation',
   u'Ali-Akber Saifee', 'manual'),
]
man_pages = [
    ('index', 'holmiumcore', u'holmium.core Documentation',
     [u'Ali-Akber Saifee'], 1)
]

texinfo_documents = [
  ('index', 'holmiumcore', u'holmium.core Documentation',
   u'Ali-Akber Saifee', 'holmiumcore', 'One line description of project.',
   'Miscellaneous'),
]
intersphinx_mapping = {'http://docs.python.org/': None, "http://selenium-python.readthedocs.org/en/latest":None, "http://jinja.pocoo.org/docs/" : None}
