# -*- coding: utf-8 -*-
#

import sys, os
sys.path.insert(0, os.path.abspath('../../'))
import holmium.core

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

if not on_rtd:  # only import and set the theme if we're building docs locally
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

extensions = [
    'sphinx.ext.autodoc', 'sphinx.ext.autosummary',
    'sphinx.ext.doctest', 'sphinx.ext.intersphinx', 'sphinx.ext.todo',
    'sphinx.ext.ifconfig', 'sphinx.ext.viewcode',
]

html_theme_options = {
    'logo_only': True,
}


templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'holmium.core'
copyright = u'2014, Ali-Akber Saifee'
version = release = holmium.core.__version__

exclude_patterns = []
pygments_style = 'sphinx'
html_title = "holmium"
html_static_path = ['_static']
htmlhelp_basename = 'holmiumcoredoc'
html_logo = 'holmium-logo.png'

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
intersphinx_mapping = {
    'http://docs.python.org/': None,
    "http://selenium-python.readthedocs.org/":None,
    "http://jinja.pocoo.org/docs/" : None
}
