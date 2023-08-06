# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['panimg']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'panimg',
    'version': '0.0.1',
    'description': '',
    'long_description': '# panimg\n',
    'author': 'James Meakin',
    'author_email': '12661555+jmsmkn@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DIAGNijmegen/rse-panimg',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
