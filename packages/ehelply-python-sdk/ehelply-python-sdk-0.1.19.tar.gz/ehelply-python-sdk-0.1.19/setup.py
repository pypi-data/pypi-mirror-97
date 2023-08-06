# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ehelply_python_sdk',
 'ehelply_python_sdk.services',
 'ehelply_python_sdk.services.access',
 'ehelply_python_sdk.services.meta',
 'ehelply_python_sdk.services.notes',
 'ehelply_python_sdk.services.security']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=2.9.2,<3.0.0',
 'ehelply-logger>=0.0.8,<0.0.9',
 'isodate>=0.6.0,<0.7.0',
 'passlib[bcrypt]>=1.7.2,<2.0.0',
 'pdoc3>=0.9.2,<0.10.0',
 'pydantic>=1.7.3,<2.0.0',
 'pyjwt>=1.7.1,<2.0.0',
 'pyopenssl>=19.1.0,<20.0.0',
 'pytest-asyncio>=0.14.0,<0.15.0',
 'pytest-cov>=2.10.1,<3.0.0',
 'python-jose[cryptography]>=3.1.0,<4.0.0',
 'python-slugify>=4.0.0,<5.0.0',
 'python_dateutil>=2.8.1,<3.0.0',
 'requests>=2.23.0,<3.0.0',
 'typer>=0.2.1,<0.3.0',
 'wheel>=0.34.2,<0.35.0']

entry_points = \
{'console_scripts': ['ehelply_sdk = ehelply_python_sdk.cli:cli_main']}

setup_kwargs = {
    'name': 'ehelply-python-sdk',
    'version': '0.1.19',
    'description': '',
    'long_description': '# SDK',
    'author': 'Shawn Clake',
    'author_email': 'shawn.clake@ehelply.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://ehelply.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
