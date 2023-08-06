# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hmip2mqtt']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'getmac>=0.8.2,<0.9.0',
 'homematicip>=0.13.1,<0.14.0',
 'paho-mqtt>=1.5.1,<2.0.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['hmip2mqtt = hmip2mqtt.cli:main']}

setup_kwargs = {
    'name': 'hmip2mqtt',
    'version': '1.0.0',
    'description': 'Connects a Homematic IP Cloud installation to MQTT',
    'long_description': None,
    'author': 'Markus Mohnen',
    'author_email': 'markus.mohnen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
