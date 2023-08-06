# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bobolink']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'requests>=2.25.1,<3.0.0', 'termcolor>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['bobolink = bobolink.main:cli']}

setup_kwargs = {
    'name': 'bobolink',
    'version': '0.2.0',
    'description': 'bobolink stores bookmarks and helps you search for them later',
    'long_description': "# bobolink-cli\n\nbobolink helps user's store bookmarks and easily search for them later. In a nutshell, bobolink provides full text search on the HTML documents associated with user's bookmarks.\n\nFor more information on bobolink in general, users should refer to the documentation hosted on the [website.](https://bobolink.me)\n\n`bobolink-cli` is the command line interface to the public instance \nof the bobolink [backend.](https://github.com/jtanza/bobolink/). User's wishing to use bobolink just need to install the cli and signup. \n\n### Installation\n\n```\n$ python -m pip install bobolink\n```\n\n### Getting Started\n\nFor user's without a bobolink account, the fastest way to get going is to run\n`bobolink signup` after installation. This, followed by `bobolink configure` is all that is needed in order to start saving and searching your bookmarks.\n\nThe cli is heavily documented and can be accessed directly via \n`bobolink [COMMAND] --help`. Also as mentioned previously, additional documentation can be found directly on the bobolink [website.](https://bobolink.me)\n\n### Examples\n\nPlease refer to the terminal session below for a quick exploration of what's possible with bobolink.\n\n[![asciicast](https://asciinema.org/a/o1PdgoFQZrn9rn1kk3sdqRJjM.svg)](https://asciinema.org/a/o1PdgoFQZrn9rn1kk3sdqRJjM)\n",
    'author': 'jtanza',
    'author_email': 'tanzajohn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jtanza/bobolink-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
