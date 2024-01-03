import os
import sys

sys.path.insert(0, os.path.abspath("../.."))

project = "envanter"
copyright = "2023, şuayip üzülmez"
author = "şuayip üzülmez"
release = "v1.2.1"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx_rtd_theme",
]
templates_path = ["_templates"]
exclude_patterns = []
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
