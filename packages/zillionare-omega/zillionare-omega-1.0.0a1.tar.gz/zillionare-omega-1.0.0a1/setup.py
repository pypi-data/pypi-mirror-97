# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['omega',
 'omega.config',
 'omega.core',
 'omega.fetcher',
 'omega.interfaces',
 'omega.interfaces.websockets',
 'omega.jobs',
 'omega.logging',
 'omega.logging.receiver']

package_data = \
{'': ['*'], 'omega.config': ['sql/*']}

install_requires = \
['APScheduler>=3.6,<4.0',
 'SQLAlchemy>=1.3.20,<2.0.0',
 'aiocache>=0.11.1,<0.12.0',
 'aiohttp>=3.7.3,<4.0.0',
 'aioredis>=1.3.1,<2.0.0',
 'arrow>=0.15,<0.16',
 'asyncpg>=0.21,<0.22',
 'cfg4py>=0.9.0,<0.10.0',
 'fire>=0.3.1,<0.4.0',
 'gino>=1.0,<2.0',
 'idna==2.5',
 'numpy>=1.18,<2.0',
 'pandas>=1.2.0,<2.0.0',
 'psutil>=5.7.3,<6.0.0',
 'pyarrow>=2.0.0,<3.0.0',
 'pyemit>=0.4.0,<0.5.0',
 'rlog==0.3',
 'sanic>=20.9.1,<21.0.0',
 'sh>=1.14.1,<2.0.0',
 'xxhash>=2.0.0,<3.0.0',
 'zillionare_omega_adaptors_jq>=0.3.5',
 'zillionare_omicron>=1.0.0.a0']

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
          'pytest-cov==2.10.1']}

entry_points = \
{'console_scripts': ['omega = omega.cli:main']}

setup_kwargs = {
    'name': 'zillionare-omega',
    'version': '1.0.0a1',
    'description': '高速分布式行情服务器',
    'long_description': '\n![](http://images.jieyu.ai/images/hot/zillionbanner.jpg)\n\n<p align="center">\n<a href="https://pypi.python.org/pypi/zillionare-omega">\n    <img src="http://img.shields.io/pypi/v/zillionare-omega?color=brightgreen" >\n</a>\n\n<a href="https://travis-ci.com/zillionare/omega">\n<img src="https://api.travis-ci.com/zillionare/omega.svg?branch=release">\n</a>\n\n<a href="https://omega.readthedocs.io/en/latest/?badge=latest">\n<img src="https://readthedocs.org/projects/omega/badge/?version=latest">\n</a>\n\n<a href="https://pepy.tech/project/zillionare-omega">\n<img src="https://pepy.tech/badge/zillionare-omega">\n</a>\n\n<a href="https://github.com/psf/black">\n<img src="https://img.shields.io/badge/code%20style-black-000000.svg">\n</a>\n\n<a href="https://opensource.org/licenses/MIT">\n<img src="https://img.shields.io/badge/License-MIT-yellow.svg">\n</a>\n</p>\n\n\n高速分布式本地行情服务器\n\n\n# 简介\n\nOmega为大富翁(Zillionare)智能量化交易平台提供数据服务。它是一个分布式、高性能的行情服务器，核心功能有：\n\n1. 并发对接多个上游数据源，如果数据源还支持多账户和多个并发会话的话，Omega也能充分利用这种能力，从而享受到最快的实时行情。目前官方已提供JoinQuant的数据源适配。\n\n2. 高性能和层次化的数据本地化存储，在最佳性能和存储空间上巧妙平衡。在需要被高频调用的行情数据部分，Omega直接使用Redis存储数据；财务数据一个季度才会变动一次，因而读取频率也不会太高，所以存放在关系型数据库中。这种安排为各种交易风格都提供了最佳计算性能。\n\n3. 优秀的可伸缩部署(scalability)特性。Omega可以根据您对数据吞吐量的需求，按需部署在单机或者多台机器上，从而满足个人、工作室到大型团队的数据需求。\n\n4. 自带数据(Battery included)。我们提供了从2015年以来的30分钟k线以上数据，并且通过CDN进行高速分发。安装好Omega之后，您可以最快在十多分钟内将这样巨量的数据同步到本地数据库。\n\n\n[帮助文档](https://zillionare-omega.readthedocs.io)\n\n鸣谢\n=========\n\nZillionare-Omega采用以下技术构建:\n\n[Pycharm开源项目支持计划](https://www.jetbrains.com/?from=zillionare-omega)\n\n![](_static/jetbrains-variant-3.svg)\n',
    'author': 'jieyu',
    'author_email': 'code@jieyu.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://zillionare-omega.readthedocs.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
