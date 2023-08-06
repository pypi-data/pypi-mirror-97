# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['inmanta_dev_dependencies']

package_data = \
{'': ['*']}

install_requires = \
['black==20.8b1',
 'flake8-black==0.2.1',
 'flake8-copyright==0.2.2',
 'flake8-isort==4.0.0',
 'flake8==3.8.4',
 'isort==5.7.0',
 'lxml==4.6.2',
 'mypy==0.800',
 'pep8-naming==0.11.1',
 'pytest==6.2.2']

extras_require = \
{'async': ['pytest-asyncio==0.14.0', 'pytest-timeout==1.4.2'],
 'core': ['pytest-env==0.6.2',
          'pytest-postgresql==2.6.0',
          'psycopg2==2.8.6',
          'tox==3.22.0',
          'asyncpg>=0.21.0,<1.0.0',
          'tornado>=6.1,<7.0'],
 'extension': ['pytest-inmanta-extensions',
               'pytest-env==0.6.2',
               'pytest-postgresql==2.6.0',
               'psycopg2==2.8.6',
               'tox==3.22.0',
               'asyncpg>=0.21.0,<1.0.0',
               'tornado>=6.1,<7.0'],
 'module': ['pytest-inmanta'],
 'pytest': ['pytest-env==0.6.2',
            'pytest-cover==3.0.0',
            'pytest-randomly==3.5.0',
            'pytest-xdist==2.2.1',
            'pytest-sugar==0.9.4',
            'pytest-sugar==0.9.4',
            'pytest-instafail==0.4.2',
            'pytest-instafail==0.4.2'],
 'sphinx': ['inmanta-sphinx==1.3.1',
            'sphinx-argparse==0.2.5',
            'sphinx-autodoc-annotation==1.0-1',
            'sphinx-rtd-theme==0.5.1',
            'sphinx-tabs==2.0.1',
            'Sphinx==3.5.1',
            'sphinxcontrib-serializinghtml==1.1.4',
            'sphinxcontrib-redoc==1.6.0',
            'sphinx-click==2.5.0']}

setup_kwargs = {
    'name': 'inmanta-dev-dependencies',
    'version': '1.25.0',
    'description': 'Package collecting all common dev dependencies of inmanta modules and extensions to synchronize dependency versions.',
    'long_description': None,
    'author': 'Inmanta',
    'author_email': 'code@inmanta.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
