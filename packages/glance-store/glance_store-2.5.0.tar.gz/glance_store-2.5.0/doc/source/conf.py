# Copyright 2010-2011 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import os
import sys

sys.path.insert(0, os.path.abspath('../..'))
# -- General configuration ----------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = ['openstackdocstheme',
              'sphinxcontrib.apidoc']

# openstackdocstheme options
openstackdocs_repo_name = 'openstack/glance_store'
openstackdocs_auto_name = False
openstackdocs_bug_project = 'glance-store'
openstackdocs_bug_tag = ''

# sphinxcontrib.apidoc options
apidoc_module_dir = '../../glance_store'
apidoc_output_dir = 'reference/api'
apidoc_excluded_paths = [
    'test',
    'tests/*']
apidoc_separate_modules = True

# autodoc generation is a bit aggressive and a nuisance when doing heavy
# text edit cycles.
# execute "export SPHINX_DEBUG=1" in your terminal to disable

# Add any paths that contain templates here, relative to this directory.
# templates_path = []

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'glance_store'
copyright = u'2014, OpenStack Foundation'

# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = True

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'native'

# -- Options for HTML output --------------------------------------------------

# The theme to use for HTML and HTML Help pages.  Major themes that come with
# Sphinx are currently 'default' and 'sphinxdoc'.
# html_theme_path = ["."]
# html_theme = '_theme'
# html_static_path = ['static']
html_theme = 'openstackdocs'

# Output file base name for HTML help builder.
htmlhelp_basename = '%sdoc' % project

modindex_common_prefix = ['glance_store.']

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass
# [howto/manual]).
latex_documents = [
    ('index',
     '%s.tex' % project,
     '%s Documentation' % project,
     'OpenStack Foundation', 'manual'),
]

# The autodoc module imports every module to check for import
# errors. Since the fs_mount module is self initializing, it
# requires configurations that aren't loaded till that time.
# It would never happen in a real scenario as it is only imported
# from cinder store after the config are loaded but to handle doc
# failures, we mock it here.
autodoc_mock_imports = ['glance_store.common.fs_mount']