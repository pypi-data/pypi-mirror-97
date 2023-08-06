# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['patina']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'patina',
    'version': '0.2.1',
    'description': 'Result and Option types for Python',
    'long_description': '# patina\n\n[![Documentation Status](https://readthedocs.org/projects/patina/badge/?version=latest)](https://patina.readthedocs.io/en/latest/?badge=latest)\n\nThis is an implementation of Rust\'s Result and Option types in Python. Most\nmethods have been implemented, and the (very good) [original documentation] has\nbeen adapted into docstrings.\n\nThe documentation for this package can be read [here][docs]. All doctests are\nrun and type-checked as part of the CI pipeline as unit tests. The tests are\ndirect ports of those in the Rust documentation.\n\n[original documentation]: https://doc.rust-lang.org/std/result/\n[docs]: https://result.readthedocs.io/en/latest\n\n## Why?\n\n2 reasons:\n- Python (in 3.10) now has pattern matching, wouldn\'t it be cool if we could\n  make the most of that?\n- Sometimes it\'s nice to have types for your errors.\n- Being able to `map` over possible failure can be very powerful.\n\nCheck this out:\n\n```python\nfrom patina import Some, None_\n\n# This value is an Option[str]\nmaybe_value = api_call_that_might_produce_a_value()\n\nmatch maybe_value.map(str.upper):  # Make it uppercase if it exists\n    case Some(val):\n        print("We got a val:", val)\n    case None_():  # Don\'t forget the parentheses (otherwise it\'s binding a name)\n        print("There was no val :(")\n```\n\nA similar thing can be done with the `Result` type (matching on `Ok` or `Err`).\nThis can be handy if you want to be more explicit about the fact that a function\nmight fail. If the function returns a `Result`, we can explicitly type the\npossible error values.\n\nIf this all sounds good, I recommend looking into functional programming,\nparticularly of the ML variety (e.g. Haskell, OCaml, SML) or Rust.\n',
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
