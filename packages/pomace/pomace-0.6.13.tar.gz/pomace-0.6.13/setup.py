# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pomace', 'pomace.tests']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.8.2,<5.0.0',
 'bullet>=2.1.0,<3.0.0',
 'cleo>=0.8.1,<0.9.0',
 'datafiles>=0.12,<0.13',
 'faker>=4.1.1,<5.0.0',
 'gitman>=2.3,<3.0',
 'inflection>=0.4.0,<0.5.0',
 'ipython>=7.20.0,<8.0.0',
 'minilog>=2.0,<3.0',
 'parse>=1.14.0,<2.0.0',
 'splinter>=0.14.0,<0.15.0',
 'webdriver_manager>=2.5.0,<3.0.0',
 'zipcodes>=1.1.2,<2.0.0']

entry_points = \
{'console_scripts': ['pomace = pomace.cli:application.run']}

setup_kwargs = {
    'name': 'pomace',
    'version': '0.6.13',
    'description': 'Dynamic page objects for browser automation.',
    'long_description': "# Pomace\n\nDynamic page objects for browser automation.\n\n[![Unix Build Status](https://img.shields.io/travis/jacebrowning/pomace/main.svg?label=unix)](https://travis-ci.org/jacebrowning/pomace)\n[![Windows Build Status](https://img.shields.io/appveyor/ci/jacebrowning/pomace/main.svg?label=window)](https://ci.appveyor.com/project/jacebrowning/pomace)\n[![Coverage Status](https://img.shields.io/coveralls/jacebrowning/pomace/main.svg)](https://coveralls.io/r/jacebrowning/pomace)\n[![PyPI Version](https://img.shields.io/pypi/v/pomace.svg)](https://pypi.org/project/pomace)\n[![PyPI License](https://img.shields.io/pypi/l/pomace.svg)](https://pypi.org/project/pomace)\n\n# Usage\n\n## Quick Start\n\nOpen **Terminal.app** in macOS and paste:\n\n```\npython3 -m pip install --upgrade pomace && python3 -m pomace run\n```\n\nor if you have Homebrew:\n\n```\nbrew install pipx; pipx run --no-cache pomace run\n```\n\n## Installation\n\nIf you're planning to run Pomace multiple times, install it with [pipx](https://pipxproject.github.io/pipx/) first:\n\n```\npipx install pomace\n```\n\nor get the latest version:\n\n```\npipx upgrade pomace\n```\n\nThen download some site models:\n\n```\npomace clone https://github.com/jacebrowning/pomace-twitter.com\n```\n\nAnd launch the application:\n\n```\npomace run twitter.com\n```\n",
    'author': 'Jace Browning',
    'author_email': 'jacebrowning@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/pomace',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
