import os
import sys

sys.path.insert(0, os.path.abspath('../backend'))

project = 'NatJobs'

copyright = '2026, NatJobs Team'

author = 'NatJobs Team'

release = '1.0.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.coverage',
]

templates_path = ['_templates']

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'

html_static_path = ['_static']
