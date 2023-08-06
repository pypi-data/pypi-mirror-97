# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zerotwo', 'zerotwo.parastie']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'zero-two',
    'version': '0.1.1',
    'description': 'Zero Two',
    'long_description': '# zero-two\n\nArbitrary library used for testing publishing a python package using poetry.\n',
    'author': 'Michael Kim',
    'author_email': 'kim.michael95@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
