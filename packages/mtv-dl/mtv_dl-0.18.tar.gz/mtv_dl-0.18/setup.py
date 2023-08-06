# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['mtv_dl']
install_requires = \
['PyYAML>=5.3,<6.0',
 'beautifulsoup4>=4.8.2,<5.0.0',
 'docopt>=0.6.2,<0.7.0',
 'durationpy>=0.5',
 'iso8601>=0.1.12,<0.2.0',
 'pydash>=4.7.6,<5.0.0',
 'rfc6266>=0.0.4,<0.0.5',
 'rich>=2.2.3,<3.0.0',
 'typing_extensions>=3.7.4,<4.0.0',
 'tzlocal>=2.0.0,<3.0.0']

entry_points = \
{'console_scripts': ['mtv_dl = mtv_dl:main']}

setup_kwargs = {
    'name': 'mtv-dl',
    'version': '0.18',
    'description': 'MediathekView Downloader',
    'long_description': 'Command line tool to download videos from sources available through MediathekView.\n',
    'author': 'Frank Epperlein',
    'author_email': 'frank+mtv_dl@epperle.in',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/efenka/mtv_dl',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
