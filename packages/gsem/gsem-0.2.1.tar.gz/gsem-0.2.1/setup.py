# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gsem']

package_data = \
{'': ['*']}

install_requires = \
['PyGObject>=3.38.0,<4.0.0']

entry_points = \
{'console_scripts': ['gsem = gsem.cli:main']}

setup_kwargs = {
    'name': 'gsem',
    'version': '0.2.1',
    'description': 'Command line extension manager for Gnome-Shell',
    'long_description': '# gsem\n\n[![PyPI version](https://badge.fury.io/py/gsem.svg)](https://pypi.org/project/gsem/)\n\n*gsem* - Command line extension manager for Gnome-Shell\n\n```\nusage: gsem [-h]\n            {ls,enabled,disabled,outdated,info,install,reinstall,uninstall,update,search,enable,disable}\n            ...\n\nGnome-Shell extension manager\n\npositional arguments:\n  {ls,enabled,disabled,outdated,info,install,reinstall,uninstall,update,search,enable,disable}\n    ls                  list installed extensions\n    enabled             list enabled extensions\n    disabled            list disabled extensions\n    outdated            list outdated extensions\n    info                show extension information\n    install             install extension\n    reinstall           reinstall extension\n    uninstall           uninstall extension\n    update              update extensions\n    search              search extensions\n    enable              enable extension\n    disable             disable extension\n\noptional arguments:\n  -h, --help            show this help message and exit\n```\n\n## Installation\n\n### User installation (recommended)\nRun `pip install --user gsem`\n\nMake sure you have `"$HOME/.local/bin"` in your `$PATH`.\n\n### Global installation\nRun `sudo pip install gsem`\n\n### Updating the package\n\nRun `pip install -U --user gsem` for user installation or `sudo pip install -U gsem` for global installation.\n\n## DONE:\n* list installed\n* list enabled/disabled\n* list outdated\n* extension info\n* search\n* enable/disable\n* install/uninstall/reinstall\n* update\n\n## Contributing\n\nDevelopment on latest python version is preferred, as of now it\'s 3.9.\nTo start you\'ll need the following setup:\n\nExample uses pyenv to install latest python and manage virtualenv. Run the following commands from the root of the repository.\n\n```sh\npyenv install 3.9.2           # install latest python version\npyenv virtualenv 3.9.2 gsem   # create gsem virtual environment\npyenv activate gsem           # activate the venv\npyenv local gsem              # set local python version for the repo\npoetry install                # install all dependencies inside the virtual environment\npre-commit install            # install pre-commit hooks\n```\n\nRun all the linters:\n```sh\npre-commit run -a\n```\n\n## TODO:\n* pin\n',
    'author': 'Andrii Kohut',
    'author_email': 'kogut.andriy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/andriykohut/gsem',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
