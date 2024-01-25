# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "basis"
copyright = "2023, Wavelet"
author = "Wavelet"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["myst_parser"]
extensions.append("autoapi.extension")
autoapi_dirs = ["../../src"]

templates_path = ["_templates"]
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]


scm_contribs_email = "true"  # Show email. Default: "true"
scm_contribs_limit_contributors = None  # Limit number of contributors. Use None
# to deactivate. Default: None
scm_contribs_min_commits = 1  # Filter by number of commits. Default: 0
scm_contribs_sort = "num"  # Sort by name or number of commits.
# Default: "name"
scm_contribs_type = "committer"  # Show info of author or committer.
# Default: "author"
