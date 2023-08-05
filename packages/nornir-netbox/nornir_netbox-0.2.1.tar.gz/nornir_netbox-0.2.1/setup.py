# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nornir_netbox', 'nornir_netbox.plugins', 'nornir_netbox.plugins.inventory']

package_data = \
{'': ['*']}

install_requires = \
['nornir>=3,<4', 'requests>=2.23.0,<3.0.0']

entry_points = \
{'nornir.plugins.inventory': ['NBInventory = '
                              'nornir_netbox.plugins.inventory.netbox:NBInventory',
                              'NetBoxInventory2 = '
                              'nornir_netbox.plugins.inventory.netbox:NetBoxInventory2']}

setup_kwargs = {
    'name': 'nornir-netbox',
    'version': '0.2.1',
    'description': 'Netbox plugin for Nornir',
    'long_description': None,
    'author': 'Wim Van Deun',
    'author_email': '7521270+enzzzy@users.noreply.github.com',
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
