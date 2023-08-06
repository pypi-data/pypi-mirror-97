# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xontrib', 'xontrib.avox_poetry']

package_data = \
{'': ['*']}

install_requires = \
['xonsh>=0.9.20']

setup_kwargs = {
    'name': 'xontrib-avox-poetry',
    'version': '0.2.1',
    'description': 'auto-activate venv as one cd into a poetry project',
    'long_description': '<p align="center">\nauto-activate venv as one cd into a poetry project folder.\n</p>\n\n## Installation\n\nTo install use pip:\n\n``` bash\nxpip install xontrib-avox-poetry\n# or: xpip install -U git+https://github.com/jnoortheen/xontrib-avox-poetry\n```\n\n## Usage\n\n``` bash\nxontrib load avox_poetry\n```\n\n## Configuration\n\n```python\n# name of the venv folder. If found will activate it.\n# if set to None then local folder activation will not work.\n$XSH_AVOX_VENV_NAME = ".venv"\n\n# exclude activation of certain paths by setting\n$XSH_AVOX_EXCLUDED_PATHS = {"xsh-src"}\n```\n\n## Credits\n\nThis package was created with [xontrib cookiecutter template](https://github.com/jnoortheen/xontrib-cookiecutter).\n',
    'author': 'Noortheen Raja NJ',
    'author_email': 'jnoortheen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jnoortheen/xontrib-avox-poetry',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
