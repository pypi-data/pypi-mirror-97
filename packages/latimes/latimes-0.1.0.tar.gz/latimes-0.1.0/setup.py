# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['latimes']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'click>=7.1.2,<8.0.0', 'pytz>=2021.1,<2022.0']

entry_points = \
{'console_scripts': ['latime = latimes.__main__:main',
                     'latimes = latimes.__main__:main']}

setup_kwargs = {
    'name': 'latimes',
    'version': '0.1.0',
    'description': 'Convierte tiempos',
    'long_description': None,
    'author': 'Antonio Feregrino',
    'author_email': 'antonio.feregrino@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
