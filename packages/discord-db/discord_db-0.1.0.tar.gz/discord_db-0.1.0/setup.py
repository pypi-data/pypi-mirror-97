# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['discord_db']
setup_kwargs = {
    'name': 'discord-db',
    'version': '0.1.0',
    'description': 'Helpfull db writen on sqlite3, already has channel vars, global user vars, server user vars and server vars',
    'long_description': None,
    'author': 'EditedCocktail',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
