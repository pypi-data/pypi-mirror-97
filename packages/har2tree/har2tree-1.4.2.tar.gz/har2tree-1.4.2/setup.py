# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['har2tree']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'ete3>=3.1.2,<4.0.0',
 'filetype>=1.0.7,<2.0.0',
 'lxml>=4.6.2,<5.0.0',
 'numpy>=1.19.4,<2.0.0',
 'publicsuffix2>=2.20191221,<3.0',
 'six>=1.15.0,<2.0.0',
 'w3lib>=1.22.0,<2.0.0']

setup_kwargs = {
    'name': 'har2tree',
    'version': '1.4.2',
    'description': 'HTTP Archive (HAR) to ETE Toolkit generator',
    'long_description': "[![Build Status](https://travis-ci.org/Lookyloo/har2tree.svg?branch=master)](https://travis-ci.org/Lookyloo/har2tree)\n[![codecov](https://codecov.io/gh/Lookyloo/har2tree/branch/master/graph/badge.svg)](https://codecov.io/gh/Lookyloo/har2tree)\n\nHar2Tree\n========\n\n\nThis package generate a tree out of a HAR dump.\n\n\nInstallation\n============\n\nThe core dependency is ETE Toolkit, which you can install following the guide\non the official website: http://etetoolkit.org/download/\n\nNote: if you don't want to export the tree to an image using PyQt4, no need to do the\nvirtualenv magic.\n\nProtip\n======\n\nIf you like using virtualenv and have `pew` installed you can also do it this way:\n\n```\nsudo apt-get install python-qt4\npip install -r requirements.txt\npew toggleglobalsitepackages  # PyQt4 is not easily installable in a virtualenv\npip install -e .\n```\n",
    'author': 'Raphaël Vinot',
    'author_email': 'raphael.vinot@circl.lu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Lookyloo/har2tree',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
