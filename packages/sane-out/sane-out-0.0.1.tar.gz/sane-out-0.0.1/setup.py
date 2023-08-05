# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sane_out']

package_data = \
{'': ['*']}

extras_require = \
{':sys_platform == "win32"': ['colorama>=0.4.4,<0.5.0']}

setup_kwargs = {
    'name': 'sane-out',
    'version': '0.0.1',
    'description': 'A lightweight library for clean console output',
    'long_description': '# sane-out for Python\n\n> A lightweight library for clean console output\n\n## License\n\nMIT © Nikita Karamov\n',
    'author': 'Nikita Karamov',
    'author_email': 'nick@karamoff.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sane-out/python',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
