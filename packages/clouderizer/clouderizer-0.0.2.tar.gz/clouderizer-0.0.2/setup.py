# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clouderizer']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT>=1.7.0,<2.0.0',
 'coolname>=1.1.0,<2.0.0',
 'fire>=0.3.1,<0.4.0',
 'pipreqs>=0.4.0,<0.5.0',
 'prettytable>=0.7.2,<0.8.0',
 'requests>=2.7.0,<3.0.0',
 'requirements-parser>=0.2.0,<0.3.0']

entry_points = \
{'console_scripts': ['cldz = clouderizer.clouderizer:main']}

setup_kwargs = {
    'name': 'clouderizer',
    'version': '0.0.2',
    'description': '',
    'long_description': None,
    'author': 'Rohan Kothapalli',
    'author_email': 'rohan.kothapalli@clouderizer.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
