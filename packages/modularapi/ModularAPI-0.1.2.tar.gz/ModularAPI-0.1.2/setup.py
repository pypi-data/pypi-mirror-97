# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['modularapi', 'modularapi.templates.default']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.13,<4.0.0',
 'alembic>=1.5.5,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'psycopg2-binary>=2.8.6,<3.0.0',
 'pydantic>=1.8,<2.0']

entry_points = \
{'console_scripts': ['ModularAPI = modularapi.cli:cli']}

setup_kwargs = {
    'name': 'modularapi',
    'version': '0.1.2',
    'description': 'A CLI Framework based on FastAPI using module-based architecture.',
    'long_description': None,
    'author': 'Modular-lab',
    'author_email': 'contact.flapili@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://modular-lab.github.io/Modular-API/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
