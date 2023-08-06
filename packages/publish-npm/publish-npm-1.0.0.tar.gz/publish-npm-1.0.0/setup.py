# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['publish_npm']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['run = publish:main']}

setup_kwargs = {
    'name': 'publish-npm',
    'version': '1.0.0',
    'description': 'a script to update an NPM package',
    'long_description': None,
    'author': 'Zamiell',
    'author_email': '5511220+Zamiell@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
