# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
# pylint: skip-file
import os
import sys

sys.path.insert(0, os.path.abspath("../.."))
# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "aymara-ai"
copyright = "2024, Aymara"
author = "Aymara"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "myst_nb",
    "sphinxcontrib.googleanalytics",
]

googleanalytics_id = "G-VYYZ5093ZM"

nb_execution_mode = "off"
pygments_style = "sphinx"


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_book_theme"
html_theme_options = {
    "home_page_in_toc": True,
    "path_to_docs": "docs",
    "navigation_with_keys": False,
    "logo": {
        "image_light": "_static/logo-wide-black.png",
        "image_dark": "_static/logo-wide-white.png",
    },
}
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_favicon = "_static/favicon-light.png"
html_js_files = ["favicon-switcher.js"]

source_suffix = [".rst", ".md", ".ipynb"]


def setup(app):
    app.connect("include-read", on_include_read)


def on_include_read(app, path, docname, source):
    new_source = []
    in_sphinx_ignore = False
    for line in source[0].splitlines():
        if "<!-- sphinx-ignore-start -->" in line:
            in_sphinx_ignore = True
        elif "<!-- sphinx-ignore-end -->" in line:
            in_sphinx_ignore = False
        elif not in_sphinx_ignore:
            new_source.append(line)
    source[0] = "\n".join(new_source)
