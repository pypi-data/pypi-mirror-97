# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qctrlvisualizer']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=2.1',
 'numpy>=1.16,<2.0',
 'sphinx-rtd-theme>=0.4.3,<0.5.0',
 'toml>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'qctrl-visualizer',
    'version': '2.4.0',
    'description': 'Q-CTRL Python Visualizer',
    'long_description': '# Q-CTRL Python Visualizer\n\nProvides visualization of data for Q-CTRL’s Python products.\n',
    'author': 'Q-CTRL',
    'author_email': 'support@q-ctrl.com',
    'maintainer': 'Q-CTRL',
    'maintainer_email': 'support@q-ctrl.com',
    'url': 'https://q-ctrl.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.4,<4.0.0',
}


setup(**setup_kwargs)
