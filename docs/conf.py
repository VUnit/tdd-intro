# -*- coding: utf-8 -*-

import os
import sys
from pathlib import Path

# -- Sphinx Options -----------------------------------------------------------

# If your project needs a minimal Sphinx version, state it here.
needs_sphinx = "3.0"

extensions = [
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinxarg.ext",  # Automatic argparse command line argument documentation
]

# The suffix(es) of source filenames.
source_suffix = {
    ".rst": "restructuredtext"
}

master_doc = "index"

project = u"Introduction to TDD and CI With VUnit"
copyright = u"2014-2021, Lars Asplund"
author = u"LarsAsplund and contributors"

version = ""
release = ""

language = None

exclude_patterns = []

pygments_style = "sphinx"

todo_include_todos = False

# -- Options for HTML output ----------------------------------------------

html_theme_path = ["."]
html_theme = "_theme"

html_theme_options = {
    "analytics_id": "UA-abcdefghi-j",
    "logo_only": True,
    "vcs_pageview_mode": "blob",
    "style_nav_header_background": "#0c479d",
    "home_breadcrumbs": False,
}
html_context = {
    "conf_py_path": "%s/" % Path(__file__).parent.name,
    "display_github": True,
    "github_user": "VUnit",
    "github_repo": "vunit",
    "github_version": "master/",
}

html_static_path = ["_static"]

html_logo = str(Path(html_static_path[0]) / "VUnit_logo_175x175.png")

html_favicon = str(Path(html_static_path[0]) / "vunit.ico")

# Output file base name for HTML help builder.
htmlhelp_basename = "VUnitDoc"

# -- InterSphinx ----------------------------------------------------------

intersphinx_mapping = {
    "ghdl": ("https://ghdl.github.io/ghdl", None),
    "python": ("https://docs.python.org/3.8/", None),
    "vunit": ("https://vunit.github.io", None),
}

# -- ExtLinks -------------------------------------------------------------

extlinks = {
    "vunit_example": ("https://github.com/VUnit/vunit/tree/master/examples/%s/", ""),
    "vunit_file": ("https://github.com/VUnit/vunit/tree/master/%s/", ""),
    "vunit_commit": ("https://github.com/vunit/vunit/tree/%s/", "@"),
    "vunit_issue": ("https://github.com/VUnit/vunit/issues/%s/", "#"),
}
