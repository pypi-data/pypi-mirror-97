# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['patina']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'patina',
    'version': '0.2.0',
    'description': 'Result and Option types for Python',
    'long_description': "# patina\n\n[![Documentation Status](https://readthedocs.org/projects/patina/badge/?version=latest)](https://patina.readthedocs.io/en/latest/?badge=latest)\n\nThis is an implementation of Rust's Result and Option types in Python. Most\nmethods have been implemented, and the (very good) [original documentation] has\nbeen adapted into docstrings.\n\nThe documentation for this package can be read [here][docs]. All doctests are\nrun and type-checked as part of the CI pipeline as unit tests. The tests are\ndirect ports of those in the Rust documentation.\n\n[original documentation]: https://doc.rust-lang.org/std/result/\n[docs]: https://result.readthedocs.io/en/latest",
    'author': 'Patrick Gingras',
    'author_email': '775.pg.12@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/p7g/patina',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
