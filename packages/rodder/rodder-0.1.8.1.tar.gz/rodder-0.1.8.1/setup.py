# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rodder']

package_data = \
{'': ['*']}

install_requires = \
['pygit2>=1.5.0,<2.0.0']

setup_kwargs = {
    'name': 'rodder',
    'version': '0.1.8.1',
    'description': 'A distro-independant package manager for Linux',
    'long_description': '# rodder\nA distro-independent (or distro-agonistic if you wanna be fancy), non-system package manager with custom repos, similar to Homebrew\n\n# FAQ\n\n## Why "rodder"?\nBecause a fishing rod grabs fish, similar to how a package manager grabs packages.\n\n# Notes\n\n## PyPI CLI Interface\n\nIf you want to run the command line app from the PyPI installer, please use the command\n```python -m rodder.rodder [command]```\nI\'ve no fucking idea how to fix this, so deal with it I guess.\n\n## PyPI Library\n\nSimilarly (although less bad), if you want to import the package and use it, I recommend using\n```import rodder.rodder as rodder```\nso you can do `rodder.help()`, `rodder.install(\'package\')`, etc. etc.\n\nI\'ll have some docs up on the library soonish, but it\'s pretty simple, just look at the code\n',
    'author': 'Drake',
    'author_email': 'mdrakea3@tutanota.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Ruthenic/rodder',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
