# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['diffuse',
 'diffuse.diffuser',
 'diffuse.diffuser.tests',
 'diffuse.tests',
 'diffuse.worker',
 'diffuse.worker.tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'diffuse',
    'version': '0.2.0',
    'description': 'Python Diffuse',
    'long_description': "# Python Diffuse\n\n[![Build Status](https://travis-ci.org/asandeep/diffuse.svg?branch=master)](https://travis-ci.org/asandeep/diffuse)\n[![codecov](https://codecov.io/gh/asandeep/diffuse/branch/master/graph/badge.svg)](https://codecov.io/gh/asandeep/diffuse)\n[![license](https://img.shields.io/pypi/l/diffuse.svg)](https://github.com/asandeep/diffuse/blob/master/LICENSE)\n[![Python Versions](https://img.shields.io/pypi/pyversions/diffuse.svg)](https://pypi.org/project/diffuse/)\n[![Package Version](https://img.shields.io/pypi/v/diffuse.svg)](https://pypi.org/project/diffuse/)\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nDiffuse is yet another python library to run concurrent code.\n\nThe library builds upon standard library's `concurrent.futures` module and provides a consistent interface to run your code in separate Threads, Processes or ASyncIO coroutines.\n",
    'author': 'Sandeep Aggarwal',
    'author_email': 'asandeep.me@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://asandeep.github.io/diffuse/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
