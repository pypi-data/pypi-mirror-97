# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['playsongs']

package_data = \
{'': ['*']}

install_requires = \
['playsound>=1.2.2,<2.0.0']

setup_kwargs = {
    'name': 'playsongs',
    'version': '2021.1.0.6',
    'description': 'Play MP3s from a directory.',
    'long_description': '==============\n**PlaySongs**\n==============\n\nOverview\n--------\n\nPlay MP3 from a specified directory.\n\nPrerequisites\n-------------\n\n- *playsound* module (installed as a dependency)\n- **CAVEAT**: Due to *playsound* limitations, directory and filenames with spaces are not allowed.\n\nRequired (Positional) Arguments\n-------------------------------\n\n- Position 1: /path/to/mp3/files\n\nOptional (Keyword) Arguments\n----------------------------\n\n- repeat\n    - Description: Number of times to repeat the whole collection.\n    - Type: Integer\n    - Default: 0\n- shuffle\n    - Description: Select whether to shuffle the list of songs being played.\n    - Type: Boolean\n    - Default: False\n\nUsage\n-----\n\nInstallation:\n\n.. code-block:: BASH\n\n   pip3 install playsongs\n   # or\n   python3 -m pip install playsongs\n\nIn Python3:\n\n.. code-block:: BASH\n\n   from playsongs.playsongs import PlaySongs\n   PlaySongs(\'/home/username/Music\', repeat = 10000000, shuffle = True)\n\nIn BASH:\n\n.. code-block:: BASH\n\n   python3 -c "from playsongs.playsongs import PlaySongs; PlaySongs(\'/home/username/Music\', repeat = 10000000, shuffle = True)"\n\nChangelog\n---------\n\n2021.1.0.6\n\n- Updated README.\n\n2021.1.0.5\n\n- Updated code to return instead of exit in case of exceptions.\n\n2021.1.0.4\n\n- Updated typo in README (this file).\n- No code change.\n\n2021.1.0.3\n\n- Removed system exit at the end of the playlist so it won\'t kill Python runtime.\n- CTRL+C will still kill Python runtime.\n\n2021.1.0.1\n\n- Initial release.\n\n*Current version: 2021.1.0.6*\n',
    'author': 'Ahmad Ferdaus Abd Razak',
    'author_email': 'ahmad.ferdaus.abd.razak@ni.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fer1035/pypi-playsongs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
