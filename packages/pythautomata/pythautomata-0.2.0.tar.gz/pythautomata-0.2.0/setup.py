# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pythautomata',
 'pythautomata.abstract',
 'pythautomata.automata',
 'pythautomata.automata.wheighted_automaton_definition',
 'pythautomata.automata_definitions',
 'pythautomata.base_types',
 'pythautomata.exceptions',
 'pythautomata.model_comparators',
 'pythautomata.model_exporters',
 'pythautomata.tests',
 'pythautomata.utilities']

package_data = \
{'': ['*']}

install_requires = \
['graphviz', 'numpy']

setup_kwargs = {
    'name': 'pythautomata',
    'version': '0.2.0',
    'description': "ORT's implementation of various kinds of automata",
    'long_description': None,
    'author': 'Federico Vilensky',
    'author_email': 'fedevilensky@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
