# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datek_agar_kivy']

package_data = \
{'': ['*']}

install_requires = \
['Kivy>=2.0.0,<3.0.0', 'datek-agar-core>=0.1.0,<0.2.0', 'numpy>=1.20.0,<2.0.0']

entry_points = \
{'console_scripts': ['agar-kivy = datek_agar_kivy.agar:main']}

setup_kwargs = {
    'name': 'datek-agar-kivy',
    'version': '0.1.0',
    'description': 'Kivy client for Agar game',
    'long_description': '# Agar - Kivy\nKivy client for `datek-agar-core`.\nThe project is in early development stage.\n\n## Usage\nAfter installation, run the `agar-kivy` command.\n\n## Controls\nincrease speed: &#8593;  \ndecrease speed: &#8595;  \nturn left: &#8592;  \nturn right: &#8594;',
    'author': 'Attila Dudas',
    'author_email': 'dudasa7@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/datek-agar/agar-core',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
