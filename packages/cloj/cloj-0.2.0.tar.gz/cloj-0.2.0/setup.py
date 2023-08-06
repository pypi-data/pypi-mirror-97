# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cloj']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cloj',
    'version': '0.2.0',
    'description': 'Clojure inspired helper functions',
    'long_description': '# Clojure inspired helper functions for Python\n\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cloj)\n![PyPI - License](https://img.shields.io/pypi/l/cloj)\n![PyPI](https://img.shields.io/pypi/v/cloj?color=blue)\n\nThis is a small library with Clojure inspired helper functions. It uses only the standard library, without any external dependencies.\n\nThe goal is to implement replicas of the Clojure funcs that I admire.\n\n## Installation\n\nWith [poetry](https://python-poetry.org/) (always recommended):\n```bash\npoetry add cloj\n```\n\nWith pip:\n```bash \npip install cloj\n```\n\nImplemented:\n* take/drop\n* take_while/drop_while\n* some\n* nth, first, second, third, fourth, fifth, forty_second, last\n* get-in\n\nSome examples:\n\n```python\nfrom cloj import take, drop\n\ntake(3, [1, 2, 3, 4, 5])\n>> [1, 2, 3]\n\ndrop(3, [1, 2, 3, 4, 5])\n>> [4, 5]\n\ndrop (100, [1, 2, 3, 4, 5])\n>> []\n```\n\n```python\nfrom cloj import first, second, third, fourth, fifth, forty_second, last\n\nfirst([1, 2, 3])\n>> 1\n\nlast([1, 2, 3])\n>> 3\n\nfirst([])\n>> None\n```\n\n```python\nfrom cloj import get_in\n\nsample = {"foo": {"bar": [0, {"spam": "target"}, 1]}}\nget_in(sample, ["foo", "bar", 1, "spam"])\n>>> "target"\n```\n',
    'author': 'MB',
    'author_email': 'mb@blaster.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/licht1stein/cloj',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
