# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['begroing_index', 'begroing_index.begroing']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'begroing-index',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Håkon Drolsum Røkenes',
    'author_email': 'hakon.drolsum.rokenes@niva.no',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
