# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['desdemona']

package_data = \
{'': ['*'], 'desdemona': ['static/*', 'templates/*']}

install_requires = \
['Flask-SocketIO>=5.0.1,<6.0.0',
 'Flask>=1.1.2,<2.0.0',
 'coolname>=1.1.0,<2.0.0',
 'dataclasses-json>=0.5.2,<0.6.0',
 'eventlet>=0.30.2,<0.31.0',
 'numpy>=1.20.1,<2.0.0',
 'python-socketio[client]>=5.0.4,<6.0.0']

entry_points = \
{'console_scripts': ['desdemona-player = desdemona.player:run',
                     'desdemona-server = desdemona.server:run']}

setup_kwargs = {
    'name': 'desdemona',
    'version': '0.1.0',
    'description': 'A server for othello AI games',
    'long_description': None,
    'author': 'Brian Cruz',
    'author_email': 'cruz.s.brian@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
