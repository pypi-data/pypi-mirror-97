# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['azure_data_scraper_pkg_test']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2', 'lxml>=4.6.2,<5.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'azure-data-scraper-pkg-test',
    'version': '0.1.2',
    'description': '',
    'long_description': '[![Tests](https://github.com/timothymeyers/azure-data-scraper/actions/workflows/unit-test.yml/badge.svg)](https://github.com/timothymeyers/azure-data-scraper/actions/workflows/unit-test.yml)\n\n\n# azure-data-scraper\ntbd',
    'author': 'Tim Meyers',
    'author_email': 'timothy.m.meyers@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
