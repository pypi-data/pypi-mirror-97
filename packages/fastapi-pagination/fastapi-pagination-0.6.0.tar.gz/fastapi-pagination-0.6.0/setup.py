# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_pagination', 'fastapi_pagination.ext']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.61.2', 'pydantic>=1.7.2,<2.0.0', 'typing-extensions>=3.7.4,<4.0.0']

extras_require = \
{'all': ['gino[starlette]>=1.0.1,<2.0.0',
         'SQLAlchemy>=1.3.20,<2.0.0',
         'sqlalchemy-stubs>=0.4,<0.5',
         'databases[sqlite,mysql,postgresql]>=0.4.0,<0.5.0',
         'orm>=0.1.5,<0.2.0',
         'tortoise-orm[asyncpg,aiosqlite,aiomysql]>=0.16.18,<0.17.0'],
 'databases': ['databases[sqlite,mysql,postgresql]>=0.4.0,<0.5.0'],
 'gino': ['gino[starlette]>=1.0.1,<2.0.0',
          'SQLAlchemy>=1.3.20,<2.0.0',
          'sqlalchemy-stubs>=0.4,<0.5'],
 'orm': ['databases[sqlite,mysql,postgresql]>=0.4.0,<0.5.0',
         'orm>=0.1.5,<0.2.0'],
 'sqlalchemy': ['SQLAlchemy>=1.3.20,<2.0.0', 'sqlalchemy-stubs>=0.4,<0.5'],
 'tortoise': ['tortoise-orm[asyncpg,aiosqlite,aiomysql]>=0.16.18,<0.17.0']}

setup_kwargs = {
    'name': 'fastapi-pagination',
    'version': '0.6.0',
    'description': 'FastAPI pagination',
    'long_description': "# FastAPI Pagination\n\n[![License](https://img.shields.io/badge/License-MIT-lightgrey)](/LICENSE)\n[![codecov](https://github.com/uriyyo/fastapi-pagination/workflows/Test/badge.svg)](https://github.com/uriyyo/fastapi-pagination/actions)\n[![codecov](https://codecov.io/gh/uriyyo/fastapi-pagination/branch/main/graph/badge.svg?token=QqIqDQ7FZi)](https://codecov.io/gh/uriyyo/fastapi-pagination)\n[![Downloads](https://pepy.tech/badge/fastapi-pagination)](https://pepy.tech/project/fastapi-pagination)\n[![PYPI](https://img.shields.io/pypi/v/fastapi-pagination)](https://pypi.org/project/fastapi-pagination/)\n[![PYPI](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n## Installation\n\n```bash\n# Basic version\npip install fastapi-pagination\n\n# All available integrations\npip install fastapi-pagination[all]\n```\n\nAvailable integrations:\n\n* [sqlalchemy](https://github.com/sqlalchemy/sqlalchemy)\n* [gino](https://github.com/python-gino/gino)\n* [databases](https://github.com/encode/databases)\n* [orm](https://github.com/encode/orm)\n* [tortoise](https://github.com/tortoise/tortoise-orm)\n\n## Example\n\n```python\nfrom fastapi import FastAPI\nfrom pydantic import BaseModel\n\nfrom fastapi_pagination import Page, add_pagination, paginate\n\napp = FastAPI()\n\n\nclass User(BaseModel):\n    name: str\n    surname: str\n\n\nusers = [\n    User(name='Yurii', surname='Karabas'),\n    # ...\n]\n\n\n@app.get('/users', response_model=Page[User])\nasync def get_users():\n    return paginate(users)\n\n\nadd_pagination(app)\n```\n",
    'author': 'Yurii Karabas',
    'author_email': '1998uriyyo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/uriyyo/fastapi-pagination',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
