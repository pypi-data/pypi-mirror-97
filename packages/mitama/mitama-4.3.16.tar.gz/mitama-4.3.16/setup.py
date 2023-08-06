# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mitama',
 'mitama.app',
 'mitama.app.forms',
 'mitama.app.http',
 'mitama.db',
 'mitama.db.driver',
 'mitama.models',
 'mitama.portal',
 'mitama.project',
 'mitama.skeleton.app_templates',
 'mitama.skeleton.project',
 'mitama.utils']

package_data = \
{'': ['*'],
 'mitama.app': ['static/*', 'templates/*', 'templates/base/*'],
 'mitama.portal': ['static/*',
                   'templates/*',
                   'templates/apps/*',
                   'templates/group/*',
                   'templates/user/*'],
 'mitama.skeleton.app_templates': ['static/*', 'templates/*']}

install_requires = \
['Jinja2>=2.11.3,<3.0.0',
 'Markdown>=3.3.3,<4.0.0',
 'Pillow>=8.1.0,<9.0.0',
 'PyJWT>=2.0.1,<3.0.0',
 'SQLAlchemy>=1.3.23,<2.0.0',
 'bcrypt>=3.2.0,<4.0.0',
 'jinja-markdown>=1.200630,<2.0',
 'pycryptodome>=3.10.1,<4.0.0',
 'pysaml2>=6.5.1,<7.0.0',
 'python-magic>=0.4.22,<0.5.0',
 'tzlocal>=2.1,<3.0',
 'watchdog>=2.0.1,<3.0.0',
 'yarl>=1.6.3,<2.0.0']

entry_points = \
{'console_scripts': ['mitama = mitama:command_exec']}

setup_kwargs = {
    'name': 'mitama',
    'version': '4.3.16',
    'description': '',
    'long_description': None,
    'author': 'boke0',
    'author_email': 'speken00.tt@gmail.com',
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
