# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pythink_toolbox', 'pythink_toolbox.testing']

package_data = \
{'': ['*']}

install_requires = \
['pandera>=0.4.4,<0.7.0']

entry_points = \
{'console_scripts': ['cli = cli:main']}

setup_kwargs = {
    'name': 'pythink-toolbox',
    'version': '1.2.0',
    'description': 'TODO',
    'long_description': None,
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
