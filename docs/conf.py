# -*- coding: utf-8 -*-

import os
import sys
from json import loads
from pathlib import Path
from shutil import copyfile

ROOT = Path(__file__).resolve().parent

TUTORIAL = ROOT / "tutorial"

if not TUTORIAL.exists():
    TUTORIAL.mkdir(exist_ok=True)

for idx in range(1,8):
    instructions = ROOT.parent / "tutorial/exercise_0{}/instructions.rst".format(idx)
    if instructions.exists():
        copyfile(instructions, TUTORIAL / "ex0{}.rst".format(idx))

# -- Sphinx Options -----------------------------------------------------------

# If your project needs a minimal Sphinx version, state it here.
needs_sphinx = "3.0"

extensions = [
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo"
]

# The suffix(es) of source filenames.
source_suffix = {
    ".rst": "restructuredtext"
}

master_doc = "index"

project = u"VUnit: Introduction to TDD and CI"
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

html_context = {}
ctx = Path(__file__).resolve().parent / 'context.json'
if ctx.is_file():
    html_context.update(loads(ctx.open('r').read()))


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
    "vunit_commit": ("https://github.com/VUnit/vunit/tree/%s/", "@"),
    "vunit_issue": ("https://github.com/VUnit/vunit/issues/%s/", "#"),
    "tdd_file": ("https://github.com/VUnit/tdd-intro/tree/master/%s/", ""),
    "tdd_commit": ("https://github.com/VUnit/tdd-intro/tree/%s/", "@"),
    "tdd_issue": ("https://github.com/VUnit/tdd-intro/issues/%s/", "#"),
}
