# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['PrognosAIs',
 'PrognosAIs.IO',
 'PrognosAIs.Model',
 'PrognosAIs.Model.Architectures',
 'PrognosAIs.Preprocessing']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'SimpleITK>=1.2.4,<3.0.0',
 'h5py>=2.10.0,<3.0.0',
 'matplotlib>=3.2.1,<4.0.0',
 'natsort>=7.0.1,<8.0.0',
 'numba>=0.49.1,<0.53.0',
 'numpy>=1.18,<2.0',
 'pandas>=1.0.3,<2.0.0',
 'psutil>=5.7.0,<6.0.0',
 'scikit-learn>=0.23,<0.25',
 'slurmpie>=0.4.0,<0.5.0',
 'tensorboard_plugin_profile>=2.2.0,<3.0.0',
 'tensorflow-addons>=0.11',
 'tensorflow-io>=0.15',
 'tensorflow>=2.2.0']

setup_kwargs = {
    'name': 'prognosais',
    'version': '0.3.3',
    'description': 'Tool to quickly and easily train CNNs for medical imaging tasks',
    'long_description': '[![Documentation Status](https://readthedocs.org/projects/prognosais/badge/?version=latest)](https://prognosais.readthedocs.io/en/latest/?badge=latest) [![codecov](https://codecov.io/gh/Svdvoort/prognosais/branch/master/graph/badge.svg?token=HTHVINR6Y8)](https://codecov.io/gh/Svdvoort/prognosais) [![Python test](https://github.com/Svdvoort/prognosais/workflows/Python%20test/badge.svg)](https://github.com/Svdvoort/prognosais/actions?query=workflow%3A%22Python+test%22)[![CodeFactor](https://www.codefactor.io/repository/github/svdvoort/prognosais/badge)](https://www.codefactor.io/repository/github/svdvoort/prognosais)[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![Dependabot](https://flat.badgen.net/dependabot/Svdvoort/prognosais?icon=dependabot)](https://github.com/Svdvoort/prognosais/pulls?q=is%3Aopen+is%3Apr+label%3Adependencies)\n\n# prognosais\n\nprognosais is a tool to quickly prototype some CNNs for medical classification and segmentations tasks.\nPlease read the documentation: https://prognosais.readthedocs.io/en/latest/?badge=latest\n',
    'author': 'Sebastian van der Voort',
    'author_email': 'svoort25@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Svdvoort/prognosais',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.9',
}


setup(**setup_kwargs)
