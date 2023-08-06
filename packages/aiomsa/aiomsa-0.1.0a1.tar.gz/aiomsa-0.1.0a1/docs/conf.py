# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import json

import aiohttp.web
import yaml
from aiohttp_swagger import generate_doc_from_each_end_point

from aiomsa.server import routes


# -- Module Remapping --------------------------------------------------------

aiohttp.web.Application.__module__ = "aiohttp.web"


# -- Project information -----------------------------------------------------

project = "aiomsa"
copyright = "2021, Facebook Connectivity"
author = "Facebook Connectivity"

# The full version, including alpha/beta/rc tags
release = "0.1.0a1"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "sphinxcontrib.openapi",
]

# Add any paths that contain templates here, relative to this directory.
# templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# A list of (type, target) tuples (by default empty) that should be ignored
# when generating warnings in “nitpicky mode”
nitpick_ignore = [("http:obj", "string")]  # sphinxcontrib.openapi


# -- intersphinx configuration -----------------------------------------------

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "aiohttp": ("https://docs.aiohttp.org/en/stable/", None),
}


# -- autodoc configuration ---------------------------------------------------

autodoc_member_order = "bysource"


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "furo"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ["_static"]


def setup(app):
    web_app = aiohttp.web.Application()
    web_app.add_routes(routes)
    with open("openapi.yml", "w+") as f:
        docs = json.loads(generate_doc_from_each_end_point(web_app, ui_version=3))
        yaml.dump(docs, f)

    return app
