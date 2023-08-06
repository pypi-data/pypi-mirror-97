# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['note_clerk', 'note_clerk.checks']

package_data = \
{'': ['*']}

install_requires = \
['boltons>=20.0.0,<21.0.0',
 'click>=7.0,<8.0',
 'desert>=2020.1.6,<2021.0.0',
 'marshmallow>=3.5.1,<4.0.0',
 'orderedset>=2.0.3,<3.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'python-frontmatter>=0.5.0,<0.6.0',
 'requests>=2.23.0,<3.0.0',
 'ruamel.yaml>=0.16.12,<0.17.0']

entry_points = \
{'console_scripts': ['note-clerk = note_clerk.console:cli']}

setup_kwargs = {
    'name': 'note-clerk',
    'version': '0.0.12',
    'description': 'Utility to manage plain text notes.',
    'long_description': '# Note Clerk\n[![Tests](https://github.com/acjackman/note-clerk/workflows/Tests/badge.svg)](https://github.com/acjackman/note-clerk/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/acjackman/note-clerk/branch/master/graph/badge.svg)](https://codecov.io/gh/acjackman/note-clerk)\n[![PyPI](https://img.shields.io/pypi/v/note-clerk.svg)](https://pypi.org/project/note-clerk/)\n[![Read the Docs](https://readthedocs.org/projects/note-clerk/badge/)](https://note-clerk.readthedocs.io/)\n\nInstall development version\n\n```bash\npip install git+https://github.com/acjackman/note-clerk@master\n```\n\n\n## Contributing\n\nSee the contributing page in the docs.\n',
    'author': 'Adam Jackman',
    'author_email': 'adam@acjackman.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/acjackman/note-clerk',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
