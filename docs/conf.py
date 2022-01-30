"""Sphinx configuration."""
# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))
import narrow_down  # noqa: E402

# -- Project information -----------------------------------------------------

# General information about the project.
project = "narrow-down"
copyright = "2022, Christian Krudewig"  # noqa: A001
author = "Christian Krudewig"
# The version info for the project you're documenting, acts as replacement
# for |version| and |release|, also used in various other places throughout
# the built documents.
#
# The short X.Y version.
version = narrow_down.__version__
# The full version, including alpha/beta/rc tags.
release = narrow_down.__version__

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    # "sphinx.ext.autosummary",
    "sphinx.ext.autodoc",
    # "sphinx.ext.doctest",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "myst_parser",
]

autodoc_mock_imports = ["cassandra"]

autodoc_default_options = {
    "undoc-members": True,
    "special-members": "",
}
autoclass_content = "both"
autodoc_class_signature = "mixed"
autodoc_typehints = "description"
autodoc_inherit_docstrings = True


# Napoleon docstring parser settings
napoleon_include_init_with_doc = True


# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "apidoc/narrow_down.rst",
    "apidoc/narrow_down.proto.rst",
    "apidoc/narrow_down.proto.stored_document_pb2.rst",
]


# -- Options for HTML output -------------------------------------------------

# # The theme to use for HTML and HTML Help pages.  See the documentation for
# # a list of builtin themes.
# #
# html_theme = "alabaster"
#
# # Theme options are theme-specific and customize the look and feel of a theme
# # further.  For a list of options available for each theme, see the
# # documentation.
# html_theme_options = {
#     "github_user": "chr1st1ank",
#     "github_repo": "narrow-down",
#     "github_banner": True,
#     "show_related": False,
#     "fixed_sidebar": True,
#     "page_width": "1024px",
# }

html_theme = "furo"
html_theme_options = {}


# html_theme = "nature"
#
# # Theme options are theme-specific and customize the look and feel of a theme
# # further.  For a list of options available for each theme, see the
# # documentation.
# html_theme_options = {
#     "rightsidebar": False,
# }

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
