# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pelican', 'pelican.plugins.social_cards']

package_data = \
{'': ['*']}

install_requires = \
['pelican>=4.5,<5.0', 'pillow']

extras_require = \
{'markdown': ['markdown>=3.2.2,<4.0.0']}

setup_kwargs = {
    'name': 'pelican-social-cards',
    'version': '0.0.2',
    'description': 'Plugin to generate social media cards with post title embedded',
    'long_description': '# Generate social media cards: A Plugin for Pelican\n\nPlugin to generate social media cards with post title embedded\n\n# Installation\n\n# Initial configuration\n\n# Configuration options\n\n# Contributing\n',
    'author': 'Mirek Długosz',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
