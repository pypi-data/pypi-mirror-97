# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bgpfu', 'bgpfu.irr', 'bgpfu.prefixlist']

package_data = \
{'': ['*'], 'bgpfu': ['templates/*']}

install_requires = \
['Jinja2>=2.11.3,<3.0.0',
 'click>=7.1.2,<8.0.0',
 'gevent>=21.1.2,<22.0.0',
 'munge>=1.1.0,<2.0.0',
 'py-radix>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['bgpfu = bgpfu.cli:cli']}

setup_kwargs = {
    'name': 'bgpfu',
    'version': '0.2.0',
    'description': 'BGP toolkit',
    'long_description': None,
    'author': 'Matt Griswold',
    'author_email': 'grizz@20c.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
