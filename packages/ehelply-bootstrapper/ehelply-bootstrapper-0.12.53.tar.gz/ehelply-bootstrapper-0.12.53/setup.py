# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ehelply_bootstrapper',
 'ehelply_bootstrapper.cli',
 'ehelply_bootstrapper.drivers',
 'ehelply_bootstrapper.drivers.aws_utils',
 'ehelply_bootstrapper.drivers.fast_api_utils',
 'ehelply_bootstrapper.events',
 'ehelply_bootstrapper.integrations',
 'ehelply_bootstrapper.models',
 'ehelply_bootstrapper.sockets',
 'ehelply_bootstrapper.utils']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.2,<4.0.0',
 'SQLAlchemy>=1.3.16,<2.0.0',
 'alembic>=1.4.2,<2.0.0',
 'boto3>=1.13.3,<2.0.0',
 'cryptography>=2.9.2,<3.0.0',
 'ehelply-batcher>=1.3.0,<2.0.0',
 'ehelply-cacher>=0.1.0,<0.2.0',
 'ehelply-logger>=0.0.8,<0.0.9',
 'email-validator>=1.1.0,<2.0.0',
 'fastapi>=0.54.1,<0.55.0',
 'hiredis>=1.1.0,<2.0.0',
 'isodate>=0.6.0,<0.7.0',
 'passlib[bcrypt]>=1.7.2,<2.0.0',
 'pdoc3>=0.9.2,<0.10.0',
 'pyjwt>=1.7.1,<2.0.0',
 'pylint>=2.5.2,<3.0.0',
 'pymlconf>=2.2.0,<3.0.0',
 'pymongo>=3.10.1,<4.0.0',
 'pymysql>=0.9.3,<0.10.0',
 'pyopenssl>=19.1.0,<20.0.0',
 'pytest-asyncio>=0.14.0,<0.15.0',
 'pytest-cov>=2.10.1,<3.0.0',
 'python-jose[cryptography]>=3.1.0,<4.0.0',
 'python-multipart>=0.0.5,<0.0.6',
 'python-slugify>=4.0.0,<5.0.0',
 'python-socketio>=4.5.1,<5.0.0',
 'python_dateutil>=2.8.1,<3.0.0',
 'redis>=3.5.0,<4.0.0',
 'requests>=2.23.0,<3.0.0',
 'sentry-asgi>=0.2.0,<0.3.0',
 'typer>=0.2.1,<0.3.0',
 'uvicorn>=0.11.5,<0.12.0',
 'wheel>=0.34.2,<0.35.0']

entry_points = \
{'console_scripts': ['ehelply_bootstrapper = '
                     'ehelply_bootstrapper.cli.cli:cli_main']}

setup_kwargs = {
    'name': 'ehelply-bootstrapper',
    'version': '0.12.53',
    'description': '',
    'long_description': "# Bootstrapper\nBootstrapper is used to quickly establish generic microservices.\n\n## What does it do\n\nBootstrapper takes care of several tedious and menial microservice tasks including:\n* Handles the loading process of microservices including a hand off back to the business logic\n* Abstracts away common integrations (referred to as drivers) such as MySQL, AWS (boto3), MongoDB, Redis, Sentry, SocketIO, FastAPI\n    * Each driver has varying levels of abstraction and completeness\n* Abstracts away environments. The bootstrapper treats the loading process differently depending on whether the service is in prod, qa, test, or dev\n* Exposes an API to the developer for creating integrations between microservices which are part of the same application. These are referred to as integrations.\n* Loads default and developer defined configuration files depending on the environment the service is in.\n* Exposes a singleton state manager to the microservice\n* Contains a small library of useful models, functions, and code for development of microservices.\n* Installs many common PyPi dependencies which are used across most microservices\n\n## What is isn't\n* Bootstrapper is not a microservice template, however, it can and should be used within microservice templates.\n    * Due to proprietary nature of microservice templates, eHelply has chosen not to offer one publicly at the moment. This decision may change in the future.\n* Perfect. There are many drivers which could be added or improved. Feel free to submit PRs to add new drivers.\n\n## Is this stable and production ready?\nThe quick and dirty answer is probably. eHelply is using Bootstrapper to power all of our microservices. For this reason, this project continues to mature and evolve over time. At this point, we would consider it to be reasonably stable. By no means is it feature complete, and it is possible for breaking changes to be introduced in the near or long term, but we don't expect the Bootstrapper to fail in production scenarios at this time.\n\nIn addition to this information, eHelply plans to launch microservices into production in late 2020 or early 2021, so we would expect this project to be officially production ready at that point in time.\n\n## Contributing\nThe goal of Bootstrapper is to be a generic microservice bootstrapper. This means that it should provide value to any company, organization, or individual that wishes to utilize it. For this reason, all contributions must also be generic and refrain from opinionated choices.\n\nSince eHelply is sponsoring the development of this project, it is unlikely that breaking changes would be accepted and merged in from third parties. However, we always welcome new (non-breaking) additions and bug fixes. And, who knows, if your breaking change is necessary, it will be merged in.\n\n## Commands\n* Run tests: `pytest`\n* Run tests with coverage report: `pytest --cov=ehelply_bootstrapper`\n",
    'author': 'Shawn Clake',
    'author_email': 'shawn.clake@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://ehelply.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
