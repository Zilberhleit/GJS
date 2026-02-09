# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys

import django

project = "GJS!"
copyright = "2025, Zilberhleyt Mark, Ignatkin Ilya, Pashkin Valeriy, Chetin Grigoriy"
author = "Zilberhleyt Mark, Ignatkin Ilya, Pashkin Valeriy, Chetin Grigoriy"

#  путь к проекту Django
project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../GameJamSite")
)
# sys.path.insert(0, os.path.abspath("/GameJamSite"))
sys.path.insert(0, project_root)
# Настройки для django

os.environ["DJANGO_SETTINGS_MODULE"] = "GameJamSite.settings"
django.setup()

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    # 'sphinxcontrib.django',
    "sphinx_autodoc_typehints",
]


# Автодокументирование
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
}

templates_path = ["_templates"]
exclude_patterns = []

language = "ru"

html_static_path = ["_static"]

# Тема
html_theme = "sphinx_rtd_theme"
