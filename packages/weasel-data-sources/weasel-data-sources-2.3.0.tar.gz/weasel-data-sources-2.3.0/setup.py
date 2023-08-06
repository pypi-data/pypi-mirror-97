# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['weasel_data_sources', 'weasel_data_sources.mapping']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.12,<4.0.0',
 'requests>=2.25.1,<3.0.0',
 'ssdeep>=3.4,<4.0',
 'svn>=1.0.1,<2.0.0']

setup_kwargs = {
    'name': 'weasel-data-sources',
    'version': '2.3.0',
    'description': '`weasel-data-sources` is a collection of data sources to retrieve information about software releases and vulnerabilities.',
    'long_description': None,
    'author': 'Christopher Schmidt',
    'author_email': 'schmidtc@cs.uni-bonn.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
