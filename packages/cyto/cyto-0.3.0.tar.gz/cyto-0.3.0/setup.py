# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cyto',
 'cyto._extra',
 'cyto.app',
 'cyto.basic',
 'cyto.settings',
 'cyto.settings.sources',
 'cyto.settings.sources.cli',
 'cyto.settings.sources.glob']

package_data = \
{'': ['*']}

extras_require = \
{'all': ['anyio>=2.0.2,<3.0.0',
         'click>=7.1.2,<8.0.0',
         'pydantic>=1.8.1,<2.0.0',
         'toml>=0.10.2,<0.11.0'],
 'app': ['anyio>=2.0.2,<3.0.0', 'pydantic>=1.8.1,<2.0.0'],
 'settings': ['pydantic>=1.8.1,<2.0.0'],
 'settings.sources.cli': ['click>=7.1.2,<8.0.0'],
 'settings.sources.toml': ['toml>=0.10.2,<0.11.0']}

setup_kwargs = {
    'name': 'cyto',
    'version': '0.3.0',
    'description': "SBT Instruments' framework for Python-based applications",
    'long_description': '# Cyto 🦠\n\nThis is a work-in-progress replacement for `geist`.\n\n## Development\n\n### Python Version\n\nDevelopment requires Python 3.8 or later. Test your python version with:\n```shell\npython3 --version\n```\n\nIf you have multiple python installations, you can replace `python3`\nwith a specific version (e.g., `python3.8`) in the steps below.\n\n### Getting Started\n\nDo the following:\n\n 1. Clone this repository\n    ```shell\n    git clone git@github.com:sbtinstruments/cyto.git\n    ```\n 2. Install poetry (for dependency management)\n    ```shell\n    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3\n    ```\n 3. Optional: Use a local poetry virtual environment\n    ```shell\n    poetry config --local virtualenvs.in-project true\n    ```\n    This integrates better with editors such as Visual Studio Code.\n 4. Create poetry\'s virtual environment and get all dependencies\n and all extra features.\n    ```shell\n    poetry install --extras all\n    ```\n 5. Optional: Run the QA basic tools (e.g., isort, black, pylint, mypy) automatically before each commit\n    ```shell\n    poetry run pre-commit install\n    ```\n\n### Quality Assurance (QA) Tools\n\n#### QA Basic Tools\n\n*All QA basic tools automatically run in Jenkins for each commit pushed\nto the remote repository. If you installed the `pre-commit` hooks,\nall QA basic tools automatically run before each commit too.*\n\nThe QA basic tools are:\n * `isort` (for import ordering)\n * `black` (for formatting)\n * `pylint` (for linting)\n * `mypy` (for type checking)\n\nYou can run the QA basic tools manually. This is useful if you\ndon\'t want to install the `pre-commit` hooks.\n\nRun the QA basic tools manually with:\n```shell\npoetry run task isort\npoetry run task black\npoetry run task pylint\npoetry run task mypy\n```\n\nRun all the basic QA tools manually with a single command:\n\n```shell\npoetry run task pre-commit\n```\n\nNote that this doesn\'t require you to install the `pre-commit` hooks.\n\n#### QA Test Tools\n\n*All of the tools below automatically run in Jenkins for each\ncommit pushed to the remote repository.*\n\nThe QA test tools are:\n * `tox` (for automation across Python versions)\n * `pytest` (the test framework itself)\n * `pytest-cov` (for test coverage percentage)\n\nRun the tests manually:\n\n 1. Install `tox`\n    ```shell\n    python3 -m pip install tox\n    ```\n 2. Start a tox run:\n    ```\n    tox\n    ```\n\nNote that `tox` invokes `pytest` in a set of virtual environments. Said\nvirtual environments have nothing to do with poetry\'s virtual environment. Poetry and tox runs in isolation of each other.\n\n### Visual Studio Code\n\n#### Settings\n\nWe have a default settings file that you can use via the following command:\n```shell\ncp .vscode/settings.json.default .vscode/settings.json\n```\nThis is optional.\n\n#### Python Interpreter\n\nHopefully, you used the local poetry virtual environment during\ninstallation (the `poetry config --local virtualenvs.in-project true` part). This way, Visual Studio Code automatically finds the\nPython interpreter within poetry\'s virtual environment.\n\nAlternatively, you can point Visual Studio Code to poetry\'s\nglobal virtual environments folder. Add the following entry\nto your `./vscode/settings.json` file:\n```json\n{ "python.venvPath": "~/.cache/pypoetry/virtualenvs" }\n```\n\nThen, you look for the poetry\'s currently active virtual environment:\n```shell\npoetry env list\n```\n\nLastly, you use the Visual Studio Code command\n`Python: Select Interpreter` and choose the interpreter inside\npoetry\'s currently active virtual environment.',
    'author': 'Frederik Peter Aalund',
    'author_email': 'fpa@sbtinstruments.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sbtinstruments/cyto',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
