# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dialogy',
 'dialogy.cli',
 'dialogy.constants',
 'dialogy.errors',
 'dialogy.parser',
 'dialogy.parser.text',
 'dialogy.parser.text.entity',
 'dialogy.plugin',
 'dialogy.postprocess',
 'dialogy.postprocess.text',
 'dialogy.postprocess.text.slot_filler',
 'dialogy.preprocess',
 'dialogy.preprocess.text',
 'dialogy.types',
 'dialogy.types.entity',
 'dialogy.types.intent',
 'dialogy.types.plugin',
 'dialogy.types.slots',
 'dialogy.types.utterances',
 'dialogy.utils',
 'dialogy.workflow']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.3.0,<21.0.0',
 'coloredlogs>=15.0,<16.0',
 'copier>=5.1.0,<6.0.0',
 'docopt>=0.6.2,<0.7.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'pytz>=2020.4,<2021.0',
 'requests>=2.25.1,<3.0.0',
 'watchdog>=1.0.2,<2.0.0']

entry_points = \
{'console_scripts': ['dialogy = dialogy.cli:main']}

setup_kwargs = {
    'name': 'dialogy',
    'version': '0.3.0',
    'description': 'Language understanding for human dialog.',
    'long_description': None,
    'author': 'Amresh Venugopal',
    'author_email': 'amresh.venugopal@gmail.com',
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
