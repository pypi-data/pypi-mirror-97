# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['uhi', 'uhi.typing']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.8"': ['typing_extensions>=3.7'],
 'docs': ['sphinx>=3.0,<4.0',
          'sphinx_book_theme>=0.0.40',
          'sphinx_copybutton>=0.3.1'],
 'test': ['pytest>=5.2'],
 'test:python_version < "3.8"': ['importlib_metadata>=1.0']}

setup_kwargs = {
    'name': 'uhi',
    'version': '0.1.2',
    'description': 'Unified Histogram Interface: tools to help library authors work with histograms',
    'long_description': '# UHI\n\n\n[![Actions Status][actions-badge]][actions-link]\n[![Documentation Status][rtd-badge]][rtd-link]\n[![Code style: black][black-badge]][black-link]\n\n[![PyPI version][pypi-version]][pypi-link]\n[![PyPI platforms][pypi-platforms]][pypi-link]\n\n[![GitHub Discussion][github-discussions-badge]][github-discussions-link]\n[![Gitter][gitter-badge]][gitter-link]\n[![Scikit-HEP][sk-badge]](https://scikit-hep.org/)\n\n\nThis is a package meant primarily for [documenting][rtd-link] histogram indexing and the PlottableProtocol and any future cross-library standards. It also contains the code for the PlottableProtocol, to be used in type checking libraries wanting to conform to the protocol. Eventually, it might gain a set of tools for testing conformance to UHI indexing, as well. It is not currently intended to be a runtime dependency, but only a type checking, testing, and/or docs dependency in support of other libraries (such as [boost-histogram][], [hist][], [mplhep][], [uproot4][], and eventually [histoprint][]). It requires Python 3.6+.\n\n\n[actions-badge]:            https://github.com/Scikit-HEP/uhi/workflows/CI/badge.svg\n[actions-link]:             https://github.com/Scikit-HEP/uhi/actions\n[black-badge]:              https://img.shields.io/badge/code%20style-black-000000.svg\n[black-link]:               https://github.com/psf/black\n[conda-badge]:              https://img.shields.io/conda/vn/conda-forge/uhi\n[conda-link]:               https://github.com/conda-forge/uhi-feedstock\n[github-discussions-badge]: https://img.shields.io/static/v1?label=Discussions&message=Ask&color=blue&logo=github\n[github-discussions-link]:  https://github.com/Scikit-HEP/uhi/discussions\n[gitter-badge]:             https://badges.gitter.im/https://github.com/Scikit-HEP/uhi/community.svg\n[gitter-link]:              https://gitter.im/https://github.com/Scikit-HEP/uhi/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge\n[pypi-link]:                https://pypi.org/project/uhi/\n[pypi-platforms]:           https://img.shields.io/pypi/pyversions/uhi\n[pypi-version]:             https://badge.fury.io/py/uhi.svg\n[rtd-badge]:                https://readthedocs.org/projects/uhi/badge/?version=latest\n[rtd-link]:                 https://uhi.readthedocs.io/en/latest/?badge=latest\n[sk-badge]:                 https://scikit-hep.org/assets/images/Scikit--HEP-Project-blue.svg\n\n[boost-histogram]:          https://github.com/scikit-hep/boost-histogram\n[hist]:                     https://github.com/scikit-hep/hist\n[mplhep]:                   https://github.com/scikit-hep/mplhep\n[uproot4]:                  https://github.com/scikit-hep/uproot4\n[histoprint]:               https://github.com/scikit-hep/histoprint\n',
    'author': 'Henry Schreiner',
    'author_email': 'henryschreineriii@gmail.com',
    'maintainer': 'The Scikit-HEP admins',
    'maintainer_email': 'scikit-hep-admins@googlegroups.com',
    'url': 'https://github.com/Scikit-HEP/uhi',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
