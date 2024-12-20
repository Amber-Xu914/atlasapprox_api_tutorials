# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Explore Average Expression'
copyright = '2024, Amber Xu'
author = 'Amber Xu'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",          # Enables MyST Markdown support
    "jupyter_sphinx",
    "sphinx_codeautolink"    # Adds support for automatic code output linking
]

# Configuration for MyST parser
myst_enable_extensions = [
    "colon_fence",  # Enables ::: fences for directives
    "deflist",      # Enables definition lists
]

# Configuration for executing code
execute_code_executors = {
    "python": "python3",      # Define Python 3 as the executor
}

nbsphinx_execute = 'auto'  # Executes only if no output is present in the notebook

# Configuration for sphinx-codeautolink
codeautolink_autolink = True  # Automatically links and shows output for code examples

templates_path = ['_templates']
exclude_patterns = ['**.ipynb_checkpoints']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
