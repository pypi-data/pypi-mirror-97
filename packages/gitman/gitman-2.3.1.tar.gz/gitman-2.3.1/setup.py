# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gitman', 'gitman.models', 'gitman.tests']

package_data = \
{'': ['*'], 'gitman.tests': ['files/*']}

install_requires = \
['datafiles>=0.11', 'minilog>=2.0,<3.0']

entry_points = \
{'console_scripts': ['git-deps = gitman.plugin:main',
                     'gitman = gitman.cli:main']}

setup_kwargs = {
    'name': 'gitman',
    'version': '2.3.1',
    'description': 'A language-agnostic dependency manager using Git.',
    'long_description': '## Overview\n\nGitMan is a language-agnostic dependency manager using Git. It aims to serve as a submodules replacement and provides advanced options for managing versions of nested Git repositories.\n\n[![Demo](https://raw.githubusercontent.com/jacebrowning/gitman/main/docs/demo.gif)](https://asciinema.org/a/y3VenEKfLreczVpaLPbnU6AEQ)\n\n[![Unix Build Status](https://img.shields.io/travis/com/jacebrowning/gitman/main.svg?label=unix)](https://travis-ci.com/jacebrowning/gitman)\n[![Windows Build Status](https://img.shields.io/appveyor/ci/jacebrowning/gitman/main.svg?label=window)](https://ci.appveyor.com/project/jacebrowning/gitman)\n[![Coverage Status](https://img.shields.io/coveralls/jacebrowning/gitman/main.svg)](https://coveralls.io/r/jacebrowning/gitman)\n[![Scrutinizer Code Quality](https://img.shields.io/scrutinizer/g/jacebrowning/gitman.svg)](https://scrutinizer-ci.com/g/jacebrowning/gitman/?branch=main)\n[![PyPI Version](https://img.shields.io/pypi/v/GitMan.svg)](https://pypi.org/project/GitMan)\n[![PyPI License](https://img.shields.io/pypi/l/GitMan.svg)](https://pypi.org/project/GitMan)\n\n## Setup\n\n### Requirements\n\n- Python 3.7+\n- Git 2.8+ (with [stored credentials](http://gitman.readthedocs.io/en/latest/setup/git/))\n\n### Installation\n\nInstall this tool globally with [pipx](https://pipxproject.github.io/pipx/) (or pip):\n\n```sh\n$ pipx install gitman\n```\nor add it to your [Poetry](https://python-poetry.org/docs/) project:\n\n```sh\n$ poetry add gitman\n```\n\n### Configuration\n\nGenerate a sample config file:\n\n```sh\n$ gitman init\n```\n\nor manually create one (`gitman.yml` or `.gitman.yml`) in the root of your working tree:\n\n```yaml\nlocation: vendor/gitman\n\nsources:\n  - repo: https://github.com/kstenerud/iOS-Universal-Framework\n    name: framework\n    rev: Mk5-end-of-life\n  - repo: https://github.com/jonreid/XcodeCoverage\n    name: coverage\n    links:\n      - target: Tools/XcodeCoverage\n  - repo: https://github.com/dxa4481/truffleHog\n    name: trufflehog\n    rev: master\n    scripts:\n      - chmod a+x truffleHog/truffleHog.py\n  - repo: https://github.com/FortAwesome/Font-Awesome\n    name: fontawesome\n    rev: master\n    sparse_paths:\n      - "webfonts/*"\n  - repo: https://github.com/google/material-design-icons.git\n    name: material-design-icons\n    rev: master\n\ngroups:\n  - name: code\n    members:\n      - framework\n      - trufflehog\n  - name: resources\n    members:\n      - fontawesome\n      - material-design-icons\n\ndefault_group: code\n```\n\nIgnore the dependency storage location:\n\n```sh\n$ echo vendor/gitman >> .gitignore\n```\n\n## Usage\n\nSee the available commands:\n\n```sh\n$ gitman --help\n```\n\n### Updating Dependencies\n\nGet the latest versions of all dependencies:\n\n```sh\n$ gitman update\n```\n\nwhich will essentially:\n\n1. Create a working tree at `<root>`/`<location>`/`<name>`\n2. Fetch from `repo` and checkout the specified `rev`\n3. Symbolically link each `<location>`/`<name>` from `<root>`/`<link>` (if specified)\n4. Repeat for all nested working trees containing a config file\n5. Record the actual commit SHAs that were checked out (with `--lock` option)\n6. Run optional post-install scripts for each dependency\n\nwhere `rev` can be:\n\n- all or part of a commit SHA: `123def`\n- a tag: `v1.0`\n- a branch: `main`\n- a `rev-parse` date: `\'main@{2015-06-18 10:30:59}\'`\n\nAlternatively, get the latest versions of specific dependencies:\n\n```sh\n$ gitman update framework\n```\n\nor named groups:\n\n```sh\n$ gitman update resources\n```\n\n### Restoring Previous Versions\n\nDisplay the versions that are currently installed:\n\n```sh\n$ gitman list\n```\n\nReinstall these specific versions at a later time:\n\n```sh\n$ gitman install\n```\n\n### Deleting Dependencies\n\nRemove all installed dependencies:\n\n```sh\n$ gitman uninstall\n```\n\n## Resources\n\n- [Source code](https://github.com/jacebrowning/gitman)\n- [Issue tracker](https://github.com/jacebrowning/gitman/issues)\n- [Release history](https://github.com/jacebrowning/gitman/blob/main/CHANGELOG.md)\n',
    'author': 'Jace Browning',
    'author_email': 'jacebrowning@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/gitman',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
