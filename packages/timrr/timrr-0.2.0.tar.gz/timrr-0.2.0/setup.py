# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['timrr', 'timrr.core']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'tabulate>=0.8.9,<0.9.0']

setup_kwargs = {
    'name': 'timrr',
    'version': '0.2.0',
    'description': 'Time to submit while mobile working',
    'long_description': '# Time to submit while mobile working ヽ(´▽`)/\n[![Python application](https://github.com/MikeGlotzkowski/timr/actions/workflows/python-app.yml/badge.svg)](https://github.com/MikeGlotzkowski/timr/actions/workflows/python-app.yml)\n## Setup (currently)\n\n```bash\npython3 -m pip install poetry\npoetry install\npoetry shell\npoetry run python timrr/timrr.py calc\n```\n\n## Short Docu\n\n### calculate work time\n\n```bash\nUsage: timr.py calc [OPTIONS]\n\nOptions:\n  -s, --start-time TEXT\n  -e, --end-time TEXT\n  -b, --break-time TEXT\n  -ch, --contract-hours-per-day TEXT\n  --local-config / --no-local-config\n  --help\n```\n\n### configure defaults\n\n```bash\nUsage: timrr.py configure [OPTIONS]\n\nOptions:\n  --start-time TEXT              [required]\n  --end-time TEXT                [required]\n  --break-time TEXT              [required]\n  --contract-hours-per-day TEXT  [required]\n  --help                         Show this message and exit.\n```\n',
    'author': 'MikeGlotzkowski',
    'author_email': 'sebastian.lischewski@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
