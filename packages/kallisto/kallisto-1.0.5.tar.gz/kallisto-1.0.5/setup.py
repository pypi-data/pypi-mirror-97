# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kallisto', 'kallisto.data', 'kallisto.reader', 'kallisto.utils']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'numpy>=1.19.0,<2.0.0', 'scipy>=1.5.2,<2.0.0']

entry_points = \
{'console_scripts': ['kallisto = kallisto.console:cli']}

setup_kwargs = {
    'name': 'kallisto',
    'version': '1.0.5',
    'description': 'The Kallisto software enables the efficient calculation of atomic features that can be used within a quantitative structure-activity relationship (QSAR) approach. Furthermore, several modelling helpers are implemented.',
    'long_description': '<div align="center">\n<img src="./assets/logo.svg" alt="Kallisto" width="300">\n</div>\n\n##\n\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/kallisto)\n[![Documentation](https://img.shields.io/badge/GitBook-Docu-lightgrey)](https://app.gitbook.com/@ehjc/s/kallisto/)\n[![Maturity Level](https://img.shields.io/badge/Maturity%20Level-ML--1-orange)](https://img.shields.io/badge/Maturity%20Level-ML--1-orange)\n[![Tests](https://github.com/AstraZeneca/kallisto/workflows/Tests/badge.svg)](https://github.com/AstraZeneca/kallisto/actions?workflow=Tests)\n[![codecov](https://codecov.io/gh/AstraZeneca/kallisto/branch/master/graph/badge.svg?token=HI0U0R96X8)](https://codecov.io/gh/AstraZeneca/kallisto)\n[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/AstraZeneca/kallisto.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/AstraZeneca/kallisto/context:python)\n[![status](https://joss.theoj.org/papers/16126cbcfb826bf4810d243a009a6b02/status.svg)](https://joss.theoj.org/papers/16126cbcfb826bf4810d243a009a6b02)\n\n# Table of Contents\n\n- Full Author List\n- Introduction\n- Installation\n- Testing suite\n- Reference\n\n# Full Author List\n\n- Developer [Eike Caldeweyher](https://scholar.google.com/citations?user=25n8C3wAAAAJ&hl=de)\n- Developer [Philipp Pracht](https://scholar.google.com/citations?user=PJiGPk0AAAAJ&hl=de)\n\n# Introduction\n\nWe developed the `kallisto` program for the efficient and robust calculation of atomic features using molecular geometries either in a ``xmol`` or a ``Turbomole`` format.\nFurthermore, several modelling tools are implemented, e.g., to calculate root-mean squared deviations via quaternions (including rotation matrices), sorting of molecular geometries and many more. All features of ``kallisto`` are described in detail within our [documentation](https://app.gitbook.com/@ehjc/s/kallisto/) ([GitBook repository](https://github.com/f3rmion/gitbook-kallisto)).\n\nMain dependencies\n-----------------\n\n```bash\nclick 7.1.2 Composable command line interface toolkit\nnumpy 1.20.1 NumPy is the fundamental package for array computing with Python.\nscipy 1.6.0 SciPy: Scientific Library for Python\n└── numpy >=1.16.5\n```\n\nFor a list of all dependencies have a look at the pyproject.toml file.\n\nInstallation from PyPI\n----------------------\n\nTo install ``kallisto`` via `pip` use our published PyPI package\n```bash\npip install kallisto\n```\n\nInstallation from Source\n------------------------\n\nRequirements to install ``kallisto``from sources:\n- [poetry](https://python-poetry.org/docs/#installation)\n- [pyenv](https://github.com/pyenv/pyenv#installation) or [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)\n- python >=3.7\n\nFirst check that ``poetry`` is running correctly (v1.0.10 at the time of writing)\n\n```bash\n> poetry --version\nPoetry version 1.0.10\n```\n\nCreate a virtual environment (via ``pyenv`` or ``conda``) and activate it. Afterwards, clone the ``kallisto`` project from GitHub and install it using ``poetry``\n\n```bash\n> git clone git@github.com:AstraZeneca/kallisto.git\n> cd kallisto\n> poetry install\n```\n\nTesting suite\n-------------\n\nThe ``kallisto`` project uses [nox](https://nox.thea.codes/en/stable/tutorial.html#installation) as an automated unit test suite, which is therefore an additional dependency.\n\n### Default nox session\n\nThe default session includes: linting (lint), type checks (mypy, pytype), and unit tests (tests). \n\n```bash\n> nox\n```\n\nWhen everything runs smoothly through, you are ready to go! After one successful nox run, we can reuse the created virtual environment via the ``-r`` flag.\n\n```bash\n> nox -r\n```\n\nDifferent unit test sessions are implemented (check the noxfile.py). They can be called separately via the run session ``-rs`` flag.\n\n### Tests\n\nRun all unit tests that are defined in the /tests directory.\n\n```bash \n> nox -rs tests\n```\n\n### Lint\n\n``kallisto`` uses the [flake8](https://flake8.pycqa.org/en/latest/) linter (check the .flake8 config file).\n\n```bash\n> nox -rs lint\n```\n\n### Black\n\n``kallisto`` uses the [black](https://github.com/psf/black) code formatter.\n\n```bash \n> nox -rs black\n```\n\n### Safety\n\n``kallisto`` checks the security of dependencies via [safety](https://pyup.io/safety/).\n\n```bash\n> nox -rs safety\n```\n\n### Mypy\n\n``kallisto`` checks for static types via [mypy](https://github.com/python/mypy) (check the mypy.ini config file).\n\n```bash\n> nox -rs mypy\n```\n\n### Pytype\n\n``kallisto`` furthermore uses [pytype](https://github.com/google/pytype) for type checks.\n\n```bash\n> nox -rs pytype\n```\n\n### Coverage\n\nUnit test [coverage](https://coverage.readthedocs.io/en/coverage-5.4/) can be checked as well.\n\n\n```bash\n> nox -rs coverage\n```\n\nReference\n---------\n\ntba\n',
    'author': 'Eike Caldeweyher',
    'author_email': 'hello@eikecaldeweyher.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AstraZeneca/kallisto',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
