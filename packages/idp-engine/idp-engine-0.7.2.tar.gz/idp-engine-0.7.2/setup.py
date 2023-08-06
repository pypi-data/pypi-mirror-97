# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['idp_engine']

package_data = \
{'': ['*']}

install_requires = \
['Click>=7.0,<8.0',
 'pretty-errors>=1.2.19,<2.0.0',
 'sphinxcontrib-mermaid==0.6.3',
 'textX>=2.1.0,<3.0.0',
 'z3-solver==4.8.8.0']

entry_points = \
{'console_scripts': ['idp-engine = idp_engine.IDP_Z3:cli']}

setup_kwargs = {
    'name': 'idp-engine',
    'version': '0.7.2',
    'description': 'IDP-Z3 is a collection of software components implementing the Knowledge Base paradigm using the FO(.) language and a Z3 SMT solver.',
    'long_description': 'The IDP-Z3 tools implement a knowledge base system combining the Microsoft Z3 solver and a grounder developed in-house, supporting the IDP language.  See the presentation at [www.IDP-Z3.be](https://www.IDP-Z3.be).\n\nIt is developed by the Knowledge Representation group at KU Leuven in Leuven, Belgium, and made available under the [GNU LGPL v3 License](https://www.gnu.org/licenses/lgpl-3.0.txt).\n\n\n# Installation\n\n* Install [python3](https://www.python.org/downloads/) on your machine.\n* Install [poetry](https://python-poetry.org/docs/#installation):\n    * after that, logout and login if requested, to update `$PATH`\n* Use git to clone https://gitlab.com/krr/IDP-Z3 to a directory on your machine\n* Open a terminal in that directory\n* If you have several versions of python3, and want to run on a particular one, e.g., 3.9:\n    * run `poetry env use 3.9`\n    * replace `python3` by `python3.9` in every command below\n* Run `poetry install`\n\n\n# Get started\n\nTo launch the Interactive Consultant web server:\n\n* open a terminal in that directory and run `poetry run python3 main.py`\n* open your browser at http://127.0.0.1:5000\n\n\n# Develop\n\nYou may want to read about the [technical documentation](http://docs.idp-z3.be/en/latest/code_reference.html) and the [Development and deployment guide](https://gitlab.com/krr/IDP-Z3/-/wikis/Development-and-deployment-guide).\n\nThe user manual is in the `/docs` folder and can be locally generated as follows:\n~~~~\npoetry run sphinx-autobuild docs docs/_build/html\n~~~~\nTo view it, open `http://127.0.0.1:8000`\n\nThe [documentation](https://docs.IDP-Z3.be) on [readthedocs](https://readthedocs.org/projects/idp-z3/) is automatically updated from the main branch of the GitLab repository.\n\nThe [home page](https://www.IDP-Z3.be) is in the `/homepage` folder and can be locally generated as follows:\n~~~~\npoetry run sphinx-autobuild homepage homepage/_build/html\n~~~~\nTo view it, open `http://127.0.0.1:8000`.  The website is also automatically updated from the main branch of the GitLab repository.\n\n\n# Testing\n\nTo generate the tests, from the top directory run `poetry run python3 test.py` or `poetry run python3 test.py generate`.\nAfter this, you can manually check what has changed using git.\n\nThere is also a testing pipeline available, which can be used by running `poetry run python3 test.py pipeline`.\n\n\n# Deploy\n\nSee the instructions [here](https://gitlab.com/krr/IDP-Z3/-/wikis/Development-and-deployment-guide).\n',
    'author': 'pierre.carbonnelle',
    'author_email': 'pierre.carbonnelle@cs.kuleuven.be',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.idp-z3.be',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
