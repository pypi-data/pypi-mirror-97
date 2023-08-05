# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aozorabunko_extractor']

package_data = \
{'': ['*']}

install_requires = \
['konoha>=4.6.2,<5.0.0']

entry_points = \
{'console_scripts': ['aozorabunko-extractor = aozorabunko_extractor.cli:main']}

setup_kwargs = {
    'name': 'aozorabunko-extractor',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'hppRC',
    'author_email': 'hpp.ricecake@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hpprc/aozorabunko-extractor',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
