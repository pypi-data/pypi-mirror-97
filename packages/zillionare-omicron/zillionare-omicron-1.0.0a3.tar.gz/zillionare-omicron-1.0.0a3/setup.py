# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['omicron',
 'omicron.client',
 'omicron.config',
 'omicron.core',
 'omicron.dal',
 'omicron.models']

package_data = \
{'': ['*'], 'omicron.config': ['sql/*']}

install_requires = \
['SQLAlchemy>=1.3.20,<2.0.0',
 'aiohttp>=3.7.3,<4.0.0',
 'aioredis>=1.3.1,<2.0.0',
 'arrow>=0.15,<0.16',
 'asyncpg>=0.21.0,<0.22.0',
 'cfg4py>=0.9',
 'gino>=1.0.1,<2.0.0',
 'idna==2.5',
 'numpy>=1.18,<2.0',
 'pyemit>=0.4.0,<0.5.0',
 'scikit-learn>=0.23.2,<0.24.0',
 'sh>=1.14.1,<2.0.0']

extras_require = \
{'dev': ['pre-commit==2.8.2',
         'tox>=3.20.1,<4.0.0',
         'virtualenv>=20.2.2,<21.0.0',
         'pip>=20.3.1,<21.0.0',
         'twine>=3.3.0,<4.0.0'],
 'doc': ['mkdocs>=1.1.2,<2.0.0',
         'mkdocs-include-markdown-plugin>=1.0.0,<2.0.0',
         'mkdocs-material>=6.1.7,<7.0.0',
         'mkdocstrings>=0.13.6,<0.14.0'],
 'test': ['black==20.8b1',
          'isort==5.6.4',
          'doc8==0.8.1',
          'flake8==3.8.4',
          'pytest==6.1.2',
          'pytest-cov==2.10.1',
          'psutil>=5.7.3,<6.0.0']}

setup_kwargs = {
    'name': 'zillionare-omicron',
    'version': '1.0.0a3',
    'description': 'Core Library for Zillionare',
    'long_description': '\n![](http://images.jieyu.ai/images/hot/zillionbanner.jpg)\n\n<h1 align="center">Omicron - Core Library for Zillionare</h1>\n\n\n<p align="center">\n<a href="https://pypi.python.org/pypi/zillionare-omicron">\n    <img src="http://img.shields.io/pypi/v/zillionare-omicron?color=brightgreen" >\n</a>\n<a href="https://travis-ci.com/zillionare/omicron">\n<img src="https://api.travis-ci.com/zillionare/omicron.svg?branch=release">\n</a>\n<a href="https://omicron.readthedocs.io/en/latest/?badge=latest">\n<img src="https://readthedocs.org/projects/omicron/badge/?version=latest" >\n</a>\n<a href="https://github.com/psf/black/blob/master/LICENSE">\n<img src="https://black.readthedocs.io/en/stable/_static/license.svg" >\n</a>\n\n<a href="https://pepy.tech/project/zillionare-omicron">\n<img src="https://pepy.tech/badge/zillionare-omicron" >\n</a>\n<a href="https://github.com/psf/black">\n<img src="https://img.shields.io/badge/code%20style-black-000000.svg" >\n</a>\n\n<a href="https://opensource.org/licenses/MIT">\n<img src="https://img.shields.io/badge/License-MIT-yellow.svg" >\n</a>\n</p>\n\nContents\n---------\n\n* [installation](installation.md)\n## 简介\n\nOmicron是Zillionare的核心公共模块，实现了数据访问层，向其它模块提供行情、市值、交易日历、证券列表、时间操作及Trigger等功能。\n\n[使用文档](https://omicron.readthedocs.io/zh_CN/latest/)\n\n## Credits\n\nZillionare-Omicron采用以下技术构建:\n\n* Pycharm开源项目支持计划\n\n    ![](_static/jetbrains-variant-3.svg)\n\n* [Cookiecutter](https://github.com/audreyr/cookiecutter)\n* [Cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)\n',
    'author': 'jieyu',
    'author_email': 'code@jieyu.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://zillionare-omicron.readthedocs.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
