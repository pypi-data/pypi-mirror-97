#!/usr/bin/env python3
# --------------------( LICENSE                           )--------------------
# Copyright (c) 2014-2021 Beartype authors.
# See "LICENSE" for further details.
#
# --------------------( SYNOPSIS                          )--------------------
# Configuration file for the Sphinx documentation builder.
#
# --------------------( SEE ALSO                          )--------------------
# * https://www.sphinx-doc.org/en/master/usage/configuration.html
#   List of all options supported in this file.

# ....................{ TODO                              }....................
#FIXME: Add one or more pytest-based functional tests exercising this
#configuration. This is slightly less trivial than I'd like, largely as the
#Sphinx team has yet to properly document their "sphinx.testing" system. See
#this pending issue for working code examples:
#    https://github.com/sphinx-doc/sphinx/issues/7008
#
#At the least, we probably need to add the following line to our top-level
#"conftest.py" file:
#    pytest_plugins = 'sphinx.testing.fixtures'
#FIXME: Additionally, we should similarly add a single pytest-based functional
#test exercising the correctness of our top-level "README.rst" file -- ideally
#by invoking "checkdocs" somehow if conditionally available.

# ....................{ IMPORTS                           }....................
# Sphinx defaults to hardcoding version specifiers. Since this is insane, we
# import our package-specific version specifier for reuse below. See also:
# * https://protips.readthedocs.io/git-tag-version.html
#   "Inferring Release Number from Git Tags", detailing a clever one-liner
#   harvesting this specifier from the most recent git tag.
from beartype.meta import AUTHORS, COPYRIGHT, NAME, VERSION
from beartype.roar import BeartypeDependencyOptionalMissingWarning
from warnings import warn

# ....................{ IMPORTS ~ kludge                  }....................
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# See also:
# * https://samnicholls.net/2016/06/15/how-to-sphinx-readthedocs
#   The "Make autodoc actually work" is the canonical writeup on this kludge.

#FIXME: Uncomment if actually necessary.
# import os, sys
# sys.path.insert(0, os.path.abspath('..'))

# ....................{ METADATA                          }....................
# Metadata programmatically defined by this package.
project = NAME
author = AUTHORS
copyright = COPYRIGHT
release = VERSION

# ....................{ SETTINGS                          }....................
# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files. This pattern also
# affects html_static_path and html_extra_path.
exclude_patterns = []

# ....................{ EXTENSIONS ~ mandatory            }....................
# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    # ..................{ BUILTIN                           }..................
    # Builtin extensions unconditionally available under *ALL* reasonably
    # modern versions of Sphinx uniquely prefixed by "sphinx.ext.".

    # Builtin extension autogenerating reStructuredText documentation from
    # class, callable, and variable docstrings embedded in Python modules,
    # documenting this project's public (and optionally also private) API.
    'sphinx.ext.autodoc',

    # Builtin extension autogenerating reStructuredText documentation from
    # class, callable, and variable docstrings embedded in Python modules
    # formatted according to either NumPy or Google style.
    #
    # Note this effectively requires 'sphinx.ext.autodoc' to be listed as well.
    'sphinx.ext.napoleon',

    # Builtin extension rendering "math::" directives into HTML-only JavaScript
    # via the third-party MathJax library.
    'sphinx.ext.mathjax',

    # Builtin extension autogenerating reStructuredText documentation listing
    # each of this project's Python modules and linking external references to
    # those modules to these listings.
    'sphinx.ext.viewcode',

    # ..................{ THIRD-PARTY                       }..................
    # Third-party Sphinx extensions required to be externally installed. For
    # usability, this block should typically be empty. Third-party Sphinx
    # extensions should ideally be optionally enabled. See below.
]

# ....................{ EXTENSIONS ~ optional             }....................
# Third-party Sphinx extensions conditionally used if externally installed.

# Attempt to optionally...
try:
    # Import "sphinx_rtd_theme", a third-party Sphinx extension providing the
    # official Read The Docs (RTD) HTML theme. This theme is preferable where
    # available for improved mobile-friendly rendering.
    import sphinx_rtd_theme

    # Register the fully-qualified name of this extension.
    extensions.append('sphinx_rtd_theme')

    # Set the HTML theme to this theme.
    html_theme = 'sphinx_rtd_theme'
# If this theme extension is unavailable, fallback to the default HTML theme...
except ImportError:
    # Emit a non-fatal warning to warn callers of the performance
    # pitfalls associated with memoizing keyword arguments.
    warn(
        (
            'Optional Sphinx extension "sphinx_rtd_theme" unimportable; '
            'falling back to default Sphinx HTML theme.'
        ),
        BeartypeDependencyOptionalMissingWarning
    )

# ....................{ EXTENSIONS ~ conf : napoleon      }....................
# 'sphinx.ext.napoleon'-specific settings. See also:
# * https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html
#   Official documentation.

# Prevent Napoleon from attempting to erroneously parse docstrings in the
# Google format unused by this project.
napoleon_google_docstring = False

#FIXME: Experiment with enabling these non-default settings as well.
# napoleon_use_param = False
# napoleon_use_ivar = True

# ....................{ BUILD ~ html                      }....................
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# ....................{ BUILD ~ html : mathjax            }....................
# Remote URI to the top-level "MathJax.js" script providing MathJax. If
# unspecified, the current user *MUST* have MathJax locally installed. Note
# that MathJax is locally installable under:
# * Debian systems with:
#   $ sudo apt install libjs-mathjax
#
# See also:
# * https://docs.mathjax.org/en/v2.7-latest/start.html
#   List of all third-party Content Delivery Networks (CDNs) officially hosting
#   MathJax assets.
mathjax_path="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML"
