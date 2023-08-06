# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zygoat',
 'zygoat.components',
 'zygoat.components.backend',
 'zygoat.components.backend.flake8',
 'zygoat.components.backend.flake8.resources',
 'zygoat.components.backend.resources',
 'zygoat.components.backend.settings',
 'zygoat.components.frontend',
 'zygoat.components.frontend.cypress',
 'zygoat.components.frontend.cypress.resources',
 'zygoat.components.frontend.dependencies',
 'zygoat.components.frontend.dependencies.resources',
 'zygoat.components.frontend.eslint',
 'zygoat.components.frontend.eslint.resources',
 'zygoat.components.frontend.prettier',
 'zygoat.components.frontend.prettier.resources',
 'zygoat.components.frontend.resources',
 'zygoat.components.proxy',
 'zygoat.components.proxy.resources',
 'zygoat.components.resources',
 'zygoat.utils']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'colorama>=0.4.3,<0.5.0',
 'importlib_metadata>=1.7.0,<2.0.0',
 'python-box[all]>=5.1.0,<6.0.0',
 'redbaron>=0.9.2,<0.10.0',
 'requests>=2.23.0,<3.0.0',
 'rtd-poetry>=0.1.0,<0.2.0',
 'ruamel.yaml>=0.16.10,<0.17.0',
 'virtualenv>=20.0,<21.0']

entry_points = \
{'console_scripts': ['zg = zygoat.cli:cli']}

setup_kwargs = {
    'name': 'zygoat',
    'version': '1.8.2',
    'description': '',
    'long_description': '# zygoat\n\n<img src="https://user-images.githubusercontent.com/640862/75250233-e287ea80-57a5-11ea-9d9f-553662a17706.jpeg" />\n\n## What is zygoat?\n\n`zygoat` is a command line tool used to bootstrap and configure a React/Django/Postgres stack web application.\n\nLinting, test configuration, boilerplate, and development environment are automatically taken care of using `zygoat` so that you can get up and running faster.\n\n`zygoat` also includes a preset deployment configuration to allow you to deploy your stack to an AWS environment with a single command. You\'ll get a full serverless AWS stack to keep things inexpensive and nimble.\n\n## How does it work?\n\n`zygoat` works by defining `Components`, defined as parts of projects, and then defining how you implement those components based on whether you\'re creating a new project, updating an existing project, or deleting a component that\'s no longer needed.\n\nFor instance, for the python backend, we want to include `black`, which is a tool for automatically formatting python code in a standard way to make it pep8 compliant. To install `black` in for the python backend part of the project, we create a `Component` for it, specifically a `FileComponent`, which defines how we treat files that we need in projects. Then we register the `Black` component (defined in [black.py](https://github.com/bequest/zygoat/blob/master/zygoat/components/backend/black.py)) with the `Backend` component (defined in [backend/\\_\\_init\\_\\_.py](https://github.com/bequest/zygoat/blob/master/zygoat/components/backend/__init__.py)) as a sub component. This way, whenever you create or update (or delete) a project with the `Backend` component, you\'ll do the same \'phase\' to the `Black` component.\n\n## How do I use it?\n\nMake a new git repository somewhere, we\'ll call it test-zg\n\n```bash\nmkdir test-zg && cd test-zg\ngit init\n```\n\nInstall the zygoat package locally\n\n```bash\npip install --user --upgrade ~/Projects/zygoat  # Or wherever you have it\n```\n\nIf you\'re using the asdf version manager, reshim\n\n```bash\nasdf reshim python\n```\n\nRun zg commands, see if they fail\n\n```bash\nzg new test\nzg update\nzg delete\n```\n\n---\n\n## Contributing\n\n`zygoat` is developed using the [Poetry](https://python-poetry.org/docs/) packaging framework for Python projects to make development as simple and portable as possible.\n\n---\n\n## Documentation\n\n[Available on ReadTheDocs](https://zygoat.readthedocs.io/en/latest/)\n',
    'author': 'Bequest, Inc.',
    'author_email': 'oss@willing.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
