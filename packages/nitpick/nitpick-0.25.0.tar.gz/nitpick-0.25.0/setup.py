# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nitpick', 'nitpick.plugins']

package_data = \
{'': ['*']}

install_requires = \
['ConfigUpdater',
 'attrs',
 'autorepr',
 'click',
 'dictdiffer',
 'flake8>=3.0.0',
 'identify',
 'jmespath',
 'loguru',
 'marshmallow-polyfield>=5.10,<6.0',
 'marshmallow>=3.0.0b10',
 'more-itertools',
 'pluggy',
 'pydantic',
 'python-slugify',
 'requests',
 'ruamel.yaml',
 'sortedcontainers',
 'toml',
 'tomlkit']

extras_require = \
{'doc': ['sphinx', 'sphinx_rtd_theme', 'sphobjinv'],
 'lint': ['pylint'],
 'test': ['pytest', 'pytest-cov', 'testfixtures', 'responses']}

entry_points = \
{'console_scripts': ['nitpick = nitpick.cli:nitpick_cli'],
 'flake8.extension': ['NIP = nitpick.flake8:NitpickFlake8Extension'],
 'nitpick': ['ini = nitpick.plugins.ini',
             'json = nitpick.plugins.json',
             'pre_commit = nitpick.plugins.pre_commit',
             'pyproject_toml = nitpick.plugins.pyproject_toml',
             'text = nitpick.plugins.text']}

setup_kwargs = {
    'name': 'nitpick',
    'version': '0.25.0',
    'description': 'Enforce the same configuration across multiple projects',
    'long_description': '# Nitpick\n\n[![PyPI](https://img.shields.io/pypi/v/nitpick.svg)](https://pypi.org/project/nitpick)\n![GitHub Actions Python Workflow](https://github.com/andreoliwa/nitpick/workflows/Python/badge.svg)\n[![Documentation Status](https://readthedocs.org/projects/nitpick/badge/?version=latest)](https://nitpick.rtfd.io/en/latest/?badge=latest)\n[![Coveralls](https://coveralls.io/repos/github/andreoliwa/nitpick/badge.svg)](https://coveralls.io/github/andreoliwa/nitpick)\n[![Maintainability](https://api.codeclimate.com/v1/badges/61e0cdc48e24e76a0460/maintainability)](https://codeclimate.com/github/andreoliwa/nitpick)\n[![Test Coverage](https://api.codeclimate.com/v1/badges/61e0cdc48e24e76a0460/test_coverage)](https://codeclimate.com/github/andreoliwa/nitpick)\n[![Supported Python versions](https://img.shields.io/pypi/pyversions/nitpick.svg)](https://pypi.org/project/nitpick/)\n[![Project License](https://img.shields.io/pypi/l/nitpick.svg)](https://pypi.org/project/nitpick/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Dependabot Status](https://api.dependabot.com/badges/status?host=github&repo=andreoliwa/nitpick)](https://dependabot.com)\n[![semantic-release](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg)](https://github.com/semantic-release/semantic-release)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/andreoliwa/nitpick/develop.svg)](https://results.pre-commit.ci/latest/github/andreoliwa/nitpick/develop)\n\nFlake8 plugin to enforce the same tool configuration ([flake8](https://gitlab.com/pycqa/flake8), [isort](https://github.com/PyCQA/isort), [mypy](http://mypy-lang.org/), [Pylint](https://www.pylint.org)...) across multiple Python projects.\n\nUseful if you maintain multiple projects and want to use the same configs in all of them.\n\n## Style file\n\nA "nitpick code style" is a [TOML](https://github.com/toml-lang/toml) file with the settings that should be present in config files from other tools.\n\nExample of a style:\n\n```\n["pyproject.toml".tool.black]\nline-length = 120\n\n["pyproject.toml".tool.poetry.dev-dependencies]\npylint = "*"\n\n["setup.cfg".flake8]\nignore = "D107,D202,D203,D401"\nmax-line-length = 120\ninline-quotes = "double"\n\n["setup.cfg".isort]\nline_length = 120\nmulti_line_output = 3\ninclude_trailing_comma = true\nforce_grid_wrap = 0\ncombine_as_imports = true\n```\n\nThis style will assert that:\n\n- ... [black](https://github.com/psf/black), [isort](https://github.com/PyCQA/isort) and [flake8](https://gitlab.com/pycqa/flake8) have a line length of 120;\n- ... [flake8](https://gitlab.com/pycqa/flake8) and [isort](https://github.com/PyCQA/isort) are configured as above in `setup.cfg`;\n- ... [Pylint](https://www.pylint.org) is present as a [Poetry](https://github.com/python-poetry/poetry) dev dependency in `pyproject.toml`).\n\n## Quick setup\n\nTo try the package, simply install it (in a virtualenv or globally) and run `flake8` on a project with at least one Python (`.py`) file:\n\n    # Install using pip:\n    $ pip install -U nitpick\n\n    # Or using Poetry:\n    $ poetry add --dev nitpick\n\n    $ flake8 .\n\nNitpick will download and use the opinionated [default style file](https://raw.githubusercontent.com/andreoliwa/nitpick/v0.25.0/nitpick-style.toml).\n\nYou can use it as a template to configure your own style.\n\n### Run as a pre-commit hook (recommended)\n\nIf you use [pre-commit](https://pre-commit.com/) on your project (you should), add this to the `.pre-commit-config.yaml` in your repository:\n\n    repos:\n      - repo: https://github.com/andreoliwa/nitpick\n        rev: v0.25.0\n        hooks:\n          - id: nitpick\n\nTo install the `pre-commit` and `commit-msg` Git hooks:\n\n    pre-commit install --install-hooks\n    pre-commit install -t commit-msg\n\nTo start checking all your code against the default rules:\n\n    pre-commit run --all-files\n\n---\n\nFor more details on styles and which configuration files are currently supported, [see the full documentation](https://nitpick.rtfd.io/).\n',
    'author': 'W. Augusto Andreoli',
    'author_email': 'andreoliwa@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/andreoliwa/nitpick',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
